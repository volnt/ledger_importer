import datetime
from decimal import Decimal


def test_parses_transactions(transactions_handler):
    transactions_handler.config.skip_lines = 0
    transactions_handler.config.parse_date = lambda fields: datetime.datetime.strptime(fields[0], "%m-%d-%Y")
    transactions_handler.config.parse_description = lambda fields: fields[1]
    transactions_handler.config.parse_amount = lambda fields: Decimal(fields[2])
    transactions_handler.config.parse_payee = lambda _: "Expenses"
    transactions_handler.config.parse_account = lambda _: "Assets:Checking"

    transactions = transactions_handler.parse_transactions((el for el in [("05-23-2021", "description", "-100.42")]))

    assert len(transactions) == 1
    assert transactions[0].date == datetime.datetime(year=2021, day=23, month=5)
    assert transactions[0].description == "description"
    assert transactions[0].amount == Decimal("-100.42")
    assert transactions[0].payee == "Expenses"
    assert transactions[0].account == "Assets:Checking"


def test_skip_lines(transactions_handler):
    transactions_handler.config.skip_lines = 1

    transactions = transactions_handler.parse_transactions((el for el in [("date", "description", "amount")]))

    assert len(transactions) == 0
