from unittest import mock

import pytest

from ledger_importer.transactions_handler import TransactionsHandler


@pytest.fixture
def transactions_handler():
    yield TransactionsHandler(mock.MagicMock())
