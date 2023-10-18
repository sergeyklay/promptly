# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
The ``services`` package contains service classes and functions that
encapsulate the logic for interacting with external systems such as the
OpenAI API.

Each service is defined in its own module, and the ``__init__.py`` file is
used to aggregate these exports into a single namespace for easier import and
usage elsewhere in the application.
"""

from promptly.services.openai_service import OpenAIService  # noqa: F401
