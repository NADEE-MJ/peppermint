from os import system

import typer
from rich import print

app = typer.Typer()


@app.command()
def start(recreate: bool = False, nocache: bool = False) -> None:
    if nocache:
        print("[green]Rebuilding Image without cache...[/green]")
        system("docker compose build --no-cache")
    print("[green]Starting Containers![/green]")
    system(f"docker compose up -d {'--force-recreate' if recreate else ''}")


@app.command()
def stop() -> None:
    print("[red]Stop Containers![/red]")
    system("docker compose down")


@app.command()
def attach() -> None:
    print("[green]Attaching to peppermint app container...[/green]")
    system("docker exec -it -w /home/deploy/peppermint peppermint-app /bin/bash")


app()
