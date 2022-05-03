import datetime
from decimal import Decimal
from unittest import mock

import pytest

from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction


@pytest.fixture
def mock_stdin():
    with mock.patch("ledger_importer.transactions_handler.sys.stdin") as stdin:
        yield stdin


def test_skip_doesnt_confirm_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "s"  # send "skip" command
    transaction = Transaction(
        date=datetime.datetime(year=2021, month=1, day=23),
        payee="Description",
        postings=[
            Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
        ],
    )

    confirmed_transactions = transactions_handler.confirm_transactions([transaction])

    assert len(confirmed_transactions) == 0


def test_quit_doesnt_confirm_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "q"  # send "quit" command
    transaction = Transaction(
        date=datetime.datetime(year=2021, month=1, day=23),
        payee="Description",
        postings=[
            Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
        ],
    )

    confirmed_transactions = transactions_handler.confirm_transactions([transaction])

    assert len(confirmed_transactions) == 0


def test_empty_string_confirms_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "\n"
    transaction = Transaction(
        date=datetime.datetime(year=2021, month=1, day=23),
        payee="Description",
        postings=[
            Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("150"), commodity="€")),
            Posting(account="Income", amount=Amount(quantity=Decimal("-150"), commodity="€")),
        ],
    )

    confirmed_transactions = transactions_handler.confirm_transactions([transaction])

    assert len(confirmed_transactions) == 1


def test_string_updates_target_account_and_confirms_transaction(transactions_handler, mock_stdin):
    mock_stdin.readline.return_value = "Expenses:Foobar"
    transaction = Transaction(
        date=datetime.datetime(year=2021, month=1, day=23),
        payee="Description",
        postings=[
            Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
        ],
    )

    confirmed_transactions = transactions_handler.confirm_transactions([transaction])

    assert len(confirmed_transactions) == 1
    assert confirmed_transactions[0].postings[1].account == "Expenses:Foobar"
