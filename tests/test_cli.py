from typer.testing import CliRunner
from tests.conftest import app_requests_session
from app.cli.__main__ import cli
import json

runner = CliRunner()

def create_one_customer():
    name= "Jason"
    postal_code = "12345"
    phone="4251234234"

    runner.invoke(cli, ["customer", "new", 
        "--name", name, 
        "--postal-code", postal_code,
        "--phone", phone
        ])

def test_empty_get_customers_list(app_requests_session):
    #Act
    output = runner.invoke(cli, ["customer", "list"])

    #Assert
    assert output.exit_code == 0
    result = json.loads(output.stdout)  
    assert result["status_code"] == 200
    assert result["data"] == []

def test_get_customers_list_with_one_record(app_requests_session):
    #Arrange
    create_one_customer()
    #Act
    output = runner.invoke(cli, ["customer", "list"])

    #Assert
    assert output.exit_code == 0
    result = json.loads(output.stdout)  
    assert result["status_code"] == 200
    assert len(result["data"]) == 1
    customer_data = result["data"][0]
    assert customer_data["id"] == 1
    assert customer_data["name"] == "Jason"
    assert customer_data["postal_code"] == "12345"
    assert customer_data["phone"] == "4251234234"

def test_get_customer_one(app_requests_session):
    #Arrange
    create_one_customer()

    #Act
    output = runner.invoke(cli, ["customer", "get", "1"])

    #Assert
    assert output.exit_code == 0
    result = json.loads(output.stdout)  
    assert result["status_code"] == 200
    customer_data = result["data"]
    assert customer_data["id"] == 1
    assert customer_data["name"] == "Jason"
    assert customer_data["postal_code"] == "12345"
    assert customer_data["phone"] == "4251234234"

def test_customer_new_successful(app_requests_session):
    #Arrange
    name= "Jason"
    postal_code = "12345"
    phone="4251234234" 
    #Act
    output = runner.invoke(cli, ["customer", "new", 
            "--name", name, 
            "--postal-code", postal_code,
            "--phone", phone
            ])
    #Assert
    assert output.exit_code == 0
    result = json.loads(output.stdout)
    assert result["status_code"] == 201
    assert result["data"]["id"] == 1

def test_delete_customer_one_successful(app_requests_session):
    #Arrange
    create_one_customer()

    #Act
    output = runner.invoke(cli, ["customer", "delete", "1"])
    output_test = runner.invoke(cli, ["customer", "list"])

    #Assert
    assert output.exit_code == 0
    result = json.loads(output.stdout)
    assert result["status_code"] == 200
    assert result["data"]["id"] == 1
    assert output_test.exit_code == 0
    result_test = json.loads(output_test.stdout)
    assert len(result_test["data"]) == 0

def test_customer_update_successful(app_requests_session):
    #Arrange
    create_one_customer()
    new_name = "Cathy"
    new_postal_code = "54321"
    new_phone = "4251111111"

    #Act
    output = runner.invoke(cli, ["customer", "update", 
        "--id", "1",
        "--name", new_name, 
        "--postal-code", new_postal_code,
        "--phone", new_phone
        ])
    #Assert
    assert output.exit_code == 0
    result = json.loads(output.stdout)
    assert result["status_code"] == 200
    customer_data = result["data"]
    assert customer_data["name"] == new_name
    assert customer_data["postal_code"] == new_postal_code
    





