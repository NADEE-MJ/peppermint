from os import system
from shutil import which

import typer
from rich import print

app = typer.Typer()

PATH: str = "backend/"


@app.command()
def start() -> None:
    if not which("screen"):
        print("[red]\nPlease install screen!\n\n")
        print("Run the following: [red u]sudo apt install screen -y\n")
        return None
    print("[green]FastAPI Server Start!")
    system(f"cd {PATH} && screen -S fastapi-server -dm poetry run uvicorn --host 0.0.0.0 src.main:app --reload")

    print("[green]SvelteKit Server Start!")
    system(f"cd {PATH} && screen -S sveltekit-server -dm npm run dev")


@app.command()
def stop() -> None:
    if not which("screen"):
        print("[red u]\nPlease install screen!\n\n")
        print("Run the following: [red]sudo apt install screen -y\n")
        return None
    system("screen -S fastapi-server -X quit")
    print("[red]FastAPI Server Stop!")

    system("screen -S sveltekit-server -X quit")
    print("[red]SvelteKit Server Stop!")


@app.command()
def attach(screen: str) -> None:
    if screen == "back":
        print("[bright_blue bold]Attaching to FastAPI Screen...")
        system(f"screen -r fastapi-server")
    elif screen == "front":
        print("[bright_blue bold]Attaching to SvelteKit Screen...")
        system(f"screen -r sveltekit-server")


@app.command()
def fast() -> None:
    print("[bright_blue bold]FastAPI Server Start!")
    system(f"cd {PATH} && poetry run uvicorn --host 0.0.0.0 src.main:app --reload")


@app.command()
def kit() -> None:
    print("[bright_blue bold]SvelteKit Server Start!")
    system(f"npm run dev")


app()
