#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
KEY_WORDS:      QScintilla   code editor   lexer
CLASS_NAME:     QScintillaTab
WIDGETS:        QsciScintilla
STATUS:         runs_correctly_0_10      demo_complete_0_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      QScintilla / Reference
DESCRIPTION:    A minimal reference for the QScintilla editor widget
HOW_COMPLETE:   10  # small first pass, add more features later
"""

WIKI_LINK = "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QScintilla"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    pass
# --------------------



from qtpy import QtGui
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QPushButton)

from qtpy.Qsci import QsciScintilla, QsciLexerPython

import wat_inspector
import tab_base


# ---- end imports


class QScintillaTab(tab_base.TabBase):
    """
    Simple tab showing a QScintilla editor with a few core features.
    """

    def __init__(self):
        super().__init__()
        self.module_file = __file__  # save for help file usage

        global WIKI_LINK
        self.wiki_link = WIKI_LINK

        self.mutate_dict[0] = self.mutate_0
        self.mutate_dict[1] = self.mutate_1

        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout):
        """
        Build the GUI with a QScintilla editor and a few demo buttons.
        """
        layout = QGridLayout()
        main_layout.addLayout(layout)

        row = 0
        col = 0

        # ---- label
        label = QLabel("QScintilla code editor")
        layout.addWidget(label, row, col, 1, 2)

        # ---- the QScintilla editor
        row += 1
        self.editor = QsciScintilla()
        self._configure_editor(self.editor)
        layout.addWidget(self.editor, row, col, 1, 2)

        # ---- basic action buttons
        row += 1
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout, row, col, 1, 2)

        btn = QPushButton("set_sample\n_code")
        btn.clicked.connect(self.set_sample_code)
        button_layout.addWidget(btn)

        btn = QPushButton("clear\n_code")
        btn.clicked.connect(self.clear_code)
        button_layout.addWidget(btn)

        btn = QPushButton("toggle\nread_only")
        btn.clicked.connect(self.toggle_read_only)
        button_layout.addWidget(btn)

        # ---- final standard buttons from base class
        row += 1
        last_buttons_layout = QHBoxLayout()
        layout.addLayout(last_buttons_layout, row, col, 1, 2)
        self.build_gui_last_buttons(last_buttons_layout)

    #----------------------------
    def _configure_editor(self, editor: QsciScintilla):
        """
        Configure a few core QScintilla features:
        - Python lexer
        - line numbers
        - current line highlight
        - brace matching
        - basic folding
        """
        # lexer
        lexer = QsciLexerPython(editor)
        editor.setLexer(lexer)

        # line numbers in margin 0
        margin = 0
        number_margin = getattr(
            getattr(QsciScintilla, "MarginType", QsciScintilla),
            "NumberMargin",
            0,
        )
        editor.setMarginType(margin, number_margin)
        editor.setMarginWidth(margin, "0000")
        editor.setMarginsForegroundColor(QColor("#555555"))
        editor.setMarginsBackgroundColor(QColor("#f0f0f0"))

        # current line highlight
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QColor("#e8f2ff"))

        # brace matching
        brace_match_style = getattr(
            getattr(QsciScintilla, "BraceMatch", QsciScintilla),
            "SloppyBraceMatch",
            0,
        )
        editor.setBraceMatching(brace_match_style)

        # simple code folding
        fold_style = getattr(
            getattr(QsciScintilla, "FoldStyle", QsciScintilla),
            "BoxedTreeFoldStyle",
            0,
        )
        editor.setFolding(fold_style)

        # a few general editor options
        editor.setUtf8(True)
        editor.setIndentationGuides(True)
        editor.setAutoIndent(True)

    # ------------------------------------
    def set_sample_code(self):
        """
        Load a short Python snippet to show syntax highlighting and line numbers.
        """
        self.append_function_msg("set_sample_code()")

        sample = (
            "# QScintilla demo: basic Python code\n"
            "import sys\n\n"
            "def greet(name: str) -> None:\n"
            "    print(f\"Hello, {name} from QScintilla!\")\n\n"
            "if __name__ == '__main__':\n"
            "    greet('world')\n"
        )
        self.editor.setText(sample)
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def clear_code(self):
        """
        Clear all text from the editor.
        """
        self.append_function_msg("clear_code()")
        self.editor.clear()
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def toggle_read_only(self):
        """
        Toggle the editor's read-only state.
        """
        self.append_function_msg("toggle_read_only()")
        new_state = not self.editor.isReadOnly()
        self.editor.setReadOnly(new_state)
        self.append_msg(f"editor.readOnly -> {new_state}")
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def mutate_0(self):
        """
        Basic mutation: adjust font and tab width.
        """
        self.append_function_msg("mutate_0()")

        font = QtGui.QFont("Courier New", 11)
        self.editor.setFont(font)
        self.editor.setTabWidth(4)

        self.append_msg("set Courier 11pt, tab width 4", clear=False)
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def mutate_1(self):
        """
        Mutation: change colors for a simple dark-ish theme.
        """
        self.append_function_msg("mutate_1()")

        editor = self.editor
        editor.setCaretLineBackgroundColor(QColor("#333333"))
        editor.setCaretForegroundColor(QColor("#ffffff"))
        editor.setMarginsForegroundColor(QColor("#aaaaaa"))
        editor.setMarginsBackgroundColor(QColor("#222222"))
        editor.setPaper(QColor("#202020"))
        editor.setColor(QColor("#f0f0f0"))

        self.append_msg("applied simple dark-ish palette", clear=False)
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------
    def inspect(self):
        """
        The usual: hand off locals/globals to wat_inspector.
        """
        self.append_function_msg(tab_base.INSPECT_MSG)

        local_self = self
        local_editor = self.editor
        wat_inspector.go(
            msg="inspect QScintillaTab",
            a_locals=locals(),
            a_globals=globals(),
        )

        self.append_msg(tab_base.DONE_MSG)

    # ------------------------
    def breakpoint(self):
        """
        Break into this tab's code.
        """
        self.append_function_msg(tab_base.BREAK_MSG)
        breakpoint()
        self.append_msg(tab_base.DONE_MSG)

