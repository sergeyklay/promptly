# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

#
# -- Utils -----------------------------------------------------
#

import os
import sys


PROJECT_DIR = os.path.abspath('..')

sys.path.insert(0, PROJECT_DIR)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# General information about the project.
project = 'Promptly'
author = 'Serghei Iakovlev'
copyright = f'2023, {author}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# The following Sphinx extensions are being used:
# - sphinx.ext.autodoc: This extension generates documentation from docstrings
#   in the code.
# - sphinx.ext.intersphinx: This extension generates links to the documentation
#   of objects in other projects.
# - sphinx.ext.viewcode: This extension includes links to the source code in
#   the generated documentation.
# - sphinx.ext.doctest: This extension searches for and executes code snippets
#   embedded in the documentation to ensure they produce the expected outputs.
# - sphinx.ext.todo: This extension allows to insert TODO notes in the
#   documentation, which can be shown or hidden.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# Allow non-local URIs, so we can have images in CHANGELOG etc.
suppress_warnings = []

# The master toctree document.
master_doc = 'index'

# The version info
# The short X.Y version.
from promptly import __version__ as release  # noqa: E402
version = release.rsplit('.', 1)[0]
# The full version, including alpha/beta/rc tags.

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'any'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

#
# -- Options for autodoc -----------------------------------------------------
#

# Determines what content will be inserted into the main body of an autoclass
# directive.
# - 'class': Only the class' docstring is inserted.
# - 'both': Both the class’ and the ``__init__`` method’s docstrings are
#       concatenated and inserted.
# - 'init': Only the __init__ method’s docstring is inserted.
autoclass_content = 'class'

# List of modules to be mocked up. This is useful when you have dependencies
# that are not installed during the documentation build process. A mock object
# will be used instead.
autodoc_mock_imports = []

# If True, the docstring of the parent class will be inherited if the subclass
# doesn't have one.
autodoc_inherit_docstrings = True

# Determines the sorting order for documented members.
# 'bysource': Order by source order
# 'alphabetical': Alphabetically ('A' to 'Z')
autodoc_member_order = 'bysource'

# Controls how typehints are displayed in the generated documentation.
# - 'none': No type information.
# - 'description': Only used in the parameter description, like Sphinx’s
#      default format.
# - 'signature': Only used in the signature, like the style of mypy.
# - 'both': Used in the signature and in the parameter description.
autodoc_typehints = 'signature'

#
# -- Options for intersphinx -------------------------------------------------
#
intersphinx_mapping = {
    'alembic': ('https://alembic.sqlalchemy.org/en/latest/', None),
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master', None),
    'flask': ('https://flask.palletsprojects.com/en/3.0.x/', None),
    'werkzeug': ('https://werkzeug.palletsprojects.com/en/3.0.x/', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/20/', None),
    'flask_sqlalchemy': (
        'https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/', None),
    'flask_migrate': ('https://flask-migrate.readthedocs.io/en/latest/', None),
}

#
# -- Options for TODOs -------------------------------------------------------
#
todo_include_todos = True

# -- Options for HTML output ----------------------------------------------

# html_favicon = None

html_theme = 'alabaster'
html_title = project

html_theme_options = {}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, 'Created using Sphinx' is shown in the HTML footer. Default is True.
html_show_sphinx = True

# If true, '(C) Copyright ...' is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'promptlydoc'

#
# -- Options for manual page output ---------------------------------------
#

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', project, 'Promptly Documentation', [author], 1)
]

#
# -- Options for Texinfo output -------------------------------------------
#

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        'index',
        project,
        'Promptly Documentation',
        author,
        project,
        'A customizable ChatGPT API interface for OpenAPI models.',
        'Miscellaneous',
    )
]
