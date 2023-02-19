from os import system

import typer
from rich import print

app = typer.Typer()


@app.command()
def all() -> None:
    print("[green]Linting all files![/green]")

    print("[green]Running autoflake...[/green]")
    system(
        (
            "poetry run autoflake --remove-all-unused-imports --recursive"
            " --remove-unused-variables --in-place --exclude=__init__.py backend/src/"
        )
    )

    print("[green]Running isort...[/green]")
    system("poetry run isort backend/src/")

    print("[green]Running black...[/green]")
    system("poetry run black backend/src/")

    print("[green]Running flake8...[/green]")
    system("poetry run flake8 backend/src/")

    print("[green]Running mypy...[/green]")
    system("poetry run mypy backend/src/")


@app.command()
def mypy() -> None:
    print("[green]Running mypy...[/green]")
    system("poetry run mypy backend/src/")


@app.command()
def filter(file: str) -> None:
    # TODO make this not take a relative path

    print(f"[green]Linting file {file}![/green]")

    print("[green]Running autoflake...[/green]")
    system(
        (
            "poetry run autoflake --remove-all-unused-imports --recursive"
            f" --remove-unused-variables --in-place --exclude=__init__.py {file}"
        )
    )

    print("[green]Running isort...[/green]")
    system(f"poetry run isort {file}")

    print("[green]Running black...[/green]")
    system(f"poetry run black {file}")

    print("[green]Running flake8...[/green]")
    system(f"poetry run flake8 {file}")

    print("[green]Running mypy...[/green]")
    system(f"poetry run mypy {file}")


app()
