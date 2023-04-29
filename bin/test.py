from os import system

import typer
from rich import print

app = typer.Typer()


@app.command()
def all(warn: bool = False) -> None:
    print("[bright_blue u bold]Running all backend tests!")
    system(f"poetry run pytest backend/src/tests {'' if warn else '--disable-warnings'}")


@app.command()
def coverage(warn: bool = False) -> None:
    print("[bright_blue u bold]Running all backend tests and generating coverage report!")
    system(f"poetry run pytest --cov=src --cov-report=html backend/src/tests {'' if warn else '--disable-warnings'}")


@app.command()
def filter(test_file: str, warn: bool = False) -> None:
    print(f"[bright_blue u bold] Running {test_file} test(s)!")
    system(f"poetry run pytest {test_file} {'' if warn else '--disable-warnings'}")


app()
