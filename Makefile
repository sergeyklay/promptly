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

.env: .env.example
	cp $< $@

requirements/%.txt: requirements/%.in $(VENV_BIN)
	$(VENV_BIN)/pip-compile --allow-unsafe --generate-hashes --output-file=$@ $<

$(VENV_PYTHON): $(VENV_ROOT)
	@echo

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
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

## Public targets

.PHONY: init
init: $(VENV_PYTHON)
	@echo $(CS)Set up virtualenv$(CE)
	$(VENV_PIP) install --progress-bar=off --upgrade pip pip-tools
	@echo

.PHONY: install
install: $(REQUIREMENTS)
	@echo $(CS)Installing $(PKG_NAME) and all its dependencies$(CE)
	$(VENV_BIN)/pip-sync $^
	$(VENV_PIP) install --progress-bar=off -e .
	@echo

.PHONY: uninstall
uninstall:
	@echo $(CS)Uninstalling $(PKG_NAME)$(CE)
	- $(VENV_PIP) uninstall --yes $(PKG_NAME) &2>/dev/null

	@echo Verifying...
	cd .. && ! $(VENV_PYTHON) -m $(PKG_NAME) --version &2>/dev/null

	@echo Done.
	@echo

.PHONY: serve
serve: $(VENV_PYTHON) .env runner.py
	@echo $(CS)Run builtin server$(CE)
	$(VENV_BIN)/flask --app runner:app run --debug
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)
	$(call rm-venv-link)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./.cache ./.pytest_cache
	$(RM) -r ./htmlcov
	$(RM) ./coverage.*
	@echo

.PHONY: maintainer-clean
maintainer-clean: clean
	@echo $(CS)Performing full clean$(CE)
	-$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	$(RM) requirements/*.txt
	$(RM) *.env *.sqlite3
	@echo

.PHONY: help
help:
	@echo 'Promptly'
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:         Show this help and exit'
	@echo '  init:         Set up virtualenv (has to be launched first)'
	@echo '  install:      Install project and all its dependencies'
	@echo '  uninstall:    Uninstall local version of the project'
	@echo '  serve:        Run builtin server'
	@echo '  clean:        Remove build and tests artefacts and directories'
	@echo '  maintainer-clean:'
	@echo '                Delete almost everything that can be reconstructed'
	@echo '                with this Makefile'
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
	@echo