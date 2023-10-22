// This file is part of the Promptly.
//
// Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
//
// For the full copyright and license information, please view
// the LICENSE file that was distributed with this source code.

import { createChatElement } from '../../promptly/static/js/chat.js';

describe('chat', () => {
    test('should create a chat element with given message and role', () => {
        const element = createChatElement('Hello', 'user');
        expect(element.getAttribute('data-entry-role')).toBe('user');
        expect(element.textContent).toBe('Hello');
    });
});
