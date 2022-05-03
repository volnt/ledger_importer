import datetime
from decimal import Decimal

from ledger_importer.transaction import Transaction


def test_transactions_with_opposite_amount_and_different_accounts_match(config):
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("-150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("150"),
            target_account="Income",
            account="Assets:Savings",
        ),
    ]

    assert config.transactions_match(*transactions) is True


def test_transactions_with_opposite_amount_and_same_account_dont_match(config):
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("-150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("150"),
            target_account="Income",
            account="Assets:Checking",
        ),
    ]

    assert config.transactions_match(*transactions) is False


def test_transactions_with_different_amount_and_different_account_dont_match(config):
    transactions = [
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("-150"),
            target_account="Expenses",
            account="Assets:Checking",
        ),
        Transaction(
            date=datetime.datetime.now(),
            description="",
            amount=Decimal("86"),
            target_account="Income",
            account="Assets:Savings",
        ),
    ]

    assert config.transactions_match(*transactions) is False
