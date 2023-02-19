from os import system

import typer
from rich import print

app = typer.Typer()

PATH: str = "backend/"


@app.command()
def create(new_migration_name: str) -> None:
    print(f"[green]Creating migration {new_migration_name}[/green]")
    system(f"cd {PATH} && poetry run python -m alembic revision --autogenerate -m {new_migration_name}")


@app.command()
def fresh(seed: bool = False) -> None:
    print("[green]Downgrading to base[/green]")
    system(f"cd {PATH} && poetry run python -m alembic downgrade base")
    print("[green]Upgrading to head[/green]")
    system(f"cd {PATH} && poetry run python -m alembic upgrade head")

    if seed:
        print("[green]Seeding database![/green]")
        system(f"cd {PATH} && poetry run python src/db/seed.py")


@app.command()
def up(num_of_steps: int = 1) -> None:
    print(f"[green]Running {num_of_steps} migrations[/green]")
    system(f"cd {PATH} && poetry run python -m alembic upgrade +{num_of_steps}")


@app.command()
def down(num_of_steps: int = 1) -> None:
    print(f"[green]Dropping {num_of_steps} migrations[/green]")
    system(f"cd {PATH} && poetry run python -m alembic downgrade -{num_of_steps}")


app()
