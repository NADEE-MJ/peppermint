from os import system

import typer
from rich import print

app = typer.Typer()


@app.command()
def all() -> None:
    print("[bold u bright_blue]Linting all backend files!")

    print("[bright_green]Running autoflake...")
    system(
        (
            "poetry run autoflake --remove-all-unused-imports --recursive"
            " --remove-unused-variables --in-place --exclude=__init__.py backend/src/"
        )
    )

    print("[bright_green]Running isort...")
    system("poetry run isort backend/src/")

    print("[bright_green]Running black...")
    system("poetry run black backend/src/")

    print("[bright_green]Running flake8...")
    system("poetry run flake8 backend/src/")

    print("[bright_green]Running mypy...")
    system("poetry run mypy backend/src/")


@app.command()
def mypy() -> None:
    print("[bright_green]Running mypy...")
    system("poetry run mypy backend/src/")


@app.command()
def frontend() -> None:
    print("[bold u bright_blue]Linting all frontend files!")
    print("[bright_green]Running prettier write...")
    system("npm run format")
    print("[bright_green]Running prettier check and eslint...")
    system("npm run lint")
    print("[bright_green]Running svelte-kit sync and svelte-check...")
    system("npm run check")


@app.command()
def filter(file: str) -> None:
    # TODO make this not take a relative path

    print(f"[bold u bright_blue]Linting file {file}!")

    print("[green]Running autoflake...")
    system(
        (
            "poetry run autoflake --remove-all-unused-imports --recursive"
            f" --remove-unused-variables --in-place --exclude=__init__.py {file}"
        )
    )

    print("[green]Running isort...")
    system(f"poetry run isort {file}")

    print("[green]Running black...")
    system(f"poetry run black {file}")

    print("[green]Running flake8...")
    system(f"poetry run flake8 {file}")

    print("[green]Running mypy...")
    system(f"poetry run mypy {file}")


app()
