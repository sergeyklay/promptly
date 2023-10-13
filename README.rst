.. raw:: html

    <h1 align="center">Promptly</h1>
    <p align="center">
        <a href="https://github.com/sergeyklay/promptly/actions/workflows/test-code.yaml">
            <img src="https://github.com/sergeyklay/promptly/actions/workflows/test-code.yaml/badge.svg" alt="Test Code" />
        </a>
        <a href="https://github.com/sergeyklay/promptly/actions/workflows/lint-code.yaml">
            <img src="https://github.com/sergeyklay/promptly/actions/workflows/lint-code.yaml/badge.svg" alt="Lint Code" />
        </a>
        <a href="https://codecov.io/gh/sergeyklay/promptly" >
            <img src="https://codecov.io/gh/sergeyklay/promptly/graph/badge.svg?token=QoPTJP3wRv" alt="Coverage Status"/>
        </a>
        <br>
        <img src="https://github.com/sergeyklay/promptly/blob/main/docs/screenshot.png?raw=true" alt="Demo">
    </p>


.. teaser-begin

Welcome to Promptly, an open-source research project aimed at interacting with
OpenAPI compatible language models. If you're an engineer, data scientist, or
just an enthusiast looking for fine-grained control over your conversational
model, you're in the right place.

This project isn't production-ready. It's more like a sandbox where you can mess
around with prompt injections, fine-tuning, and much more. Do expect bugs; after
all, that's part of the fun!

Features:

- **Customizable API Calls:** Go beyond the traditional ChatGPT API limitations.
- **Prompt Injection:** Want to steer the conversation? Inject prompts to guide
  the model.
- **Fine-Tuning Support:** Got a model that's been fine-tuned? This project has
  you covered.
- **Multiple Models:** This isn't a one-trick pony. Use any OpenAPI-compatible
  model you like.

.. teaser-end

Local Development
=================

It's highly recommended to use a virtual environment for local development to
keep the dependencies required by different projects separate and to avoid
potential conflicts. A virtual environment is a self-contained directory tree
that contains a Python installation for a particular version of Python, plus a
number of additional packages. This way, you can work on your project using its
specific dependencies, without any interference with other projects or system
libraries.

To create a virtual environment, follow these steps:

1. Install `virtualenv` if you haven't already:

.. code-block:: console

   $ pip install virtualenv

2. Navigate to your project directory
   (assuming you've already cloned the repository):

.. code-block:: console

   $ cd promptly

3. Create a virtual environment in the project directory:

.. code-block:: console

   $ virtualenv venv

4. Activate the virtual environment:

.. code-block:: console

   # On Unix or MacOS, use:
   $ source venv/bin/activate

   # On Windows use:
   $ .\venv\Scripts\activate

Now you're in the virtual environment, and you can install dependencies isolated
from your global environment.

For more information on virtual environments, check out the official
`Python documentation <https://docs.python.org/3/tutorial/venv.html>`_.


Getting Started
===============

Prerequisites
-------------

Ensure you have the following installed on your machine:

- Python >= 3.10
- Your favorite text editor
  (*If you're an Emacs hacker, you'll feel right at home*)
- Basic understanding of OpenAPI, web development, and how GPT models work

Installing
----------

Clone the repository and navigate to the project directory:

.. code-block:: console

   $ git clone https://github.com/sergeyklay/promptly.git
   $ cd promptly

Install the necessary Python libraries:

.. code-block:: console

   $ make init
   $ make install

Run database migrations:

.. code-block:: console

   $ make migrate


Finally the necessary JS libraries:

.. code-block:: console

   $ npm ci

Optionally you can add seed (fake) data to the database:

.. code-block:: console

   $ make seed


Usage
-----

Work in progres...

.. -project-information-

Project Information
===================

Promptly is an open-source project under the `MIT License <https://choosealicense.com/licenses/mit/>`_,
with its code available at `GitHub <https://github.com/sergeyklay/promptly>`_.
It’s tested rigorously to ensure reliable interactions with ML models.

Contributions to Promptly are most welcome!

.. -support-


Support
=======

This project is a research tool and comes with no warranties. It might crash,
produce nonsensical outputs, or accidentally start a thermonuclear war. Use at
your own risk.

For any questions, remarks, or bug reporting, feel free to
`open an issue <https://github.com/sergeyklay/promptly/issues>`_ on GitHub.
