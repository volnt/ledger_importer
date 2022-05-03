import datetime
from decimal import Decimal

from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction


def test_merged_transactions_are_deduplicated(transactions_handler):
    transactions_handler.config.transactions_match = lambda *_: True
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

    merged_transactions = transactions_handler.merge_transactions(transactions)

    assert len(merged_transactions) == 1
    assert merged_transactions[0].postings[1].account == "Assets:Checking"


def test_nothing_is_done_when_transactions_arent_merged(transactions_handler):
    transactions_handler.config.transactions_match = lambda *_: False
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

    merged_transactions = transactions_handler.merge_transactions(transactions)

    assert len(merged_transactions) == 2
    assert merged_transactions[0].postings[1].account == "Expenses"
