import datetime
from decimal import Decimal
from unittest import mock

import pytest

from ledger_importer.config import Config
from ledger_importer.transactions_handler import TransactionsHandler


class MyConfig(Config):
    def parse_date(self, fields):
        return datetime.datetime.strptime(fields[0], "%m-%d-%Y")

    def parse_description(self, fields):
        return fields[1]

    def parse_amount(self, fields):
        return Decimal(fields[2])

    def parse_payee(self, _):
        return "Expenses"

    def parse_account(self, _):
        return "Assets:Checking"

    def format_amount(self, amount):
        return f"{amount}€"


@pytest.fixture
def config():
    yield MyConfig()


@pytest.fixture
def transactions_handler():
    yield TransactionsHandler(mock.MagicMock())
