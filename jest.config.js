/** @type {import('jest').Config} */
const config = {
    moduleFileExtensions: ['js'],
    testEnvironment: 'jsdom',
    testPathIgnorePatterns: ['/node_modules/'],
    testMatch: ['**/tests/js/**/*.test.js'],
    transform: {
        '^.+\\.js$': 'babel-jest',
    },
    collectCoverage: true,
    verbose: true,
};

module.exports = config;
