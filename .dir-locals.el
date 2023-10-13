;;; This file is part of the Promptly.
;;;
;;; Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
;;;
;;; For the full copyright and license information, please view
;;; the LICENSE file that was distributed with this source code.

;;; Commentary:

;; Directory Local Variables

;; This file is for setting local variables in Emacs. Local variables
;; are used to customize the behavior of Emacs on a per-directory basis.

;; For a deeper understanding, you can refer to:
;; - Inside Emacs, run the command: (info "(emacs) Directory Variables")
;; - In the terminal, execute: info "(emacs) Directory Variables"
;;
;; Note: In some installations may be necessary to specify the info path using
;; '-d' like so:
;;
;;   info -d /Applications/Emacs.app/Contents/Resources/info "(emacs) Directory Variables"

;;; Code:

((python-mode . ((indent-tabs-mode . nil)      ; Use spaces, not tabs
                 (tab-width . 4)               ; A tab is four spaces
                 (fill-column . 79)            ; Set fill column to 79 chars
                 (python-indent-offset . 4)))) ; Set indentation to 4 spaces

;;; Commentary:
;;
;; - `indent-tabs-mode':
;;   Set to `nil` to use spaces for indentation instead of tabs. This is the
;;   conventional way to indent Python code.
;;
;; - `tab-width':
;;   This sets the number of spaces a tab character represents. The conventional
;;   setting is 4 for Python code.
;;
;; - `fill-column':
;;   This sets the column beyond which automatic line-wrapping occurs. Setting
;;   it to 79 is in compliance with PEP 8, which is the style guide for writing
;;   Python code.
;;
;; - `python-indent-offset':
;;   This sets the number of spaces for each indentation level in Python mode.
;;   The conventional setting is 4.
;;
;; This configuration ensures that your Python code is neatly formatted and
;; adheres to common style guidelines, making it easier for other developers to
;; read and understand your code.
