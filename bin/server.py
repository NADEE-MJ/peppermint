from os import system
from shutil import which

import typer
from rich import print

app = typer.Typer()

PATH: str = "backend/"


@app.command()
def start() -> None:
    if not which("screen"):
        print("[red]\nPlease install screen![/red]\n\n")
        print("Run the following: [red]sudo apt install screen -y\n[/red]")
        return None
    print("[green]FastAPI Server Start![/green]")
    system(f"cd {PATH} && screen -S fastapi-server -dm poetry run uvicorn src.main:app --reload")

    print("[green]SvelteKit Server Start![/green]")
    system(f"cd {PATH} && screen -S sveltekit-server -dm npm run dev")


@app.command()
def stop() -> None:
    if not which("screen"):
        print("[red]\nPlease install screen![/red]\n\n")
        print("Run the following: [red]sudo apt install screen -y\n[/red]")
        return None
    system("screen -S fastapi-server -X quit")
    print("[red]FastAPI Server Stop![/red]")

    system("screen -S sveltekit-server -X quit")
    print("[red]SvelteKit Server Stop![/red]")

@app.command()
def attach(screen: str) -> None:
    if screen == 'back':
        print("[green]Attaching to FastAPI Screen...[/green]")
        system(f"screen -r fastapi-server")
    elif screen == 'front':
        print("[green]Attaching to SvelteKit Screen...[/green]")
        system(f"screen -r sveltekit-server")

@app.command()
def fast() -> None:
    print("[green]FastAPI Server Start![/green]")
    system(f"cd {PATH} && poetry run uvicorn src.main:app --reload")

@app.command()
def kit() -> None:
    print("[green]SvelteKit Server Start![/green]")
    system(f"npm run dev")


app()
