============
Installation
============

Ensure you have the following installed on your machine:

- Python >= 3.10
- Node.js >= 16
- Your favorite text editor
  (*If you're an Emacs hacker, you'll feel right at home*)
- Basic understanding of OpenAPI, web development, and how GPT models work

Local Development
-----------------

It's highly recommended to use a virtual environment for local development to
keep the dependencies required by different projects separate and to avoid
potential conflicts. A virtual environment is a self-contained directory tree
that contains a Python installation for a particular version of Python, plus a
number of additional packages. This way, you can work on your project using its
specific dependencies, without any interference with other projects or system
libraries.

To create a virtual environment, follow these steps:

1. Install ``virtualenv`` if you haven't already:

.. code-block:: console

   $ pip install virtualenv

2. Navigate to your project directory:

.. code-block:: console

   $ git clone https://github.com/sergeyklay/promptly.git
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

Optionally you can add seed (fake) data to the database:

.. code-block:: console

   $ make seed

To install the necessary JS libraries run the following command in the ``frontend``
directory:

.. code-block:: console

   $ npm ci

To build JS part of the application run the following command in the ``frontend``
directory:

.. code-block:: console

   $ npm run build

Testing
--------

Run Python unit tests with coverage in the ``backend`` directory:

.. code-block:: console

   $ make test

Run JS unit tests with coverage in the ``frontend`` directory:

.. code-block:: console

   $ npm run test
