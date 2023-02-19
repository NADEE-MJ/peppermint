from os import system

import typer
from rich import print

app = typer.Typer()


@app.command()
def all(warn: bool = False) -> None:
    print("[green]Running all tests![/green]")
    system(f"poetry run pytest backend/src/tests {'' if warn else '--disable-warnings'}")


@app.command()
def coverage(warn: bool = False) -> None:
    print("[green]Running all tests![/green]")
    system(f"poetry run pytest --cov=src --cov-report=html backend/src/tests {'' if warn else '--disable-warnings'}")


@app.command()
def filter(test_file: str, warn: bool = False) -> None:
    print(f"[green]Running {test_file} test(s)![/green]")
    system(f"poetry run pytest {test_file} {'' if warn else '--disable-warnings'}")


app()
