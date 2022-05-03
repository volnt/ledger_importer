import datetime
from decimal import Decimal

from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction


def test_to_ledger(config):
    transaction = Transaction(
        date=datetime.datetime(year=2021, month=1, day=23),
        payee="Description",
        postings=[
            Posting(account="Assets:Checking", amount=Amount(quantity=Decimal("-150"), commodity="€")),
            Posting(account="Expenses", amount=Amount(quantity=Decimal("150"), commodity="€")),
        ],
    )

    assert (
        transaction.to_ledger()
        == """2021/01/23    Description
    Assets:Checking    -150 €
    Expenses    150 €
"""
    )
