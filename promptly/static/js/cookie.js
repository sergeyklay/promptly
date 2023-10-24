/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

/**
 * Sets a cookie with the given name, value, and expiration time.
 *
 * This function sets a cookie in the user's browser with a specific
 * name, value, and expiration time. The cookie will be accessible
 * from the JavaScript code for as long as it has not expired.
 *
 * @param {string} name - The name of the cookie.
 * @param {string} value - The value to store in the cookie.
 * @param {number} days - The number of days until the cookie expires.
 */
export function setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = `; expires=${date.toUTCString()}`;
  }

  let cookieValue = '';
  if (value) {
    cookieValue = value;
  }

  document.cookie = `${name}=${cookieValue}${expires}; path=/`;
}

/**
 * Retrieves a cookie value by its name.
 *
 * This function attempts to find a cookie set in the user's browser
 * with the given name. If found, it returns the value of that cookie;
 * otherwise, it returns null.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie or null if not found.
 */
export function getCookie(name) {
  const nameEQ = `${name}=`;
  const ca = document.cookie.split(';');

  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];

    while (c.charAt(0) === ' ') {
      c = c.substring(1, c.length);
    }

    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}
