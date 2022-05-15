.DEFAULT_GOAL := help

PACKAGE_VERSION := grep "version =" pyproject.toml | sed -E 's/^version = "(.*)"/\1/g'

.PHONY: test
test:  ## Launch tests
	poetry run pytest --cov=ledger_importer --cov-report=xml:/tmp/test-reports/coverage.xml --junitxml=/tmp/test-reports/junit.xml -vv -s tests
	poetry run coverage html
	poetry run coverage report

.PHONY: style
style: ## Check code linting and style
	poetry run pre-commit run -a

ledger_importer/__init__.py: pyproject.toml
	@printf "Generate $@ ......... "
	@sed -E 's/__version__ = "(.*)"/__version__ = "$(shell ${PACKAGE_VERSION})"/' $@ -i
	@printf "✓\n"

.PHONY: version-patch
version-patch: poetry-version-patch ledger_importer/__init__.py ## Create a new patch version

.PHONY: version-minor
version-minor: poetry-version-minor ledger_importer/__init__.py  ## Create a new minor version

.PHONY: version-major
version-major: poetry-version-major ledger_importer/__init__.py  ## Create a new major version

.PHONY: poetry-version-patch
poetry-version-patch:
	@poetry version patch

.PHONY: poetry-version-minor
poetry-version-minor:
	@poetry version minor

.PHONY: poetry-version-major
poetry-version-major:
	@poetry version major

# Implements this pattern for autodocumenting Makefiles:
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
#
# Picks up all comments that start with a ## and are at the end of a target definition line.
.PHONY: help
help:  ## Display command usage
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
