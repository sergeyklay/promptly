/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

/** @type {import('jest').Config} */
const config = {
    moduleFileExtensions: ['js'],
    testEnvironment: 'jsdom',
    testPathIgnorePatterns: ['/node_modules/'],
    testMatch: ['**/tests/frontend/**/*.test.js'],
    transform: {
        '^.+\\.js$': 'babel-jest',
    },
    collectCoverage: true,
    verbose: true,
};

module.exports = config;
