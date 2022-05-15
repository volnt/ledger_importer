from ledger_importer.__main__ import parse_accounts


def test_parse_accounts():
    accounts = parse_accounts(
        """
account Expenses:Groceries  ; comment
account Foo

commodity €
"""
    )

    assert accounts == ["Expenses:Groceries", "Foo"]
