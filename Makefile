.DEFAULT_GOAL := help

PYTHON := poetry run python

.PHONY: test
test:  ## Launch tests
	${PYTHON} -m coverage run --source ledger_importer -m pytest -vv -s
	${PYTHON} -m coverage report
	${PYTHON} -m coverage html

.PHONY: style
style: ## Check code linting and style
	poetry run pre-commit run -a

# Implements this pattern for autodocumenting Makefiles:
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
#
# Picks up all comments that start with a ## and are at the end of a target definition line.
.PHONY: help
help:  ## Display command usage
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
