import base64
import csv
from io import StringIO

from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.category import CategoryCreate
from src.models.transaction import TransactionCreate


async def parser(db: AsyncSession, *, mapping: dict, file: str, user_id: int, account_id: int, budget_id: int) -> bool:
    # mapping example {"Date": "date", "Description": "desc", "Amount": "amnt"}
    # mapping example with category {"Date": "date", "Description": "desc", "Amount": "amnt", "Category": "category"}

    # Example Header row from a csv file
    # Transaction Date,Clear Date,Description,Category,Amount,Current Balance

    filterData = await crud.filter.get_all_filters_for_user(db, user_id=user_id, limit=-1)
    if filterData is not None:
        filters = filterData["paginated_results"]
    else:
        filters = None
    categoryData = await crud.category.get_all_categories_for_user(db, user_id=user_id, limit=-1)
    if categoryData is not None:
        categories = categoryData["paginated_results"]
    else:
        categories = None
    default_category = await crud.category.get_unsorted_category_for_budget(db, user_id=user_id, budget_id=budget_id)
    if default_category:
        default_category_id = default_category.id
    else:
        categoryCreate = CategoryCreate(name="Unsorted", desc="Created when uploading a file", amount=-1)
        new_category = await crud.category.create(db, obj_in=categoryCreate, user_id=user_id, budget_id=budget_id)
        default_category_id = new_category.id

    decoded_data = base64.b64decode(file.split(",")[1])
    lines = decoded_data.decode("utf-8")

    csvfile = StringIO(lines)
    csvreader = csv.reader(csvfile)
    file_lines = iter(csvreader)
    header_row = next(file_lines)
    indexes = {}
    # to figure out column mapping
    for col in header_row:
        if col in mapping:
            index = header_row.index(col)
            indexes[index] = mapping[col]
    # indexes example value {0: "date", 2: "desc", 4: "amnt"}
    has_categories = False
    if "category" in indexes.values():
        has_categories = True

    for row in csvreader:
        # row example = 3/11/2023,3/12/2023,THIS IS A DESCRIPTION,3000,Food,1000000
        split_row = row
        new_transaction = {}
        for index, column_name in indexes.items():
            try:
                new_transaction[column_name] = split_row[index]
            except IndexError:
                # this most likely means that the csv file is not formatted correctly
                return False
        category_id = None
        if has_categories and new_transaction["category"] is not None:
            if categories is not None and isinstance(categories, list):
                for category in categories:
                    if category.name.lower() == new_transaction["category"].lower():
                        category_id = category.id
                        break

            if category_id is None and new_transaction["category"] is not None and new_transaction["category"] != "":
                categoryCreate = CategoryCreate(
                    name=new_transaction["category"], desc="Created when uploading a file", amount=-1
                )
                new_category = await crud.category.create(
                    db, obj_in=categoryCreate, user_id=user_id, budget_id=budget_id
                )
                categoryData = await crud.category.get_all_categories_for_user(db, user_id=user_id)
                if categoryData is not None:
                    categories = categoryData["paginated_results"]
                category_id = new_category.id

        # new_transaction {"date": "3/11/2023", "desc": "THIS IS A DESCRIPTION", "amnt": "3000"}
        if filters is not None and type(filters) == list:
            for filter in filters:
                if filter.filter_by.lower() in new_transaction["desc"].lower():
                    category_id = filter.category_id
                    break

        if category_id is None:
            category_id = default_category_id

        transaction_create = TransactionCreate(
            amount=float(new_transaction["amnt"]), desc=new_transaction["desc"], date=new_transaction["date"]
        )

        await crud.transaction.create(
            db,
            obj_in=transaction_create,
            user_id=user_id,
            category_id=category_id,
            account_id=account_id,
            budget_id=budget_id,
        )

    return True
