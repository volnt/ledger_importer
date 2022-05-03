import datetime
from decimal import Decimal

from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction


def test_transactions_with_opposite_amount_and_different_accounts_match(config):
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            payee="Description",
            postings=[
                Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
                Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
            ],
        ),
        Transaction(
            date=datetime.datetime.now(),
            payee="",
            postings=[
                Posting(account="Assets:Savings", amount=Amount(quantity=Decimal("150"), commodity="€")),
                Posting(account="Income", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            ],
        ),
    ]

    assert config.transactions_match(*transactions) is True


def test_transactions_with_opposite_amount_and_same_account_dont_match(config):
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            payee="Description",
            postings=[
                Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
                Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
            ],
        ),
        Transaction(
            date=datetime.datetime.now(),
            payee="",
            postings=[
                Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("150"), commodity="€")),
                Posting(account="Income", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            ],
        ),
    ]

    assert config.transactions_match(*transactions) is False


def test_transactions_with_different_amount_and_different_account_dont_match(config):
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            payee="Description",
            postings=[
                Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
                Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
            ],
        ),
        Transaction(
            date=datetime.datetime.now(),
            payee="",
            postings=[
                Posting(account="Assets:Savings", amount=Amount(quantity=Decimal("85"), commodity="€")),
                Posting(account="Income", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            ],
        ),
    ]

    assert config.transactions_match(*transactions) is False
