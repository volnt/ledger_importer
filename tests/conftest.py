import datetime
from decimal import Decimal
from unittest import mock

import pytest

from ledger_importer.config import Config
from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transactions_handler import TransactionsHandler


class MyConfig(Config):
    def parse_date(self, fields):
        return datetime.datetime.strptime(fields[0], "%m-%d-%Y")

    def parse_payee(self, fields):
        return fields[1]

    def parse_postings(self, fields):
        return [
            Posting(account="Assets:Checking", amount=Amount(quantity=Decimal(fields[2]), commodity="€")),
            Posting(account="Expenses", amount=Amount(quantity=-Decimal(fields[2]), commodity="€")),
        ]


@pytest.fixture
def config():
    yield MyConfig()


@pytest.fixture
def transactions_handler():
    yield TransactionsHandler(mock.MagicMock())
