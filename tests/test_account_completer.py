from ledger_importer import AccountCompleter


def test_complete():
    completer = AccountCompleter(["Expenses:Groceries", "Expenses:Restaurant"])

    assert completer.complete("", 0) == "Expenses:Groceries"
    assert completer.complete("Ex", 0) == "Expenses:Groceries"
    assert completer.complete("Ex", 1) == "Expenses:Restaurant"
    assert completer.complete("Foo", 0) is None
