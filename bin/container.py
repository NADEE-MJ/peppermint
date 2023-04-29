from os import system

import typer
from rich import print

app = typer.Typer()


@app.command()
def start(recreate: bool = False, nocache: bool = False) -> None:
    if nocache:
        print("[bold u red]Rebuilding Image without cache...")
        system("docker compose build --no-cache")
    print("[bold green]Starting Containers!")
    system(f"docker compose up -d {'--force-recreate' if recreate else ''}")


@app.command()
def stop() -> None:
    print("[bold red]Stop Containers!")
    system("docker compose down")


@app.command()
def attach() -> None:
    print("[bold green]Attaching to peppermint app container...")
    system("docker exec -it -w /home/deploy/peppermint peppermint-app /bin/bash")


app()
