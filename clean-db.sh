#!/usr/bin/env bash

# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.


set -o pipefail

# To check rows use:
#
#     echo "SELECT * FROM chats;" | sqlite3 dev-db.sqlite3
#
echo "DELETE FROM chats;" | sqlite3 dev-db.sqlite3
