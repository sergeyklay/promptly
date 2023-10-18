# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

BUILD_FLAGS   = -n -T -W

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from https://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help
help:
	@echo 'Promptly Documentation'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:      Show this help and exit'
	@echo '  clean:     Remove build artefacts'
	@echo '  html       Build standalone HTML files'
	@echo '  htmlhelp   Build HTML files and a HTML help project'
	@echo '  epub       Build an epub'
	@echo '  latex      Build LaTeX files, you can set PAPER=a4 or PAPER=letter'
	@echo '  latexpdf   Build LaTeX files and run them through pdflatex'
	@echo '  text       Build text files'
	@echo '  changes    Make an overview of all changed/added/deprecated items'
	@echo '  linkcheck  Check all external links for integrity'
	@echo
	@echo 'Programs:'
	@echo
	@echo '  sphinx-build:  $(shell sh -c "command -v $(SPHINXBUILD)")'

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*

.PHONY: html
html:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: htmlhelp
htmlhelp:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

.PHONY: epub
epub:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

.PHONY: latex
latex:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

.PHONY: latexpdf
latexpdf:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

.PHONY: text
text:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

.PHONY: changes
changes:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

.PHONY: linkcheck
linkcheck:
	$(SPHINXBUILD) $(BUILD_FLAGS) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."
