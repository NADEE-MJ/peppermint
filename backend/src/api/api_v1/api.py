from fastapi import APIRouter
from src.api.api_v1.endpoints import accounts, budgets, login, users, utils, transactions, categories, filters

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(filters.router, prefix="/filters", tags=["filters"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
