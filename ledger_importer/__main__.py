from __future__ import annotations

import csv
import importlib
import os
import pathlib
import re
import readline
import sys
from typing import Optional

import typer

from ledger_importer import __version__
from ledger_importer.transactions_handler import TransactionsHandler

app = typer.Typer()

SAMPLE_CONFIG = """#!/usr/bin/env python
from __future__ import annotations

import datetime
import re
from decimal import Decimal

from ledger_importer import Config, Posting, Amount

# Custom ledger importer configuration
class LedgerImporterConfig(Config):
    # Define the number of lines that needs to be skipped at the beginning of the file.
    # This is usefull if the csv has a line with the column names for example.
    skip_lines: int = 1

    # Define the csv delimiter
    csv_delimiter: str = ","

    # The argument `fields` given in all parse_* methods contains a whole csv row in a tuple
    # Each element of the tuple is a string representation of the column

    def parse_date(self, fields: tuple) -> datetime.datetime:
        return datetime.datetime.strptime(fields[0], "%m-%d-%Y")

    def parse_payee(self, fields: tuple) -> str:
        return fields[2]

    def parse_postings(self, fields: tuple) -> list[Posting]:
        amount = Amount(quantity=Decimal(re.sub("[€ ]", "", fields[3]).replace(",", ".")), commodity="€")
        if amount > 0:
            account = "Income"
        else:
            account = "Expenses"

        posting = Posting(account="Assets:Checking", amount=amount)

        # A Transaction should be at least 2 postings that have reversed amounts
        return [posting, Posting(account=account, amount=amount.reverse())]
"""


@app.command("init")
def init():
    """
    Bootstrap a config file that can later be customized.
    """
    print(SAMPLE_CONFIG)


ACCOUNT_LINE = r"^account ([A-z_ :]*[A-z])( +;?.*)?"


def parse_accounts(data: str) -> list[str]:
    accounts: list[str] = []

    for line in data.split("\n"):
        m = re.match(ACCOUNT_LINE, line)
        if not m:
            continue
        accounts.append(m.groups()[0])

    return accounts


class AccountCompleter:
    def __init__(self, accounts: list[str]) -> None:
        self.accounts = accounts

    def complete(self, text: str, state: int) -> str | None:
        # on first trigger, build possible matches
        if state == 0:
            if not text:
                self.matches = self.accounts[:]
            else:
                self.matches = [s for s in self.accounts if s and s.startswith(text)]

        try:
            return self.matches[state]
        except IndexError:
            pass

        return None


@app.command("import")
def import_(
    statement_path: pathlib.Path = typer.Option(..., help="Path to the bank statement to import."),
    config_path: str = typer.Option(..., help="Python path to the configuration file."),
    journal_path: Optional[pathlib.Path] = typer.Option(
        None, help="Path a ledger journal to write & learn accounts from."
    ),
    quiet: bool = typer.Option(False, help="Don't ask questions and guess all the accounts automatically."),
):
    """
    Import a bank statement.
    """
    # Load config from python path
    config_path_without_class = config_path.split("::")[:-1][0]
    module_path = "/".join(config_path_without_class.split("/")[:-1])
    module = config_path_without_class.split("/")[-1].split(".py")[0]
    klass = config_path.split("::")[-1]
    sys.path.append(os.path.abspath(module_path or "."))
    config = getattr(importlib.import_module(module), klass)()

    # Get accounts list
    accounts: list[str] = []
    if journal_path:
        with journal_path.open() as journal_file:
            accounts = parse_accounts(journal_file.read())

    # Setup account completion
    completer = AccountCompleter(accounts)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" \t\n;")

    # Parse transactions, merge them and confirm them
    handler = TransactionsHandler(config)

    with statement_path.open() as csv_file:
        transactions = handler.merge_transactions(
            handler.parse_transactions(
                csv.reader(csv_file, delimiter=config.csv_delimiter),
            ),
        )
        if not quiet:
            transactions = handler.confirm_transactions(transactions)

    for transaction in transactions:
        print(transaction.to_ledger())


def version_callback():
    typer.echo(f"ledger_importer: version {__version__}")
    raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(None, callback=version_callback),
):
    pass


if __name__ == "__main__":
    app()
