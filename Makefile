# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

include default.mk

define mk-venv-link
	@if [ -n "$(WORKON_HOME)" ] ; then \
		echo $(ROOT_DIR) > $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/$(PKG_NAME) -a ! -L $(WORKON_HOME)/$(PKG_NAME) ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/$(PKG_NAME); \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use \"workon $(PKG_NAME)\" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/$(PKG_NAME)" -a -f "$(WORKON_HOME)/$(PKG_NAME)" ]; \
		then \
			$(RM) $(WORKON_HOME)/$(PKG_NAME); \
		fi; \
	fi
endef

define section
	@echo $(CS)">>> "$(1)$(CE)
	@echo $(CS)"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"$(CE)
endef

define end_section
	@echo $(CS)"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"$(CE)
	@echo
endef

$(INSTANCE_DIR):
	@mkdir $@

.env: .env.example
	cp $< $@

requirements/%.txt: requirements/%.in $(VENV_BIN)
	$(VENV_BIN)/pip-compile --allow-unsafe --generate-hashes --output-file=$@ $<

.PHONY: docs/_static/security.txt
docs/_static/security.txt: docs/security.in
	@gpg --clearsign --armor --digest-algo SHA512 docs/security.in
	@mv docs/security.in.asc docs/_static/security.txt

$(VENV_PYTHON): $(VENV_ROOT)
	@echo

$(VENV_ROOT):
	$(call section, "Creating a Python environment $(VENV_ROOT)")
	$(VIRTUALENV) --prompt $(PKG_NAME) $(VENV_ROOT)
	@echo
	@echo Done.
	@echo
	@echo To active it manually, run:
	@echo
	@echo "    source $(VENV_BIN)/activate"
	@echo
	@echo See https://docs.python.org/3/library/venv.html for more.
	@echo
	$(call mk-venv-link)
	$(call end_section)

## Public targets

.PHONY: init
init: $(VENV_PYTHON)
	$(call section, "Set up virtualenv")
	$(VENV_PIP) install --progress-bar=off --upgrade pip pip-tools
	$(call end_section)

.PHONY: install
install: $(REQUIREMENTS)
	$(call section, "Installing $(PKG_NAME) and all its dependencies")
	$(VENV_BIN)/pip-sync $^
	$(VENV_PIP) install --progress-bar=off -e .
	$(call section, "Clean install Node.js dependencies")
	npm ci
	$(call end_section)

.PHONY: uninstall
uninstall:
	$(call section, "Uninstalling $(PKG_NAME)")
	- $(VENV_PIP) uninstall --yes $(PKG_NAME) &2>/dev/null

	@echo Verifying...
	cd .. && ! $(VENV_PYTHON) -m $(PKG_NAME) --version &2>/dev/null

	@echo Done.
	$(call end_section)

.PHONY: serve
serve: $(VENV_PYTHON) $(INSTANCE_DIR) .env runner.py
	$(call section, "Run builtin server")
	$(VENV_BIN)/flask --app runner:app run --debug
	$(call end_section)

.PHONY: revision
revision: $(VENV_PYTHON)
	$(call section, "Run database migrations")
	$(VENV_BIN)/flask --app runner:app db revision --autogenerate
	$(call end_section)

.PHONY: migrate
migrate: $(VENV_PYTHON)
	$(call section, "Run database migrations")
	$(VENV_BIN)/flask --app runner:app db upgrade
	$(call end_section)

.PHONY: shell
shell: $(INSTANCE_DIR)
	$(call section, "Starting a shell")
	$(VENV_BIN)/flask --app runner:app shell
	$(call end_section)

.PHONY: seed
seed: $(VENV_PYTHON)
	$(call section, "Add seed data to the database")
	$(VENV_BIN)/flask --app runner:app seed
	$(call end_section)

.PHONY: lint
lint: $(VENV_PYTHON)
	$(call section, "Running linters")
	-$(VENV_BIN)/flake8 $(FLAKE8_FLAGS) ./
	$(VENV_BIN)/pylint $(PYLINT_FLAGS) ./$(PKG_NAME)
	$(call end_section)

.PHONY: test
test: $(VENV_PYTHON)
	$(call section, "Running tests")
	$(VENV_BIN)/coverage erase
	$(VENV_BIN)/coverage run -m pytest $(PYTEST_FLAGS) ./$(PKG_NAME) ./tests
	$(call end_section)

.PHONY: ccov
ccov: $(VENV_PYTHON)
	$(call section, "Combine coverage reports")
	$(VENV_BIN)/coverage combine
	$(VENV_BIN)/coverage report
	$(VENV_BIN)/coverage html
	$(VENV_BIN)/coverage xml
	$(call end_section)

.PHONY: test-all
test-all: uninstall clean install test lint

.PHONY: clean
clean:
	$(call section, "Remove build and tests artefacts and directories")
	$(call rm-venv-link)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./.cache ./.pytest_cache
	$(RM) -r ./htmlcov
	$(RM) ./coverage.*
	$(MAKE) -C docs clean
	$(call end_section)

.PHONY: db-clean
db-clean:
	$(call section, "Cleanup database")
	@echo "DELETE FROM chats;" | sqlite3 dev-db.sqlite3
	$(call end_section)

.PHONY: maintainer-clean
maintainer-clean: clean
	$(call section, "Performing full clean")
	-$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	$(RM) *.env *.sqlite3
	$(RM) -r $(INSTANCE_DIR)
	$(call end_section)

.PHONY: help
help:
	@echo 'Promptly'
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:             Show this help and exit'
	@echo '  init:             Set up virtualenv (has to be launched first)'
	@echo '  install:          Install project and all its dependencies'
	@echo '  uninstall:        Uninstall local version of the project'
	@echo '  serve:            Run builtin server'
	@echo '  revision:         Autogenerate new migration revisions'
	@echo '  migrate:          Run database migrations'
	@echo '  shell:            Run a shell in the app context'
	@echo '  seed:             Add seed data to the database'
	@echo '  lint:             Lint the code'
	@echo '  test:             Run unit tests with coverage'
	@echo '  ccov:             Combine coverage reports'
	@echo '  test-all:         Test everything'
	@echo '  clean:            Remove build and tests artefacts and directories'
	@echo '  db-clean:         Cleanup database'
	@echo '  maintainer-clean: Delete nearly all reconstructable items with'
	@echo '                    this Makefile'
	@echo
	@echo 'Virtualenv:'
	@echo
	@echo '  Python:       $(VENV_PYTHON)'
	@echo '  pip:          $(VENV_PIP)'
	@echo
	@echo 'Flags:'
	@echo
	@echo '  FLAKE8_FLAGS: $(FLAKE8_FLAGS)'
	@echo '  PYTEST_FLAGS: $(PYTEST_FLAGS)'
	@echo '  PYLINT_FLAGS: $(PYLINT_FLAGS)'
	@echo
	@echo 'Environment variables:'
	@echo
	@echo '  PYTHON:       $(PYTHON)'
	@echo '  WORKON_HOME:  ${WORKON_HOME}'
	@echo '  VIRTUAL_ENV:  ${VIRTUAL_ENV}'
	@echo '  SHELL:        $(shell echo $$SHELL)'
	@echo '  TERM:         $(shell echo $$TERM)'
