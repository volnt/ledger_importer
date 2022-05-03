import datetime
from decimal import Decimal

from ledger_importer.transaction import Transaction


def test_merged_transactions_are_deduplicated(transactions_handler):
    transactions_handler.config.transactions_match = lambda *_: True
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

    merged_transactions = transactions_handler.merge_transactions(transactions)

    assert len(merged_transactions) == 1
    assert merged_transactions[0].target_account == "Assets:Checking"


def test_nothing_is_done_when_transactions_arent_merged(transactions_handler):
    transactions_handler.config.transactions_match = lambda *_: False
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

    merged_transactions = transactions_handler.merge_transactions(transactions)

    assert len(merged_transactions) == 2
    assert merged_transactions[0].target_account == "Expenses"
