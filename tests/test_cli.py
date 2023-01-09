from typer.testing import CliRunner
from app.cli import cli

runner = CliRunner()

def test_get_customers_list():
    #Act
    result = runner.invoke(cli, ["list"])

    assert result.exit_code == 0
