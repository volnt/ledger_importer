import datetime
from decimal import Decimal

from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting


def test_parses_transactions(transactions_handler):
    transactions_handler.config.skip_lines = 0
    transactions_handler.config.parse_date = lambda fields: datetime.datetime.strptime(fields[0], "%m-%d-%Y")
    transactions_handler.config.parse_payee = lambda fields: fields[1]
    transactions_handler.config.parse_postings = lambda fields: [
        Posting(account="Assets:Checking", amount=Amount(quantity=Decimal(fields[2]), commodity="€")),
        Posting(account="Expenses", amount=Amount(quantity=-Decimal(fields[2]), commodity="€")),
    ]

    transactions = transactions_handler.parse_transactions((el for el in [("05-23-2021", "payee", "-100.42")]))

    assert len(transactions) == 1
    assert transactions[0].date == datetime.datetime(year=2021, day=23, month=5)
    assert transactions[0].payee == "payee"
    assert transactions[0].postings[0].account == "Assets:Checking"
    assert transactions[0].postings[0].amount.quantity == Decimal("-100.42")
    assert transactions[0].postings[0].amount.commodity == "€"
    assert transactions[0].postings[1].account == "Expenses"
    assert transactions[0].postings[1].amount.quantity == Decimal("100.42")
    assert transactions[0].postings[1].amount.commodity == "€"


def test_skip_lines(transactions_handler):
    transactions_handler.config.skip_lines = 1

    transactions = transactions_handler.parse_transactions((el for el in [("date", "payee", "amount")]))

    assert len(transactions) == 0
