# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

# Run “make help” by default
.DEFAULT_GOAL = help

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PKG_NAME = promptly

INSTANCE_DIR = ./instance
BUILD_DOC_DIR = ./docs/_build
DOCTREES = $(BUILD_DOC_DIR)/doctrees

PYLINT_FLAGS ?=
FLAKE8_FLAGS ?= --show-source --statistics

ifneq ($(TERM),)
	GREEN := $(shell tput setaf 2)
	RESET := $(shell tput sgr0)
	CS = "${GREEN}"
	CE = "${RESET}"

	PYTEST_FLAGS ?= --color=yes
else
	CS = ""
	CE = ""

	PYTEST_FLAGS ?= --color=no
endif

COV          =
REQUIREMENTS = requirements/requirements.txt requirements/requirements-dev.txt

ifneq ($(VIRTUAL_ENV),)
	VENV_ROOT = $(VIRTUAL_ENV)
else
	VENV_ROOT = .venv
endif

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
	PYTHON  ?= python.exe
	VIRTUALENV ?= virtualenv.exe
	VENV_BIN = $(VENV_ROOT)/Scripts
else
	PYTHON  ?= python3
	VIRTUALENV ?= $(PYTHON) -m venv
	VENV_BIN = $(VENV_ROOT)/bin
endif

VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP    = $(VENV_PYTHON) -m pip

export PATH := $(VENV_BIN):$(PATH)

# Program availability
ifndef PYTHON
$(error "Python is not available please install Python")
else
ifneq ($(OS),Windows_NT)
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(error "Python is not available. Please install Python.")
endif
endif
endif

HAVE_NPM := $(shell command -v npm 2> /dev/null)
ifndef HAVE_NPM
$(error "npm is not available. Please install Node.js.")
endif
