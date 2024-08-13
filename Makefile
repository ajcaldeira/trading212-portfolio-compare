# make help - find available targes in the Makefile
.PHONY: help
help:
	@echo " pre-commit           Run pre-commit hooks"
	@echo " run-tests            Run tests"
	@echo " run-me           	 Run the project"

# make pre-commit - run pre-commit hooks
.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

# make run-tests - run tests
# .PHONY: run-tests
# run-tests:
# 	poetry run pytest

# make run-me - run the project
.PHONY: compare
compare:
	python main.py --ticker $(ticker)
