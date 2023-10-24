// This file is part of the Promptly.
//
// Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
//
// For the full copyright and license information, please view
// the LICENSE file that was distributed with this source code.

import {
    createChatElement,
    autoResizePromptTextarea
} from '../../promptly/static/js/chat.js';

describe('chat-elements', () => {
    test('should create a chat element with given message and role', () => {
        const element = createChatElement('Hello', 'user');
        expect(element.getAttribute('data-entry-role')).toBe('user');
        expect(element.textContent).toBe('Hello');
    });
});

describe('chat-textarea', () => {
    let originalGetComputedStyle;
    let textarea;

    beforeEach(() => {
        originalGetComputedStyle = window.getComputedStyle;
        textarea = document.createElement('textarea');
        document.body.appendChild(textarea);
    });

    afterEach(() => {
        window.getComputedStyle = originalGetComputedStyle;
        document.body.removeChild(textarea);
    });

    const createMockElement = (scrollHeight) => ({
        style: {},
        scrollHeight,
        setAttribute: jest.fn(),
    });

    const mockGetComputedStyle = (value) => {
        window.getComputedStyle = jest.fn().mockReturnValue({
            lineHeight: value,
        });
    };

    test('should update height based on scrollHeight', () => {
        mockGetComputedStyle('20px');

        const mockElement = createMockElement(50);
        autoResizePromptTextarea(mockElement);

        expect(mockElement.style.height).toBe('50px');
        expect(mockElement.style.overflowY).toBe('hidden');
    });

    test('should set height to 160 if scrollHeight is greater than maxHeight', () => {
        mockGetComputedStyle('20px');
        const mockElement = createMockElement(180);
        autoResizePromptTextarea(mockElement);

        expect(mockElement.style.height).toBe('160px');
        expect(mockElement.style.overflowY).toBe('auto');
    });

    test('should set overflowY to hidden by default', () => {
        autoResizePromptTextarea(textarea);

        expect(textarea.style.overflowY).toBe('hidden');
    });
});
