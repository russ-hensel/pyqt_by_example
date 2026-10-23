#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
KEY_WORDS:      spell check, spelling, enchant, QSyntaxHighlighter, squiggle underline, suggestions, plain text edit
CLASS_NAME:     QPlainTextEditSpellTab
WIDGETS:        QPlainTextEdit QSyntaxHighlighter
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      QPlainTextEdit / Spell Check
DESCRIPTION:    QPlainTextEdit with local spell checking, pyenchant + QSyntaxHighlighter
HOW_COMPLETE:   20  #  AND A COMMENT

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QPlainTextEdit"

"""
scratch

    spell check, the short version:
        Qt has no spell check, so:
        a QSyntaxHighlighter on widget.document() draws the red squiggle,
            display only, the text and undo stack are not touched
        pyenchant ( pip install pyenchant ) does the checking, uses the
            system libenchant and hunspell dictionaries, all local
        right click on a flagged word for suggestions, built on
            createStandardContextMenu()
        the same code works for a QTextEdit, it only uses document(),
            cursorForPosition() ... which both have
        a document can have only one QSyntaxHighlighter

    QPlainTextEdit vs QTextEdit, the short version:
        no setText(), use setPlainText()
        appendPlainText() adds a new paragraph ( line ), appendHtml() also exists
        no setTextColor(), setFontPointSize() ... -- no per character formatting
            from the widget, though a QTextCursor can still do some
        setMaximumBlockCount() -- keep only the last n lines, great for logs
        blockCount(), blockCountChanged signal
        scrolls by line ( paragraph ) not by pixel, faster on big text

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    pass
# --------------------


import re

from qtpy import QtCore
from qtpy.QtGui import (QSyntaxHighlighter,
                        QTextCharFormat,
                        QTextCursor,
                        QTextDocument)

from qtpy.QtWidgets import (QAction,
                             QApplication,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMenu,
                             QPlainTextEdit,
                             QPushButton)

import utils_for_tabs as uft
import wat_inspector
import tab_base

try:
    import enchant                  # uv pip install pyenchant
except ImportError:
    enchant     = None
    1/0   # remove if you want to go on without spell check

# ---- end imports


INDENT          = uft.INDENT
SPELL_LANG      = "en_US"

# letters, with inner apostrophes so don't and you’re are one word
# [^\W\d_] is "a letter" in any language
WORD_RE         = re.compile( r"[^\W\d_]+(?:['’][^\W\d_]+)*" )


# ----------------------------------------
class SpellHighlighter( QSyntaxHighlighter ):
    """
    underline misspelled words in a QTextDocument
    works for QPlainTextEdit and QTextEdit, pass it widget.document()
    highlightBlock() is called by Qt one block ( line ) at a time,
    only for blocks that changed
    """
    def __init__( self, document, spell_dict ):
        """
        spell_dict      an enchant.Dict, or anything with check( word )
        """
        super().__init__( document )
        self.spell_dict     = spell_dict
        self.enabled        = True

        a_format            = QTextCharFormat()
        a_format.setUnderlineColor( QtCore.Qt.GlobalColor.red )
        a_format.setUnderlineStyle( QTextCharFormat.UnderlineStyle.SpellCheckUnderline )
        self.err_format     = a_format

    # -----------------------
    def check( self, word ):
        """
        True if spelled ok, enchant does not like the curly apostrophe
        """
        return self.spell_dict.check( word.replace( "’", "'" ) )

    # -----------------------
    def highlightBlock( self, text ):
        """
        what it says
        """
        if not self.enabled or self.spell_dict is None:
            return

        err_format      = self.err_format
        for i_match in WORD_RE.finditer( text ):
            if not self.check( i_match.group() ):
                self.setFormat( i_match.start(),
                                i_match.end() - i_match.start(),
                                err_format )

    # -----------------------
    def set_enabled( self, enabled ):
        """
        rehighlight() runs highlightBlock() on every block,
        when disabled that clears the squiggles
        """
        self.enabled    = enabled
        self.rehighlight()


#  --------
class QPlainTextEditSpellTab( tab_base.TabBase ) :
    def __init__(self):
        """
        the usual
        tab_q_plain_text_edit_spell.py
        """
        super().__init__()
        self.module_file        = __file__

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3

        self.log_line_count     = 0     # for append_log_lines
        self.menu_slot          = None  # the connected customContextMenuRequested slot
        self._build_gui()
        self.setup_spell_check()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QGridLayout(   )
        main_layout.addLayout( layout )

        # ---- the QPlainTextEdit
        ix_row     = 0
        ix_col     = 0
        row_span   = 1
        col_span   = 3

        widget                  = QPlainTextEdit()
        self.plain_text_edit    = widget
        widget.setMinimumHeight( 100 )
        widget.setPlaceholderText( "QPlainTextEdit -- type here or use the buttons" )

        # ---- signals
        widget.cursorPositionChanged.connect( self.on_cursor_position_changed )
        widget.blockCountChanged.connect(     self.on_block_count_changed )
        # widget.textChanged.connect( ... )            # no args, fires on every key
        # widget.selectionChanged.connect( ... )
        # widget.modificationChanged.connect( ... )    # bool
        # widget.undoAvailable / redoAvailable / copyAvailable  # bool

        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )

        # ---- status label, fed by the signals
        ix_row     += 1
        widget              = QLabel( "line: 1  col: 1  blocks: 1" )
        self.status_label   = widget
        layout.addWidget( widget, ix_row, ix_col, 1, col_span )

        # ----- search
        ix_row     += 1
        ix_col     = 0
        row_span   = 1
        col_span   = 1

        widget             = QLineEdit()
        self.line_edit     = widget
        widget.setText( "Python" )
        widget.setPlaceholderText( "Enter search text" )
        layout.addWidget( widget, ix_row, ix_col, row_span,  col_span )

        ix_col     += 1
        widget           = QPushButton( "Down" )
        self.down_button = widget
        widget.clicked.connect( self.search_down )
        layout.addWidget( widget, ix_row, ix_col, row_span,  col_span )

        ix_col     += 1
        widget           = QPushButton( "Up" )
        self.up_button   = widget
        widget.clicked.connect( self.search_up )
        layout.addWidget( widget, ix_row, ix_col, row_span,  col_span )

        # ---- lower buttons
        ix_row     += 1
        ix_col     = 0
        col_span   = 3
        button_layout = QHBoxLayout(   )
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        # ---- PB set_plain\n_text_1
        widget = QPushButton( "set_plain\n_text_1" )
        widget.clicked.connect(  self.set_plain_text_1 )
        button_layout.addWidget( widget,   )

        # ---- PB set_plain\n_text_2
        widget = QPushButton( "set_plain\n_text_2" )
        widget.clicked.connect(  self.set_plain_text_2 )
        button_layout.addWidget( widget,   )

        # ---- PB insert_plain\n_text
        widget = QPushButton( "insert_plain\n_text" )
        widget.clicked.connect( self.insert_plain_text  )
        button_layout.addWidget( widget,  )

        # ---- PB append_plain\n_text
        widget = QPushButton( "append_plain\n_text" )
        widget.clicked.connect( self.append_plain_text  )
        button_layout.addWidget( widget,  )

        # ---- PB append\n_html
        widget = QPushButton( "append\n_html" )
        widget.clicked.connect( self.append_html  )
        button_layout.addWidget( widget,  )

        # ---- PB clear_text
        widget = QPushButton( "clear\n_text" )
        widget.clicked.connect( self.clear_text )
        button_layout.addWidget( widget,   )

        # ---- new row
        button_layout = QHBoxLayout( )
        ix_row    += 1
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        # ---- PB copy_all_text
        widget = QPushButton( "copy_all\n_text" )
        widget.clicked.connect( self.copy_all_text  )
        button_layout.addWidget( widget,   )

        # ---- PB copy_line_of_text
        widget = QPushButton( "copy_line\n_of_text" )
        widget.clicked.connect( self.copy_line_of_text )
        button_layout.addWidget( widget,   )

        # ---- PB copy_n_lines_of_text
        widget = QPushButton( "copy_5_lines\n_of_text" )
        widget.clicked.connect( lambda: self.copy_n_lines_of_text( 5 ) )
        button_layout.addWidget( widget,   )

        # ---- PB copy_selected_text
        widget = QPushButton( "copy_selected\n_text" )
        widget.clicked.connect( self.copy_selected_text )
        button_layout.addWidget( widget,   )

        # ---- PB show_lines
        widget = QPushButton( "show\n_lines" )
        widget.clicked.connect( self.show_lines )
        button_layout.addWidget( widget,   )

        # ---- new row
        button_layout = QHBoxLayout( )
        ix_row    += 1
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        # ---- PB cursor_to_begin
        widget = QPushButton( "cursor\n_to_begin" )
        widget.clicked.connect( self.cursor_to_begin )
        button_layout.addWidget( widget, )

        # ---- PB cursor_to_end
        widget = QPushButton( "cursor\n_to_end" )
        widget.clicked.connect( self.cursor_to_end )
        button_layout.addWidget( widget, )

        # ---- PB go_to_line
        widget = QPushButton( "go_to\n_line_10" )
        widget.clicked.connect( lambda: self.go_to_line( 10 ) )
        button_layout.addWidget( widget, )

        # ---- PB append_log_lines
        widget = QPushButton( "append_log\n_lines" )
        widget.clicked.connect( self.append_log_lines )
        button_layout.addWidget( widget, )

        # ---- PB toggle_wrap
        widget = QPushButton( "toggle\n_wrap" )
        widget.clicked.connect( self.toggle_wrap )
        button_layout.addWidget( widget, )

        # ---- new row, spell check
        button_layout = QHBoxLayout( )
        ix_row    += 1
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        # ---- PB set_misspelled_text
        widget = QPushButton( "set_misspelled\n_text" )
        widget.clicked.connect( self.set_misspelled_text )
        button_layout.addWidget( widget, )

        # ---- PB toggle_spell_check
        widget = QPushButton( "toggle_spell\n_check" )
        widget.clicked.connect( self.toggle_spell_check )
        button_layout.addWidget( widget, )

        # ---- PB list_misspelled
        widget = QPushButton( "list\n_misspelled" )
        widget.clicked.connect( self.list_misspelled )
        button_layout.addWidget( widget, )

        # ---- PB next_misspelled
        widget = QPushButton( "next\n_misspelled" )
        widget.clicked.connect( self.next_misspelled )
        button_layout.addWidget( widget, )

        # ---- PB show_languages
        widget = QPushButton( "show\n_languages" )
        widget.clicked.connect( self.show_languages )
        button_layout.addWidget( widget, )

        # ---- new row
        button_layout = QHBoxLayout(   )
        ix_row    += 1
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        self.build_gui_last_buttons( button_layout )

    # ---- signal slots
    # ---------------------------------------
    def on_cursor_position_changed( self ):
        """
        cursorPositionChanged has no args, ask the cursor
        blockNumber() is the 0 based line ( paragraph ) number
        no append_msg here, it would fire on every key and click
        """
        self.update_status_label()

    # ---------------------------------------
    def on_block_count_changed( self, new_block_count ):
        """
        blockCountChanged( int ) -- one of the few QPlainTextEdit only signals
        """
        self.update_status_label()

    # ---------------------------------------
    def update_status_label( self ):
        """
        what it says
        """
        widget      = self.plain_text_edit
        cursor      = widget.textCursor()
        line        = cursor.blockNumber()      + 1
        col         = cursor.positionInBlock()  + 1
        blocks      = widget.blockCount()
        self.status_label.setText( f"line: {line}  col: {col}  blocks: {blocks}" )

    # ---- spell check
    # ---------------------------------------
    def setup_spell_check( self ):
        """
        make the dictionary and attach the highlighter to the document
        if pyenchant or the language is missing the tab still runs,
        just with no spell check
        the context menu is set by mutate_0, which _build_gui runs
        """
        self.spell_dict     = None
        if enchant is None:
            self.append_msg( "!! pyenchant not installed, no spell check  "
                             "( pip install pyenchant )" )
        else:
            try:
                self.spell_dict     = enchant.Dict( SPELL_LANG )
            except enchant.errors.DictNotFoundError:
                self.append_msg( f"!! no enchant dictionary for {SPELL_LANG}, "
                                 f"have: {enchant.list_languages()}" )

        widget              = self.plain_text_edit
        self.highlighter    = SpellHighlighter( widget.document(), self.spell_dict )

    # ---------------------------------------
    def word_at( self, cursor ):
        """
        return ( word, cursor selecting the word ) for the word at the
        cursor position, or ( None, None )
        uses WORD_RE, same as the highlighter, rather than
        QTextCursor.WordUnderCursor which splits don't into don + t
        """
        block           = cursor.block()
        pos_in_block    = cursor.positionInBlock()

        for i_match in WORD_RE.finditer( block.text() ):
            if i_match.start() <= pos_in_block <= i_match.end():
                word_cursor     = QTextCursor( block )
                word_cursor.setPosition( block.position() + i_match.start() )
                word_cursor.setPosition( block.position() + i_match.end(),
                                         QTextCursor.MoveMode.KeepAnchor )
                return i_match.group(), word_cursor

        return None, None

    # ---------------------------------------
    def add_spell_actions( self, menu, pos ):
        """
        if the word under the mouse is misspelled put suggestions,
        ignore and add to dictionary at the top of menu
        pos is in widget viewport coordinates, as given by
        customContextMenuRequested
        """
        highlighter     = self.highlighter
        if self.spell_dict is None or not highlighter.enabled:
            return

        widget          = self.plain_text_edit
        if widget.isReadOnly():
            return

        word, word_cursor   = self.word_at( widget.cursorForPosition( pos ) )
        if word is None or highlighter.check( word ):
            return

        first_action    = menu.actions()[ 0 ] if menu.actions() else None
        new_actions     = []

        suggestions     = self.spell_dict.suggest( word.replace( "’", "'" ) )[ :8 ]
        if not suggestions:
            action      = QAction( "( no suggestions )", menu )
            action.setEnabled( False )
            new_actions.append( action )

        for i_sugg in suggestions:
            action      = QAction( i_sugg, menu )
            # default args freeze the loop values, insertText on a cursor with
            # a selection replaces it, one undo step
            action.triggered.connect(
                lambda _checked = False, a_sugg = i_sugg, a_cursor = word_cursor:
                    a_cursor.insertText( a_sugg ) )
            new_actions.append( action )

        # session only, forgotten when the app closes
        action      = QAction( f"Ignore '{word}'", menu )
        action.triggered.connect( lambda: self.ignore_word( word ) )
        new_actions.append( action )

        # personal word list, ~/.config/enchant/en_US.dic, permanent
        action      = QAction( f"Add '{word}' to dictionary", menu )
        action.triggered.connect( lambda: self.add_word( word ) )
        new_actions.append( action )

        menu.insertActions( first_action, new_actions )
        menu.insertSeparator( first_action )

    # ---------------------------------------
    def ignore_word( self, word ):
        """
        what it says, for this run only
        """
        self.spell_dict.add_to_session( word.replace( "’", "'" ) )
        self.highlighter.rehighlight()
        self.append_msg( f"ignore_word() {word!r} for this session" )

    # ---------------------------------------
    def add_word( self, word ):
        """
        what it says, saved to the personal word list
        """
        self.spell_dict.add( word.replace( "’", "'" ) )
        self.highlighter.rehighlight()
        self.append_msg( f"add_word() {word!r} added to personal word list" )

    # ---- context menu
    #----------------------------
    def connect_context_menu( self, widget, slot ):
        """
        CustomContextMenu policy, and connect slot,
        disconnecting whatever was connected before
        """
        widget.setContextMenuPolicy( QtCore.Qt.ContextMenuPolicy.CustomContextMenu )

        if self.menu_slot is not None:
            try:
                widget.customContextMenuRequested.disconnect( self.menu_slot )
            except ( TypeError, RuntimeError ):
                pass    # was not connected

        widget.customContextMenuRequested.connect( slot )
        self.menu_slot      = slot

    #----------------------------
    def set_spell_context_menu( self, widget ):
        """
        the standard menu plus spelling suggestions
        stands in for the default context menu, which has no hook
        for adding suggestions
        """
        self.append_msg( "set_spell_context_menu() -- right click a misspelled word",)
        self.connect_context_menu( widget, self.show_spell_context_menu )

    #----------------------------
    def set_custom_context_menu( self, widget ):
        """
        what it says
        """
        self.append_msg( "set_custom_context_menu() -- try the context menu",)
        self.connect_context_menu( widget, self.show_context_menu )

    # ---------------------------------------
    def show_spell_context_menu( self, pos ):
        """
        createStandardContextMenu() gives the usual Undo, Cut ... menu,
        it is ours to delete, so parent it and let exec() finish first
        """
        widget      = self.plain_text_edit
        menu        = widget.createStandardContextMenu()
        self.add_spell_actions( menu, pos )

        menu.exec( widget.mapToGlobal( pos ) )
        menu.deleteLater()

    # ---------------------------------------
    def show_context_menu( self, pos ):
        """
        a custom menu, the standard actions plus a couple of our own
        plus the spelling suggestions
        """
        widget      = self.plain_text_edit
        menu        = QMenu( widget )

        undo_action = menu.addAction( "Undo" )
        undo_action.triggered.connect( widget.undo )
        menu.addSeparator()

        cut_action = menu.addAction( "Cut" )
        cut_action.triggered.connect( widget.cut )
        copy_action = menu.addAction( "Copy" )
        copy_action.triggered.connect( widget.copy )

        paste_action = menu.addAction( "Paste" )
        paste_action.triggered.connect( widget.paste )
        menu.addSeparator()

        select_all_action = menu.addAction( "Select All" )
        select_all_action.triggered.connect( widget.selectAll )

        # ---- non standard
        menu.addSeparator()
        upper_action = menu.addAction( "Upper case selection" )
        upper_action.triggered.connect( self.upper_case_selection )

        # enable/disable actions based on context
        has_selection   = widget.textCursor().hasSelection()
        can_undo        = widget.document().isUndoAvailable()
        can_paste       = widget.canPaste()     # QPlainTextEdit has this, simpler than the clipboard

        undo_action.setEnabled(  can_undo )
        cut_action.setEnabled(   has_selection )
        copy_action.setEnabled(  has_selection )
        paste_action.setEnabled( can_paste )
        upper_action.setEnabled( has_selection )

        self.add_spell_actions( menu, pos )

        menu.exec( widget.mapToGlobal( pos ) )
        menu.deleteLater()

    # ---------------------------------------
    def upper_case_selection( self ):
        """
        replace the selection, insertText on a cursor with a selection
        replaces it, and is one undo step
        """
        cursor          = self.plain_text_edit.textCursor()
        cursor.insertText( cursor.selectedText().upper() )

    # ---- button actions
    #  --------
    def clear_text( self ):
        """
        what it says
        """
        self.append_function_msg( "clear_text()" )

        self.plain_text_edit.clear()
        self.append_msg( tab_base.DONE_MSG )

    # ----
    def set_plain_text_1( self,  ):
        """
        setPlainText -- QPlainTextEdit has no setText()
        replaces everything, clears undo history
        """
        self.append_function_msg( "set_plain_text_1()" )

        a_string    = (
"""More than 20 years have passed since I authored the Python Essential Reference. At that time,
Python was a much smaller language and it came with a useful set of batteries in its
standard library. It was something that could mostly fit in your brain. The Essential Reference
reflected that era. It was a small book that you could take with you to write some Python
code on a desert island or inside a secret vault. Over the three subsequent revisions, the
Essential Reference stuck with this vision of being a compact but complete language
reference—because if you’re going to code in Python on vacation, why not use all of it?

Python Distilled David M. Beazley""" )

        self.plain_text_edit.setPlainText( a_string )

        self.append_msg( f"{self.plain_text_edit.blockCount() = }" )
        self.append_msg( tab_base.DONE_MSG )

    #---------------
    def set_plain_text_2( self,  ):
        """
        a lot of text, enough to scroll
        """
        self.append_function_msg( "set_plain_text_2()" )

        a_string    = 22  * (
"""HOMEXCEL Sponges Kitchen 24pcs, Non-Scratch Scrub Dish Sponges,
Safe on Non-Stick Cookware,Dual Sided Cleaning Sponges
for Kitchen,Household,Bathroom and More

""" )

        self.plain_text_edit.setPlainText( a_string )

        self.append_msg( f"{self.plain_text_edit.blockCount() = }" )
        self.append_msg( tab_base.DONE_MSG )

    #--------
    def insert_plain_text( self, ):
        """
        insertPlainText -- insert at the cursor position, replaces any selection
        """
        self.append_function_msg( "insert_plain_text()" )

        a_string  = ( """>>---- so here is a bit
of text the we will
           ------------------> insert
at the cursor ----<<""")

        self.plain_text_edit.insertPlainText( a_string )
        self.append_msg( tab_base.DONE_MSG )

    #--------
    def append_plain_text( self, ):
        """
        appendPlainText -- always at the end, always as a new paragraph,
        does not move the user's cursor
        """
        self.append_function_msg( "append_plain_text()" )

        a_string  = ( "appended with appendPlainText() -- a new line at the end" )
        self.plain_text_edit.appendPlainText( a_string )
        self.append_msg( tab_base.DONE_MSG )

    #--------
    def append_html( self, ):
        """
        appendHtml -- yes QPlainTextEdit can do this, but only a
        subset of formatting survives, and toPlainText() strips it
        """
        self.append_function_msg( "append_html()" )

        a_string  = ( "<b>bold</b> <i>italic</i> "
                      "<span style='color:red'>red</span> "
                      "from appendHtml()" )
        self.plain_text_edit.appendHtml( a_string )
        self.append_msg( tab_base.DONE_MSG )

    #  --------
    def copy_all_text( self, ):
        """
        two ways, toPlainText() to the clipboard, or
        selectAll(), copy(), and restore the cursor
        """
        self.append_function_msg( "copy_all_text()" )

        widget              = self.plain_text_edit
        all_text            = widget.toPlainText()
        self.append_msg( f"{len( all_text ) = }" )

        # ---- way 2, uses the widget's own copy()
        cursor              = widget.textCursor()
        original_position   = cursor.position()

        widget.selectAll()
        widget.copy()

        cursor.setPosition( original_position )
        widget.setTextCursor( cursor )

        self.append_msg( "all text copied to clipboard" )
        self.append_msg( tab_base.DONE_MSG )

    #----------------------------
    def copy_selected_text( self,  ):
        """
        note: selectedText() uses \\u2029 not \\n between lines,
        so convert before using it
        """
        self.append_function_msg( "copy_selected_text()" )

        selected_text   = self.plain_text_edit.textCursor().selectedText()
        selected_text   = selected_text.replace( " ", "\n" )
        QApplication.clipboard().setText( selected_text )

        self.append_msg( f"   -> {selected_text = } now in clipboard" )
        self.append_msg( tab_base.DONE_MSG )

    #----------------------
    def copy_line_of_text( self, ):
        """
        copy the line ( block ) the cursor is in, the block way,
        no cursor moving at all
        """
        self.append_function_msg( "copy_line_of_text()" )

        cursor          = self.plain_text_edit.textCursor()
        selected_text   = cursor.block().text()
        QApplication.clipboard().setText( selected_text )

        self.append_msg( f"line {cursor.blockNumber() + 1}: {selected_text = }" )
        self.append_msg( tab_base.DONE_MSG )

    #----------------------
    def copy_n_lines_of_text( self, num_lines ):
        """
        copy some number of lines starting at the cursor line,
        walking the QTextBlock s
        """
        self.append_function_msg( "copy_n_lines_of_text()" )

        block   = self.plain_text_edit.textCursor().block()
        lines   = []
        for ix in range( num_lines ):
            if not block.isValid():
                break
            lines.append( block.text() )
            block   = block.next()

        QApplication.clipboard().setText( "\n".join( lines ) )

        for ix, i_line in enumerate( lines ):
            self.append_msg( f"{INDENT}{ix} >>{i_line}<<" )
        self.append_msg( tab_base.DONE_MSG )
        return lines

    #----------------------
    def show_lines( self, ):
        """
        all lines as a list, toPlainText() uses \\n here
        """
        self.append_function_msg( "show_lines()" )

        lines   = self.plain_text_edit.toPlainText().split( "\n" )
        self.append_msg( f"{len( lines ) = }" )
        for ix, i_line in enumerate( lines ):
            if ix >= 10:
                self.append_msg( "skipping additional lines " )
                break
            self.append_msg( f"{INDENT}{ix} >>{i_line}<<" )

        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def cursor_to_begin( self,  ):
        """
        moveCursor() is a QPlainTextEdit shortcut for
        textCursor(), movePosition(), setTextCursor()
        """
        self.append_function_msg( "cursor_to_begin()" )

        widget   = self.plain_text_edit
        widget.moveCursor( QTextCursor.MoveOperation.Start )
        widget.ensureCursorVisible()
        widget.setFocus()

        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def cursor_to_end( self,  ):
        """
        what it says, read
        """
        self.append_function_msg( "cursor_to_end()" )

        widget   = self.plain_text_edit
        widget.moveCursor( QTextCursor.MoveOperation.End )
        widget.ensureCursorVisible()
        widget.setFocus()

        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def go_to_line( self, line_number ):
        """
        line_number is 1 based like an editor,
        findBlockByNumber is 0 based
        """
        self.append_function_msg( "go_to_line()" )

        widget      = self.plain_text_edit
        block       = widget.document().findBlockByNumber( line_number - 1 )
        if not block.isValid():
            self.append_msg( f"no line {line_number}, only {widget.blockCount()} lines" )
            return

        cursor      = widget.textCursor()
        cursor.setPosition( block.position() )
        widget.setTextCursor( cursor )
        widget.centerCursor()       # QPlainTextEdit only, scroll so cursor is mid widget
        widget.setFocus()

        self.append_msg( f"cursor now on line {line_number}" )
        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def append_log_lines( self, ):
        """
        the classic QPlainTextEdit use, a log viewer
        setMaximumBlockCount() drops lines off the top
        mutate_2 sets the maximum
        """
        self.append_function_msg( "append_log_lines()" )

        widget      = self.plain_text_edit
        for ix in range( 10 ):
            self.log_line_count += 1
            widget.appendPlainText( f"log line {self.log_line_count}" )

        self.append_msg( f"{widget.maximumBlockCount() = }   ( 0 means no limit )" )
        self.append_msg( f"{widget.blockCount() = }" )
        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def toggle_wrap( self, ):
        """
        lineWrapMode is NoWrap or WidgetWidth for QPlainTextEdit
        ( no FixedPixelWidth / FixedColumnWidth like QTextEdit )
        """
        self.append_function_msg( "toggle_wrap()" )

        widget      = self.plain_text_edit
        LineWrap    = QPlainTextEdit.LineWrapMode
        if widget.lineWrapMode() == LineWrap.NoWrap:
            widget.setLineWrapMode( LineWrap.WidgetWidth )
        else:
            widget.setLineWrapMode( LineWrap.NoWrap )

        self.append_msg( f"{widget.lineWrapMode() = }" )
        self.append_msg( tab_base.DONE_MSG )

    # ---- spell check buttons
    # --------------------
    def set_misspelled_text( self, ):
        """
        some text with mistakes, right click the red ones
        """
        self.append_function_msg( "set_misspelled_text()" )

        a_string    = (
"""Teh quick brown fox jumpd over the lazzy dog.
Spell checking in Qt is not built in, so we recieve a litle help
from enchant, which uses the same hunspell dictionarys as LibreOffice.
Words with apostrophes: don't, can't, you’re, it's, are all fine.
Numbers like 1234 and mixed things like abc123 are skipped or split.
HOMEXCEL and other ALLCAPS words get flagged too.""" )

        self.plain_text_edit.setPlainText( a_string )
        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def toggle_spell_check( self, ):
        """
        what it says, the text is not changed either way
        """
        self.append_function_msg( "toggle_spell_check()" )

        highlighter     = self.highlighter
        highlighter.set_enabled( not highlighter.enabled )

        self.append_msg( f"{highlighter.enabled = }" )
        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def list_misspelled( self, ):
        """
        walk the blocks and check each word, the same test
        the highlighter uses
        """
        self.append_function_msg( "list_misspelled()" )

        if self.spell_dict is None:
            self.append_msg( "no spell check dictionary" )
            return

        highlighter     = self.highlighter
        block           = self.plain_text_edit.document().firstBlock()
        count           = 0
        while block.isValid():
            for i_match in WORD_RE.finditer( block.text() ):
                word    = i_match.group()
                if not highlighter.check( word ):
                    count  += 1
                    self.append_msg( f"{INDENT}line {block.blockNumber() + 1:3} "
                                     f"col {i_match.start() + 1:3}  {word}" )
            block   = block.next()

        self.append_msg( f"{count} misspelled" )
        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def next_misspelled( self, ):
        """
        select the next misspelled word after the cursor, wrap to the top
        """
        self.append_function_msg( "next_misspelled()" )

        if self.spell_dict is None:
            self.append_msg( "no spell check dictionary" )
            return

        widget          = self.plain_text_edit
        highlighter     = self.highlighter
        document        = widget.document()
        start_pos       = widget.textCursor().selectionEnd()

        for ix_pass in range( 2 ):      # second pass wraps from the top
            block   = document.firstBlock() if ix_pass else document.findBlock( start_pos )
            while block.isValid():
                for i_match in WORD_RE.finditer( block.text() ):
                    word_start  = block.position() + i_match.start()
                    if ix_pass == 0 and word_start < start_pos:
                        continue
                    if not highlighter.check( i_match.group() ):
                        cursor  = QTextCursor( document )
                        cursor.setPosition( word_start )
                        cursor.setPosition( block.position() + i_match.end(),
                                            QTextCursor.MoveMode.KeepAnchor )
                        widget.setTextCursor( cursor )
                        widget.setFocus()
                        self.append_msg( f"{i_match.group()!r}" )
                        return
                block   = block.next()

        self.append_msg( "no misspelled words" )

    # --------------------
    def show_languages( self, ):
        """
        what enchant can see, and which backend ( hunspell, aspell ... )
        """
        self.append_function_msg( "show_languages()" )

        if enchant is None:
            self.append_msg( "pyenchant not installed" )
            return

        self.append_msg( f"{enchant.list_languages() = }" )
        if self.spell_dict is not None:
            self.append_msg( f"{self.spell_dict.tag = }" )
            self.append_msg( f"{self.spell_dict.provider.name = }" )
        self.append_msg( tab_base.DONE_MSG )

    # ---------------------
    def search_down( self ):
        """
        find() searches from the current cursor and selects the hit
        wrap to the top if nothing found
        """
        self.search( backward = False )

    # ---------------------
    def search_up( self ):
        """
        what it says
        """
        self.search( backward = True )

    # ---------------------
    def search( self, backward ):
        """
        what it says
        """
        widget          = self.plain_text_edit
        search_text     = self.line_edit.text()
        if not search_text:
            return

        if backward:
            flags       = QTextDocument.FindFlag.FindBackward
            wrap_to     = QTextCursor.MoveOperation.End
        else:
            flags       = QTextDocument.FindFlag( 0 )
            wrap_to     = QTextCursor.MoveOperation.Start

        found   = widget.find( search_text, flags )
        if not found:
            widget.moveCursor( wrap_to )
            found   = widget.find( search_text, flags )

        if not found:
            self.append_msg( f"{search_text!r} not found" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        back to the defaults
        """
        self.append_function_msg( "mutate_0()" )

        widget  = self.plain_text_edit
        self.set_spell_context_menu( widget )

        widget.setReadOnly( False )
        widget.setMaximumBlockCount( 0 )            # 0 means no limit
        # setMaximumBlockCount() turns off undo, even for 0, so turn it back on
        # otherwise picking a spelling suggestion can not be undone
        widget.setUndoRedoEnabled( True )
        widget.setLineWrapMode( QPlainTextEdit.LineWrapMode.WidgetWidth )
        widget.setCenterOnScroll( False )
        widget.setTabStopDistance( 80 )             # pixels

        self.append_msg( "spell context menu, read write, no block limit, wrap" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )

        widget  = self.plain_text_edit
        self.set_custom_context_menu( widget )

        widget.setLineWrapMode( QPlainTextEdit.LineWrapMode.NoWrap )
        widget.setCenterOnScroll( True )    # can scroll past the end so last line can be centered
        widget.setTabStopDistance( 20 )

        self.append_msg( "custom context menu, no wrap, center on scroll, narrow tabs" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2()" )

        widget  = self.plain_text_edit
        widget.setMaximumBlockCount( 25 )

        self.append_msg( "setMaximumBlockCount( 25 ) -- now try append_log_lines" )
        self.append_msg( f"{widget.blockCount() = }  ( extra lines were dropped from the top )" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_3()" )

        widget  = self.plain_text_edit
        widget.setReadOnly( True )

        self.append_msg( "setReadOnly( True ) -- buttons still change the text, the user can not" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # make some locals for inspection
        local_self                  = self
        local_plain_text_edit       = self.plain_text_edit
        local_document              = self.plain_text_edit.document()
        local_highlighter           = self.highlighter
        local_spell_dict            = self.spell_dict
        wat_inspector.go(
             msg            = "inspect ",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
