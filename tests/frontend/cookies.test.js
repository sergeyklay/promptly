// This file is part of the Promptly.
//
// Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
//
// For the full copyright and license information, please view
// the LICENSE file that was distributed with this source code.

import { getCookie, setCookie } from '../../promptly/static/js/cookie.js';

describe('cookies', () => {
    test('should set and get a cookie', () => {
        setCookie('test', 'value', 1);
        expect(getCookie('test')).toBe('value');
    });

    test('should return null if cookie not found', () => {
        expect(getCookie('nonexistent')).toBe(null);
    });

    test('should handle cookies with leading whitespace', () => {
        document.cookie = ' test=value';
        expect(getCookie('test')).toBe('value');
    });

    test('should handle cookies with multiple leading whitespaces', () => {
        document.cookie = '   foo=bar';
        expect(getCookie('foo')).toBe('bar');
    });
});
