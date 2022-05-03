import datetime
from decimal import Decimal
from unittest import mock

import pytest

from ledger_importer.transaction import Transaction


@pytest.fixture
def mock_stdin():
    with mock.patch("ledger_importer.transactions_handler.sys.stdin") as stdin:
        yield stdin


def test_skip_doesnt_confirm_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "s"  # send "skip" command
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("-150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
    ]

    confirmed_transactions = transactions_handler.confirm_transactions(transactions)

    assert len(confirmed_transactions) == 0


def test_quit_doesnt_confirm_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "q"  # send "quit" command
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("-150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
    ]

    confirmed_transactions = transactions_handler.confirm_transactions(transactions)

    assert len(confirmed_transactions) == 0


def test_empty_string_confirms_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "\n"
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
    ]

    confirmed_transactions = transactions_handler.confirm_transactions(transactions)

    assert len(confirmed_transactions) == 1


def test_string_updates_target_account_and_confirms_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "Expenses:Foobar"
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("-150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
    ]

    confirmed_transactions = transactions_handler.confirm_transactions(transactions)

    assert len(confirmed_transactions) == 1
    assert confirmed_transactions[0].target_account == "Expenses:Foobar"
