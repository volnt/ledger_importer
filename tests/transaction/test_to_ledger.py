import datetime
from decimal import Decimal

from ledger_importer.transaction import Transaction


def test_to_ledger(config):
    transaction = Transaction(
        date=datetime.datetime(year=2021, month=1, day=23),
        description="description",
        amount=Decimal("-150"),
        target_account="Expenses",
        account="Assets:Checking",
    )

    assert (
        transaction.to_ledger(config)
        == """2021/01/23    description
    Assets:Checking    -150€
    Expenses
"""
    )
