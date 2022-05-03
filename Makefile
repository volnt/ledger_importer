.DEFAULT_GOAL := help

.PHONY: test
test:  ## Launch tests
	poetry run pytest --cov=ledger_importer --cov-report=xml:/tmp/test-reports/coverage.xml --junitxml=/tmp/test-reports/junit.xml -vv -s tests
	poetry run coverage html
	poetry run coverage report

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
