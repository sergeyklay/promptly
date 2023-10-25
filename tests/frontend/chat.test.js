// This file is part of the Promptly.
//
// Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
//
// For the full copyright and license information, please view
// the LICENSE file that was distributed with this source code.

import {
    autoResizePromptTextarea,
    calculateTextareaHeight,
    createChatElement,
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

    const mockGetComputedStyle = (styles) => {
        window.getComputedStyle = jest.fn().mockReturnValue(styles);
    };

    test('should exit early if element is not a TEXTAREA', () => {
        const div = document.createElement('div');
        autoResizePromptTextarea(div);
        expect(div.style.height).toBe('');
    });

    test('should set height based on scrollHeight and other styles', () => {
        mockGetComputedStyle({
            lineHeight: '20px',
            borderBottomWidth: '1px',
            borderTopWidth: '1px',
            fontSize: '14px',
            paddingBottom: '2px',
            paddingTop: '2px',
            maxHeight: 'none'
        });

        textarea.value = 'Hello\nWorld';
        autoResizePromptTextarea(textarea);
        expect(parseFloat(textarea.style.height)).toBeGreaterThanOrEqual(textarea.scrollHeight);
    });

    test('should set overflowY to empty if maxHeight is reached', () => {
        mockGetComputedStyle({
            maxHeight: '50px',
        });

        // Mock the scrollHeight property
        Object.defineProperty(textarea, 'scrollHeight', {value: 100, configurable: true});

        textarea.value = 'A very long text that should exceed the max height';

        autoResizePromptTextarea(textarea);
        expect(textarea.style.overflowY).toBe('');
    });

    test('should calculate correct height with given line count and styles', () => {
        mockGetComputedStyle({
            lineHeight: '20px',
            borderBottomWidth: '1px',
            borderTopWidth: '1px',
            fontSize: '14px',
            paddingBottom: '2px',
            paddingTop: '2px'
        });

        textarea.value = 'Hello\nWorld';

        const calculatedHeight = calculateTextareaHeight(2, textarea);
        expect(calculatedHeight).toBeGreaterThanOrEqual(textarea.scrollHeight);
    });

    test('should calculate lineHeight based on fontSize if lineHeight is normal', () => {
        const fontSize = 14;
        const borderBottom = 1;
        const borderTop = 1;
        const paddingBottom = 2;
        const paddingTop = 2;

        mockGetComputedStyle({
            lineHeight: 'normal',
            fontSize: `${fontSize}px`,
            borderBottomWidth: `${borderBottom}px`,
            borderTopWidth: `${borderTop}px`,
            paddingBottom: `${paddingBottom}px`,
            paddingTop: `${paddingTop}px`,
        });

        textarea.value = 'Hello\nWorld';

        const calculatedHeight = calculateTextareaHeight(2, textarea);
        const expectedLineHeight = 1.2 * fontSize;
        const expectedHeight = expectedLineHeight + borderBottom + borderTop + paddingBottom + paddingTop;

        expect(calculatedHeight).toBeGreaterThanOrEqual(expectedHeight);
    });


    test('should set overflowY to hidden by default', () => {
        autoResizePromptTextarea(textarea);
        expect(textarea.style.overflowY).toBe('hidden');
    });
});
