DEB_DEPENDENCIES = postgresql python3-dev python3-venv gcc

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

setup: python-deps
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

node_modules:
	yarn install

js-build: node_modules
	yarn build
.PHONY: js-build


db-setup:
	sudo -u postgres createuser $(USER) || true
	sudo -u postgres createdb $(DB_NAME) -O $(USER)
.PHONY: db-setup

clean: python-clean db-clean services-clean
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

jurge-wsgi.service: uwsgi.ini
	pwd=`pwd` envsubst < templates/jurge-wsgi.service.tmpl > jurge-wsgi.service

uwsgi.ini: templates/uwsgi.ini.tmpl
	pwd=`pwd` envsubst < templates/uwsgi.ini.tmpl > uwsgi.ini


jurge.service: nginx.conf templates/jurge.service.tmpl
	pwd=`pwd` envsubst < templates/jurge.service.tmpl > jurge.service

nginx.conf: templates/nginx.conf.tmpl
	pwd=`pwd` port=5000 server_name=jurge log_dir=`pwd` static_dir=`pwd`/build envsubst < templates/nginx.conf.tmpl > nginx.conf

services-create: jurge-wsgi.service jurge.service
.PHONY: services-create

services-clean: stop
	rm -f jurge-wsgi.service
	rm -f jurgeservice
	rm -f nginx.conf
	rm -f uwsgi.ini
.PHONY: services-create

run: services-create
	systemctl --user enable `pwd`/jurge-wsgi.service
	systemctl --user enable `pwd`/jurge.service
	systemctl --user start jurge.service
.PHONY: run

stop:
	systemctl --user stop jurge.service
	systemctl --user stop jurge-wsgi.service
	-systemctl --user disable jurge-wsgi.service
	-systemctl --user disable jurge.service
.PHONY: run

$(VIRTUALENV):
	python3 -m venv $@
