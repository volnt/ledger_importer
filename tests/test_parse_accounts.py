from ledger_importer import parse_accounts


def test_parse_accounts():
    accounts = parse_accounts(
        """
account Expenses:Groceries  ; comment
account Foo

commodity €
"""
    )

    assert accounts == ["Expenses:Groceries", "Foo"]
