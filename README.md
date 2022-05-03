# ledger_importer [![CircleCI](https://circleci.com/gh/volnt/ledger_importer.svg?style=shield&circle-token=afb73aed03518c8658de39f5d61ec3bfdf50d57c)](https://app.circleci.com/settings/project/github/volnt/ledger_importer)

ledger_importer is a csv-to-[ledger](https://www.ledger-cli.org/3.0/doc/ledger3.html) importer that can be configured in Python.

The key features are:

* **Customization**: Designed to fit your specific needs perfectly.
* **Auto-completion**: The confirmation step is auto-completed.
* **Integration**: Easy to integrate with your pipeline.

ledger_importer main selling point is that if you know Python, you can write complex rules to match & parse accounts / target_accounts. All other tools try to be smart about the target_account matching part but offer very little customization (regex matching is the best I've seen).

Another cool feature is that if you have several bank accounts, you can concatenate their csv exports and ledger_importer will de-duplicate transactions between them. The de-duplication rule can be customized to your needs.

## Installation

```sh
$ pip install ledger-importer
```

## Configure

ledger_importer works by using the configuration file as the entrypoint. The `ledger_importer.runner` function is the function that should be called when you want to run the program.

The `runner` function takes a Config as the first argument.

A Config instance can be created by creating a new class that inherits `ledger_importer.runner`. This new class must implement the following methods:

* `parse_date(self, fields: tuple) -> datetime.datetime`
* `parse_payee(self, fields: tuple) -> str`
* `parse_amount(self, fields: tuple) -> Decimal`
* `format_amount(self, amount: Decimal) -> str`
* `parse_target_account(self, fields: tuple) -> str`
* `parse_account(self, fields: tuple) -> str`

The argument `fields: tuple` will be the csv row, with each column as an element of the tuple.


Example configuration file:

```py
#!/usr/bin/env python
from __future__ import annotations

import datetime
import re
from decimal import Decimal

from ledger_importer import Config, runner, Posting

# Custom ledger importer configuration
class LedgerImporterConfig(Config):
    # Define the number of lines that needs to be skipped at the beginning of the file.
    # This is usefull if the csv has a line with the column names for example.
    skip_lines: int = 1

    # The argument `fields` given in all parse_* methods contains a whole csv row in a tuple
    # Each element of the tuple is a string representation of the column

    def parse_date(self, fields: tuple) -> datetime.datetime:
        return datetime.datetime.strptime(fields[0], "%m-%d-%Y")

    def parse_payee(self, fields: tuple) -> str:
        return fields[2]

    def parse_postings(self, fields: tuple) -> list[Posting]:
        if self.parse_amount(fields) > 0:
            account = "Income"
        else:
            account = "Expenses"

        return [
            Posting(account=account, amount=Amount(quantity=Decimal(re.sub("[€$, ]", "", fields[3])), commodity="€"))
        ]


# The next lines are required to run ledger_importer
# when the config file is executed.
if __name__ == "__main__":
    runner(LedgerImporterConfig())
```

## Run

To run leger_importer, run the configuration module:

```sh
$ python my_importer.py bank-statement.csv --journal-path journal.ledger

|        Account         |    Date    |  Amount  |     Payee     |
| Assets:Account:Florent | 2021/07/29 | 1234.56€ | VIR LOLE FOOB A.R.L |

Which account provided this income? ([Income:Salary]/[q]uit/[s]kip)


|        Account         |    Date    |  Amount |         Payee          |
| Assets:Account:Florent | 2021/08/02 | -11.77€ | CARD  27/07/21 SWILE XX*XXXX |

To which account did this money go? ([Expenses:Restaurant]/[q]uit/[s]kip)


|        Account         |    Date    |   Amount  |               Payee               |
| Assets:Account:Florent | 2021/08/03 |  -784.00€ | VIR Save some € Mr.      Florent        |

To which account did this money go? ([Expenses]/[q]uit/[s]kip)
Assets:Savings


|        Account         |    Date    |  Amount |          Payee          |
| Assets:Account:Florent | 2021/08/03 | -58.63€ | CARD  08/03/21 PAYPAL XX*XXXX |

To which account did this money go? ([Expenses:Shopping]/[q]uit/[s]kip)
q
```

## Usage

A sample configuration can be generated:

```sh
python -m ledger_importer > my_importer.py
```

The configuration can be run directly:

```sh
$ python my_importer.py --help
Usage: my_config.py [OPTIONS] CSV_PATH

  Import a bank statement.

Arguments:
  CSV_PATH  Path to the bank statement to import.  [required]

Options:
  --journal-path PATH             Path a ledger journal to write & learn
                                  accounts from.
  --quiet / --no-quiet            Don't ask questions and guess all the
                                  accounts automatically.  [default: no-quiet]
  --help                          Show this message and exit.
```
