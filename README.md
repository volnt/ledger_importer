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

## Quickstart

1. Generate a new config file:

```sh
python -m ledger_importer init > my_importer.py
```

2. /Optional/: update the configuration for your needs (see the [Configure section](#Configure))

3. Import your bank statement

```sh
python -m ledger_importer import --statement-path statement.csv --config-path my_importer.py::LedgerImporterConfig
```

Note: the ledger transactions are written to stdout. Redirect stdout to your ledger journal to write them there instead (add ` >> journal.ledger` at the end of the previous command).

## Configure

`ledger_importer` is configured in Python. You can give your configuration to the ledger_importer CLI using a string ressembling [pytest node ids](https://docs.pytest.org/en/latest/how-to/usage.html#nodeids). For example: `ledger_importer import --statement-path statement.csv --config-path ~/ledger/my_config.py::LedgerConfig`.

A Config instance can be created by creating a new class that inherits `ledger_importer.Config`. This new class must implement the following methods:

* `parse_date(self, fields: tuple) -> datetime.datetime`
* `parse_payee(self, fields: tuple) -> str`
* `parse_postings(self, fields: tuple) -> list[Posting]`

The argument `fields: tuple` will be the csv row, with each column as an element of the tuple.

Example configuration file:

```py
#!/usr/bin/env python
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
    csv_delimiter: str = ";"

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
```

## Run

To run leger_importer:

```sh
$ python -m ledger_importer import --statement-path bank-statement.csv --journal-path journal.ledger --config-path my_importer.py::LedgerImporterConfig

|        Account         |    Date    |  Amount  |        Payee        |
| Assets:Account:Florent | 2021/07/29 | 1234.56€ | VIR LOLE FOOB A.R.L |

Which account provided this income? ([Income:Salary]/[q]uit/[s]kip)


|        Account         |    Date    |  Amount |            Payee             |
| Assets:Account:Florent | 2021/08/02 | -11.77€ | CARD  27/07/21 SWILE XX*XXXX |

To which account did this money go? ([Expenses:Restaurant]/[q]uit/[s]kip)


|        Account         |    Date    |   Amount  |                  Payee                  |
| Assets:Account:Florent | 2021/08/03 |  -784.00€ | VIR Save some € Mr.      Florent        |

To which account did this money go? ([Expenses]/[q]uit/[s]kip)
Assets:Savings


|        Account         |    Date    |  Amount |             Payee             |
| Assets:Account:Florent | 2021/08/03 | -58.63€ | CARD  08/03/21 PAYPAL XX*XXXX |

To which account did this money go? ([Expenses:Shopping]/[q]uit/[s]kip)
q
```

## Usage

Root command:

```sh
$ python -m ledger_importer --help
Usage: python -m ledger_importer [OPTIONS] COMMAND [ARGS]...

Options:
  --help                          Show this message and exit.

Commands:
  import  Import a bank statement.
  init    Bootstrap a config file that can later be customized.
```

Import command imports bank statement and generates ledger transactions:

```sh
$ python -m ledger_importer import --help
Usage: python -m ledger_importer import [OPTIONS]

  Import a bank statement.

Options:
  --statement-path PATH  Path to the bank statement to import.  [required]
  --config-path TEXT     Python path to the configuration file.  [required]
  --journal-path PATH    Path a ledger journal to write & learn accounts from.
  --quiet / --no-quiet   Don't ask questions and guess all the accounts
                         automatically.  [default: no-quiet]
  --help                 Show this message and exit.
```

Init command bootstraps a new config file:

```sh
$ python -m ledger_importer init --help
Usage: python -m ledger_importer init [OPTIONS]

  Bootstrap a config file that can later be customized.

Options:
  --help  Show this message and exit.

```
