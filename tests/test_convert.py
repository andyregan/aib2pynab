import csv
import pytest
from click.testing import CliRunner
from aib2ynab import cli


@pytest.mark.datafiles("tests/test_files/transactions.csv")
def test_convert(datafiles):
    runner = CliRunner()
    with runner.isolated_filesystem(datafiles):
        input_file = "../transactions.csv"
        output_file = "converted.csv"
        result = runner.invoke(cli.convert, [input_file, output_file])
        assert result.output == "Successfully converted file.\n"
        assert result.exit_code == 0

        with open(input_file, "r") as input:
            input_reader = csv.DictReader(input, skipinitialspace=True)
            input_rows = list(input_reader)

        with open(output_file, "r") as output:
            output_reader = csv.DictReader(output)
            assert output_reader.fieldnames == [
                "Date",
                "Payee",
                "Memo",
                "Outflow",
                "Inflow",
            ]
            output_rows = list(output_reader)

        for i in range(len(input_rows)):
            assert output_rows[i]["Date"] == input_rows[i]["Posted Transactions Date"]
            assert output_rows[i]["Payee"] == input_rows[i]["Description1"]
            assert output_rows[i]["Memo"] == input_rows[i]["Description2"]
            assert output_rows[i]["Outflow"] == input_rows[i]["Debit Amount"]
            assert output_rows[i]["Inflow"] == input_rows[i]["Credit Amount"]
