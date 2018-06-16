DEB_DEPENDENCIES = postgresql python3-venv

VIRTUALENV = .ve
VE_BIN = $(VIRTUALENV)/bin
PYTHON = $(VE_BIN)/python3

DB_NAME = jurge
DATABASE_URL=postgresql:///$(DB_NAME)

REQUIREMENTS_TXT = "requirements.txt"
TEST_REQUIREMENTS_TXT = "requirements-dev.txt"
REQUIREMENTS_EXCLUDE = "jurge==|jurge\.git|pkg-resources"

.DEFAULT_GOAL := setup

deps: deb-deps python-deps
.PHONY: deps

deb-deps:
	sudo apt update
	sudo apt install --yes $(DEB_DEPENDENCIES)
.PHONY: deb-deps

python-deps: $(VIRTUALENV)
	$(VE_BIN)/pip install -r requirements.txt -r requirements-dev.txt
.PHONY: python-deps

setup: python-deps db-setup
	$(PYTHON) setup.py develop
.PHONY: setup

.PHONY: rebuild-requirements.txt
rebuild-requirements.txt: TMP_DIR := $(shell mktemp -u)
rebuild-requirements.txt: ## Rebuild the requirements.txt files with the latest dependencies.
	python3 -m venv $(TMP_DIR)
	$(TMP_DIR)/bin/python3 setup.py develop
	$(TMP_DIR)/bin/pip freeze | grep -Ev $(REQUIREMENTS_EXCLUDE) > $(REQUIREMENTS_TXT)
	$(TMP_DIR)/bin/pip install jurge[test]
	$(TMP_DIR)/bin/pip freeze | grep -Ev $(REQUIREMENTS_EXCLUDE) > temp-requirements.txt
	grep -Fv -f $(REQUIREMENTS_TXT) temp-requirements.txt > $(TEST_REQUIREMENTS_TXT)
	rm -rf $(TMP_DIR) temp-requirements.txt

db-setup:
	sudo -u postgres createuser $(USER) || true
	sudo -u postgres createdb $(DB_NAME) -O $(USER)
.PHONY: db-setup

clean: python-clean db-clean
.PHONY: clean

python-clean:
	rm -rf $(VIRTUALENV)
.PHONY: clean-python

db-clean:
	sudo -u postgres dropdb $(DB_NAME) || true
.PHONY: db-clean

db-revision:
	DATABASE_URL=$(DATABASE_URL) $(VE_BIN)/alembic revision --autogenerate
.PHONY: db-revision

migrate:
	DATABASE_URL=$(DATABASE_URL) $(VE_BIN)/alembic upgrade head
.PHONY: migrate

db-recreate: db-clean db-setup migrate
.PHONY: db-recreate

run:
	$(VE_BIN)/jurge
.PHONY: run

$(VIRTUALENV):
	python3 -m venv $@
