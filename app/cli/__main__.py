from json import dumps
import typer
from typing import Optional
import requests

SERVICE_URI = "http://127.0.0.1:5000"
requests_session = requests.Session()

cli = typer.Typer()

customer_cli = typer.Typer()
video_cli = typer.Typer()
rental_cli = typer.Typer()

cli.add_typer(customer_cli, name="customer")
cli.add_typer(video_cli, name="video")
cli.add_typer(rental_cli, name="rental")

@customer_cli.command()
def list(sort:str=typer.Option("id", help="The order"),
        page_num:str=typer.Option("", help="Which page will be displae"),
        count:str=typer.Option("", help="Each page will display")
    ):
    response = requests_session.get(f"{SERVICE_URI}/customers")
    result = {"status_code": response.status_code, "data": response.json()}
    print(dumps(result))

@customer_cli.command()
def get(id: int):
    response = requests_session.get(f"{SERVICE_URI}/customers/{id}")
    result = {"status_code": response.status_code, "data": response.json()}
    print(dumps(result))

@customer_cli.command()
def new(
    name: str = typer.Option(..., help="Full name of the customer"),
    postal_code: str = typer.Option(..., help="Customer's postal code"),
    phone: str = typer.Option(..., help="Customer's phone number"),
):
    response = requests_session.post(f"{SERVICE_URI}/customers", json={
        "name": name,
        "postal_code": postal_code,
        "phone": phone,
    })
    result = {"status_code": response.status_code, "data": response.json()}
    print(dumps(result))




if __name__ == "__main__":
    cli()
