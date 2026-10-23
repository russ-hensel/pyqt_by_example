#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
KEY_WORDS:      spell check, spelling, enchant, QSyntaxHighlighter, squiggle underline, suggestions, rich text edit
CLASS_NAME:     QTextEditSpellTab
WIDGETS:        QTextEdit QSyntaxHighlighter
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      QTextEdit / Spell Check
DESCRIPTION:    QTextEdit with local spell checking, pyenchant + QSyntaxHighlighter
HOW_COMPLETE:   20  #  AND A COMMENT

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QTextEdit"

"""
scratch

    spell check, the short version:
        Qt has no spell check, so:
        a QSyntaxHighlighter on widget.document() draws the red squiggle,
            display only, the text, undo stack and toHtml() are not touched
        pyenchant ( uv pip install pyenchant ) does the checking, uses the
            system libenchant and its aspell / hunspell dictionaries, all local
        right click on a flagged word for suggestions, built on
            createStandardContextMenu( pos )
        same code as tab_q_plain_text_edit_spell.py, kept separate so
            each example can be copied on its own
        a document can have only one QSyntaxHighlighter

    rich text notes:
        the squiggle is merged over the existing format, bold stays bold
        a replaced word takes the format of the word it replaces
        createStandardContextMenu( pos ) adds Copy Link Location over a link

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
# sql

from qtpy.QtWidgets import (QAction,
                             QApplication,
                             QGridLayout,
                             QHBoxLayout,
                             QLineEdit,
                             QMenu,
                             QPushButton,
                             QTextEdit)

#import parameters

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
# INDENT          = uft.BEGIN_MARK_1
# INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.
SPELL_LANG      = "en_US"

# letters, with inner apostrophes so don't and you’re are one word
# [^\W\d_] is "a letter" in any language
WORD_RE         = re.compile( r"[^\W\d_]+(?:['’][^\W\d_]+)*" )


# ----------------------------------------
class SpellHighlighter( QSyntaxHighlighter ):
    """
    underline misspelled words in a QTextDocument
    works for QPlainTextEdit and QTextEdit, pass it widget.document()
    highlightBlock() is called by Qt one block ( paragraph ) at a time,
    only for blocks that changed
    the format is merged over the rich text format, so bold stays bold
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
        text is plain, an image in the block shows up as \\ufffc
        which WORD_RE skips
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
class QTextEditSpellTab( tab_base.TabBase ) :
    def __init__(self):
        """
        the usual
        tab_q_text_edit_spell.py
        """
        super().__init__()
        self.module_file        = __file__

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        # State variable to track search position
        self.last_position = 0
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
        # button_layout        = QHBoxLayout(   )

        # ---- the QTextEdit
        text_edit       = QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit

        print( f"{text_edit.minimumSize( ) =} ")
        text_edit.setMinimumHeight( 100 )
        # print(  ia_qt.q_text_edit( text_edit, msg = "QTextEditTab.text_edit" ) )

        ix_row     = 0
        ix_col     = 0
        row_span   = 1
        col_span   = 1

        layout.addWidget( text_edit, ix_row, ix_col, row_span, col_span )  # rowSpan, columnSpan Alignment  # args are
            # widget: The widget you want to add to the grid.
            # row: The row number where the widget should appear (starting from 0).
            # column: The column number where the widget should appear (starting from 0).
            # rowSpan (optional): The number of rows the widget should span (default is 1).
            # columnSpan (optional): The number of columns the widget should span (default is 1).
            # alignment (optional): The ali

        # ----- search
        ix_row     += 1
        ix_col     = 0
        row_span   = 1
        col_span   = 1

        widget             = QLineEdit()
        self.line_edit     = widget

        # ---- see if these are legal
        #widget.setHeight( 10 )   # ng
        widget.setText( "Python")
        # widget.append(  "append a bit" )
        widget.setReadOnly( False )  # but this is default
        # too soon to call
        #self.set_custom_context_menu( widget )
        chat = """
Font Settings:

    setFont(QFont): Sets the default font for the editor.
    setFontPointSize(float): Sets the font size.
    setFontFamily(str): Sets the font family.

Color Settings:

    setTextColor(QColor): Sets the text color.
    setTextBackgroundColor(QColor): Sets the background color of the text.
    setPalette(QPalette): Adjusts the editor's color palette.

Alignment:

    setAlignment(Qt.AlignmentFlag): Aligns the text (e.g., Qt.AlignLeft, Qt.AlignRight).

Read-Only Mode:

    setReadOnly(bool): Makes the editor read-only (e.g., for displaying text only).

Line Wrapping:

    setLineWrapMode(QTextEdit.LineWrapMode): Controls text wrapping.
        Options: NoWrap, WidgetWidth, etc.
    setWordWrapMode(QTextOption.WrapMode): Adjusts word wrapping behavior.

Cursor Control:

    setTextCursor(QTextCursor): Sets the current text cursor.
    textCursor(): Retrieves the current cursor.
    moveCursor(QTextCursor.MoveOperation): Moves the cursor (e.g., QTextCursor.Start, QTextCursor.End).

Scrollbars:

    setVerticalScrollBarPolicy(Qt.ScrollBarPolicy): Controls vertical scrollbar visibility (e.g., Qt.ScrollBarAlwaysOn).
    setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy): Controls horizontal scrollbar visibility.

Undo/Redo:

    setUndoRedoEnabled(bool): Enables or disables undo/redo.
    undo(): Undoes the last action.
    redo(): Redoes the last undone action.
"""


        # widget.maximumHeight(…) # maximumHeight(self) -> int
        # widget.maximumSize(…) # maximumSize(self) -> QSize
        # widget.maximumViewportSize(…) # maximumViewportSize(self) -> QSize
        widget.maximumWidth(  ) # maximumWidth(self) -> int

        widget.setPlaceholderText( "Enter search text" )
        layout.addWidget( widget, ix_row, ix_col, row_span,  col_span )

        #ix_row     += 1
        ix_col     += 1
        row_span   = 1
        col_span   = 1
        widget           = QPushButton( "Down" )
        self.down_button = widget
        widget.clicked.connect(self.search_down)
        layout.addWidget( widget, ix_row, ix_col, row_span,  col_span )

        ix_col     += 1
        widget           = QPushButton("Up")
        self.up_button   = widget
        widget.clicked.connect( self.search_up )
        layout.addWidget( widget, ix_row, ix_col, row_span,  col_span )

        # ---- lower buttons
        ix_row     += 1
        ix_col     = 0
        row_span   = 1
        col_span   = 1
        button_layout = QHBoxLayout(   )
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )
            # if you have row_span you need col_span, only positional

        # ---- PB set_text\n_ver_1
        widget = QPushButton( "set_text\n_ver_1" )
        widget.clicked.connect(  self.set_text_ver_1 )
        #widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        # ---- PB set_text\n_ver_2
        widget = QPushButton( "set_text\n_ver_2" )
        widget.clicked.connect(  self.set_text_ver_2 )
        #widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        widget = QPushButton("insert_text\n")
        widget.clicked.connect( self.insert_text  )
        button_layout.addWidget( widget,  )

        # ---- PB clear_text
        widget = QPushButton("clear\n_text")
        widget.clicked.connect( self.clear_text )
        button_layout.addWidget( widget,   )

         # ---- PB copy_all_text
        widget = QPushButton( "copy_all\n_text" )
        widget.clicked.connect( self.copy_all_text  )
        button_layout.addWidget( widget,   )
        # ---- "copy_line_of_text\n"
        widget = QPushButton( "copy_line_of_text\n" )
        widget.clicked.connect(lambda: self.copy_line_of_text( text_edit ))
        button_layout.addWidget( widget,   )

        # ---- "copy_n_lines\n_of_text"
        widget = QPushButton( "copy_n_lines\n_of_text" )
        widget.clicked.connect(lambda: self.copy_n_lines_of_text( text_edit, 5 ))
        button_layout.addWidget( widget,   )

        # ---- PB
        widget = QPushButton("copy_selected\n_text")
        widget.clicked.connect( self.copy_selected_text )
        button_layout.addWidget( widget,   )

        # ---- new row
        button_layout = QHBoxLayout( )
        ix_row    += 1
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        # ---- PB
        widget = QPushButton( "cursor_to_begin" )
        widget.clicked.connect( self.cursor_to_begin )
        button_layout.addWidget( widget, )

        # ---- PB
        widget = QPushButton( "cursor_to_end" )
        widget.clicked.connect( self.cursor_to_end )
        button_layout.addWidget( widget, )

        # ---- new row, spell check
        button_layout = QHBoxLayout( )
        ix_row    += 1
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        # ---- PB set_misspelled_text
        widget = QPushButton( "set_misspelled\n_text" )
        widget.clicked.connect( self.set_misspelled_text )
        button_layout.addWidget( widget, )

        # ---- PB set_misspelled_html
        widget = QPushButton( "set_misspelled\n_html" )
        widget.clicked.connect( self.set_misspelled_html )
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

        # ---- PB show_html
        widget = QPushButton( "show\n_html" )
        widget.clicked.connect( self.show_html )
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


        # # ---- mutate
        # widget = QPushButton("mutate\n")
        # self.button_ex_1         = widget
        # widget.clicked.connect( lambda: self.mutate( ) )
        # button_layout.addWidget( widget )

        # # ---- PB inspect
        # widget = QPushButton("inspect\n")
        # widget.clicked.connect( self.inspect    )
        # button_layout.addWidget( widget,   )

        # # ---- PB breakpoint
        # widget = QPushButton("breakpoint\n")
        # widget.clicked.connect( self.breakpoint    )
        # button_layout.addWidget( widget,   )

    # ---------------  end of button actions and class
    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        !! we may phase out for print_string  or the reverse ??
             make one call the other
        print to message area, with scrolling and
        log if we are configured for it

        parameters.gui_text_log_fn    = False  # "gui_text.log"
                                               # a file name or something false


        parameters.log_gui_text       = False # True or false to log text
        parameters.log_gui_text_level = 10    # logging level for above

        !! add parameter clear_msg = True or false

        """

        self.append_function_msg( "display_string" )

        self.append_msg(  f"in display_string, with a_string = {a_string}")
        # return
        #   try  !!!  QTextEdit.clear()
        cursor = self.text_edit.textCursor()
        # cursor.movePosition( QTextCursor::End )
        cursor.insertText( a_string )

        self.append_msg( "display_string done" )

    #  --------
    def print_message(self, text):
        """
        what is says
        """
        self.append_function_msg( "print_message" )
        self.append_msg( "Button clicked: " + text )
        self.append_msg( "print_message done" )

    # ---- spell check
    # ---------------------------------------
    def setup_spell_check( self ):
        """
        make the dictionary and attach the highlighter to the document
        if the language is missing the tab still runs,
        just with no spell check
        the context menu is set by mutate_0, which _build_gui runs
        """
        self.spell_dict     = None
        if enchant is None:
            self.append_msg( "!! pyenchant not installed, no spell check  "
                             "( uv pip install pyenchant )" )
        else:
            try:
                self.spell_dict     = enchant.Dict( SPELL_LANG )
            except enchant.errors.DictNotFoundError:
                self.append_msg( f"!! no enchant dictionary for {SPELL_LANG}, "
                                 f"have: {enchant.list_languages()}" )

        widget              = self.text_edit
        self.highlighter    = SpellHighlighter( widget.document(), self.spell_dict )

        # an editable QTextEdit does not have LinksAccessibleByMouse, and without
        # it createStandardContextMenu( pos ) leaves out Copy Link Location
        Flag                = QtCore.Qt.TextInteractionFlag
        widget.setTextInteractionFlags( Flag.TextEditorInteraction
                                      | Flag.LinksAccessibleByMouse )

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

        widget          = self.text_edit
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
            # a selection replaces it, one undo step, and keeps the
            # format ( bold ... ) of the word it replaces
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
        self.context_widget   = widget # for later use in menu
        self.connect_context_menu( widget, self.show_context_menu )

    # ---------------------------------------
    def show_spell_context_menu( self, pos ):
        """
        createStandardContextMenu( pos ) gives the usual Undo, Cut ... menu,
        with pos it also adds Copy Link Location when over a link
        ( needs LinksAccessibleByMouse, see setup_spell_check )
        its pos is in document coordinates, ours is viewport, so add the scroll
        it is ours to delete, so deleteLater() after exec()
        """
        widget      = self.text_edit
        doc_pos     = pos + QtCore.QPoint( widget.horizontalScrollBar().value(),
                                           widget.verticalScrollBar().value() )
        menu        = widget.createStandardContextMenu( doc_pos )
        self.add_spell_actions( menu, pos )

        menu.exec( widget.mapToGlobal( pos ) )
        menu.deleteLater()


    # ---------------------------------------
    def show_context_menu( self, pos ):
        """
        from chat, refactor please !!
        !! needs extension

        """
        widget      = self.context_widget
        menu        = QMenu( widget )

        # Add standard actions
        undo_action = menu.addAction("Undo")
        undo_action.triggered.connect(widget.undo)
        menu.addSeparator()

        cut_action = menu.addAction("Cut")
        cut_action.triggered.connect(widget.cut)
        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect(widget.copy)

        paste_action = menu.addAction("Paste")
        paste_action.triggered.connect(widget.paste)
        #menu.addSeparator()

        # ---- "Smart Paste"
        foo_action = menu.addAction("non-standard")
        #foo_action.triggered.connect(self.smart_paste_clipboard )
        menu.addSeparator()


        select_all_action = menu.addAction("Select All")
        select_all_action.triggered.connect(widget.selectAll)

        # ---- >>   go
        menu_action = menu.addAction("non_standard_2")
        #menu_action.triggered.connect( self.cmd_exec )
        menu.addSeparator()


        # Enable/disable actions based on context
        cursor          = widget.textCursor()
        has_selection   = cursor.hasSelection()
        can_undo        = widget.document().isUndoAvailable()
        can_paste       = QApplication.clipboard().text() != ""

        undo_action.setEnabled(can_undo)
        cut_action.setEnabled(has_selection)
        copy_action.setEnabled(has_selection)
        paste_action.setEnabled(can_paste)
        foo_action.setEnabled(can_paste)

        self.add_spell_actions( menu, pos )

        # Show the context menu
        menu.exec_(widget.mapToGlobal(pos))
        menu.deleteLater()

    #  --------
    def clear_text( self ):
        """
        """
        self.append_function_msg( "clear_text()" )

        self.text_edit.clear()
        self.append_msg( "clear_text done" )

    #  --------
    def copy_text(self, text_edit):
        """
        what is says
        """
        self.append_function_msg( "copy_text" )

        self.append_msg( "QTextEditTab.copy_text"   )
        selected_text      = text_edit.toPlainText()
        QApplication.clipboard().setText(selected_text)
        self.append_msg(  f" copy_text -> {selected_text }" )
        self.append_msg( "copy_text done" )

    #  --------
    def copy_all_text( self, text_edit ):
        """
        what it says
        """
        self.append_function_msg( "copy_all_text()" )

        # text_edit not used
        all_text = self.text_edit.toPlainText()
        self.append_msg( f"{all_text = }")

        self.copy_all_text_b( None )

        self.append_msg( tab_base.DONE_MSG )

    #  --------
    def copy_all_text_b( self, text_edit ):
        """
        what it says
        """
        self.append_function_msg( "copy_all_text_b" )

        text_edit   = self.text_edit

        all_text = text_edit.toPlainText()
        self.append_msg( f"text_edit.toPlainText()  {all_text}" )

        # Save current cursor position
        cursor      = text_edit.textCursor()
        original_position = cursor.position()

        # Select all text and copy to the clipboard
        text_edit.selectAll()
        text_edit.copy()   # think goes to clipboard

        all_text = self.text_edit.toPlainText()

        # Restore cursor to its original position
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)

        self.append_msg( "all text copied to clipboard" )

        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def cursor_to_begin(self,  ):
        """
        what it says, read

        and scroll if necessary to make visible
        begin = top = start
        """
        self.append_function_msg( "cursor_to_begin()" )

        text_edit   = self.text_edit

        cursor      = text_edit.textCursor()
        cursor.movePosition(cursor.Start)
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()

        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def cursor_to_end(self,  ):
        """
        what it says, read

        and scroll if necessary to make visible
        end = bottom = end
        """
        self.append_function_msg( "cursor_to_end()" )

        text_edit   = self.text_edit
         # ---------------- scroll to bottom
        cursor = text_edit.textCursor()
        cursor.movePosition(cursor.End)
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()

        self.append_msg( tab_base.DONE_MSG )


    # ----
    def set_text_ver_1(self,  ):
        """
        what is says
        """
        text_edit   = self.text_edit
        self.append_function_msg( "set_text_ver_1" )

        a_string    = 1 * (

        """
More than 20 years have passed since I authored the Python Essential Reference. At that time,
Python was a much smaller language and it came with a useful set of batteries in its
standard library. It was something that could mostly fit in your brain. The Essential Reference
reflected that era. It was a small book that you could take with you to write some Python
code on a desert island or inside a secret vault. Over the three subsequent revisions, the
Essential Reference stuck with this vision of being a compact but complete language
reference—because if you’re going to code in Python on vacation, why not use all of it?

Python Distilled David M. Beazley
        """ )

        text_edit.setText( a_string )
        #self.text
        self.append_msg( tab_base.DONE_MSG )

    #---------------
    def set_text_ver_2(self,  ):
        """
        what is says
        """
        self.append_function_msg( "set_text_ver_2" )

        a_string    = 22  * (

        """
        HOMEXCEL Sponges Kitchen 24pcs, Non-Scratch Scrub Dish Sponges,
        Safe on Non-Stick Cookware,Dual Sided Cleaning Sponges
        for Kitchen,Household,Bathroom and More

        """ )
        self.text_edit.setText( a_string )

        self.append_msg( "set_text_ver_2 done" )
        self.append_msg( tab_base.DONE_MSG )

    #-------------------
    def delete_text(self, text_edit):
        """
        """
        self.append_function_msg( "delete_text" )

        text_edit.clear()

        self.append_msg( tab_base.DONE_MSG )

    #--------
    def insert_text( self, ):
        """
        insert text at the cursor position
        """
        self.append_function_msg( "insert_text" )

        a_string  = ( """>>---- so here is a bit
of text the we will
           ------------------> insert
at the cursor ----<<""")

        text_edit       = self.text_edit
        cursor          = text_edit.textCursor()
        cursor.insertText( a_string )
        self.append_msg( tab_base.DONE_MSG )

    #----------------------------
    def copy_selected_text(self,  ):
        """
        """
        self.append_function_msg( "copy_selected_text" )

        text_edit       = self.text_edit
        selected_text   = text_edit.textCursor().selectedText()
        QApplication.clipboard().setText( selected_text )

        # to paste get the text with QApplication.clipboard().text()
        #clipboard = QApplication.clipboard()

        self.append_msg(  f"   -> {selected_text = } now in clipboard" )
        self.append_msg( tab_base.DONE_MSG )

    #----------------------
    def copy_n_lines_of_text(self, text_edit, num_lines ):
        """
        copy some number of lines of text to clipboard
        starting at the cursor line, walking the QTextBlock s
        ( a block is a paragraph, a "line" ending in \\n )
        no cursor moving at all
        the old way moved a cursor Down with a selection still
        anchored, which gave part lines and empty strings
        """
        self.append_function_msg( "copy_n_lines_of_text" )

        block   = text_edit.textCursor().block()
        lines   = []
        for ix in range( num_lines ):
            if not block.isValid():
                break
            lines.append( block.text() )
            block   = block.next()

        QApplication.clipboard().setText( "\n".join( lines ) )

        # append_msg( msg, clear ) -- a second arg here would clear the messages
        self.append_msg( f"Next {num_lines} lines:" )
        for ix, i_line in enumerate( lines ):
            self.append_msg( f"{INDENT}{ix} >>{i_line}<<" )
        self.append_msg( tab_base.DONE_MSG )
        return lines

    #----------------------
    def copy_line_of_text(self, arg ):
        """
        chat:
        With a QTextWidge holding some text:
        from the cursor position copy the text from the
        beginning of the line to the end of the line.

        the block way, the whole paragraph, no cursor moving
        StartOfLine / EndOfLine are the visual line, so with
        wrap on they gave just the wrapped piece
        """
        self.append_function_msg( "copy_line_of_text" )

        cursor          = self.text_edit.textCursor()
        selected_text   = cursor.block().text()

        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

        self.append_msg( f"Copied text: {selected_text = }")
        self.append_msg( tab_base.DONE_MSG )

    # ---- spell check buttons
    # --------------------
    def set_misspelled_text( self, ):
        """
        some plain text with mistakes, right click the red ones
        """
        self.append_function_msg( "set_misspelled_text()" )

        a_string    = (
"""Teh quick brown fox jumpd over the lazzy dog.
Spell checking in Qt is not built in, so we recieve a litle help
from enchant, which uses the same dictionarys as LibreOffice.
Words with apostrophes: don't, can't, you’re, it's, are all fine.
Numbers like 1234 and mixed things like abc123 are skipped or split.
HOMEXCEL and other ALLCAPS words get flagged too.""" )

        self.text_edit.setPlainText( a_string )
        self.append_msg( tab_base.DONE_MSG )

    # --------------------
    def set_misspelled_html( self, ):
        """
        rich text with mistakes, the squiggle goes over bold, italic, color
        pick a suggestion and the new word keeps the format
        """
        self.append_function_msg( "set_misspelled_html()" )

        a_string    = (
"""<h3>Rich text with misteaks</h3>
<p>This word is <b>bolld</b>, this one is <i>itallic</i>,
and this one is <span style="color:blue">bluue</span>.</p>
<p>A <a href="https://www.riverbankcomputing.com">linkk to Riverbank</a>,
right click the link for Copy Link Location.</p>
<ul><li>a list itemm</li><li>another <u>underlind</u> one</li></ul>
<table border="1"><tr><td>tabel cell</td><td>fine cell</td></tr></table>""" )

        self.text_edit.setHtml( a_string )
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
        the highlighter uses, table cells and list items are blocks too
        """
        self.append_function_msg( "list_misspelled()" )

        if self.spell_dict is None:
            self.append_msg( "no spell check dictionary" )
            return

        highlighter     = self.highlighter
        block           = self.text_edit.document().firstBlock()
        count           = 0
        while block.isValid():
            for i_match in WORD_RE.finditer( block.text() ):
                word    = i_match.group()
                if not highlighter.check( word ):
                    count  += 1
                    self.append_msg( f"{INDENT}block {block.blockNumber() + 1:3} "
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

        widget          = self.text_edit
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
    def show_html( self, ):
        """
        toHtml() has no trace of the squiggles, they are display only
        """
        self.append_function_msg( "show_html()" )

        html        = self.text_edit.toHtml()
        body        = html[ html.find( "<body" ): ]
        self.append_msg( f"{'SpellCheckUnderline' in html = }  "
                         f"{'wave' in html = }" )
        self.append_msg( body[ :1500 ] )
        self.append_msg( tab_base.DONE_MSG )

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
    def search_down(self):
        """
        think i want no print for this
        search from current cursor down in text field
        """
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(self.last_position)
            found = self.text_edit.find(search_text)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if end is reached and no match
                self.last_position = 0

        self.append_msg( tab_base.DONE_MSG )
    # ---------------------
    def search_up(self):
        """
        think i want no print for this
        search from current cursor up in text field
        """
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition( self.last_position )
            # Use QTextDocument.FindBackward for backward search
            found = self.text_edit.find(search_text, QTextDocument.FindBackward)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if start is reached and no match
                self.last_position = self.text_edit.document().characterCount()

    # ---------------------
    def inspect_widget(self,  ):
        """
        in a QTextEdit how do i find the position of the cursor
        move the cursor to some position, move the cursor to the top, or bottom
        """
        self.append_function_msg( "inspect" )

        print( "\n >>>> inspect_widget.inspect_widget  -- to do "   )
        print( "some cursor stuff in copy__")
        # print( f"copy_all_text {self.copy_all_text( self.text_edit )}" )
        self.append_msg( tab_base.DONE_MSG )

    #------------------
    def change_widget(self, text_edit ):
        """
        in a QTextEdit how do i find the position of the cursor
        move the cursor to some positext_edit.show()tion, move the cursor to the top, or bottom

        # Move the cursor by 5 characters while keeping the selection
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 5)

        # Apply the modified cursor to the QTextEdit to reflect the selection
        text_edit.setTextCursor(cursor)
        """
        self.append_function_msg( "change_widget" )

        self.append_msg( "\n>>>>change_widget   -- to do "   )
        self.append_msg( "some cursor stuff in copy__")

        # Ensure that the cursor is visible and the widget scrolls to it
        text_edit.ensureCursorVisible()

        cursor = text_edit.textCursor()
        cursor.setPosition(10)  # Moves the cursor to position 10 in the text
        text_edit.setTextCursor(cursor)
        # Move the cursor by 5 characters while keeping the selection
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 5)
        # Apply the modified cursor to the QTextEdit to reflect the selection
        text_edit.setTextCursor(cursor)
        text_edit.show()
        # time.sleep( 1 )

        # cursor = text_edit.textCursor()
        # cursor.movePosition(QTextCursor.Start)   # .End
        # text_edit.setTextCursor(cursor)
        # time.sleep( 1 )

        # print( "cursor to end ")
        # cursor = text_edit.textCursor()
        # cursor.movePosition(QTextCursor.End)   # .End
        # text_edit.setTextCursor(cursor)

        # # Move cursor to position 100
        # cursor = text_edit.textCursor()
        # cursor.setPosition(100)
        # text_edit.setTextCursor(cursor)

        self.append_msg( "\n>>>>change_widget   -- to do "   )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        widget  = self.text_edit
        self.set_spell_context_menu( widget )


        widget.setReadOnly( False )  # but this is default
        # msg    = "so far not implemented "
        # self.append_msg( msg )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )

        # ----
        widget  = self.text_edit
        self.set_custom_context_menu( widget )

        # ----
        msg    = "all lines convertet to a list"
        self.append_msg( msg, )
        all_text    = widget.toPlainText()
        lines       = all_text.split('\u2029')
        if len( lines )  > 0 :
            for ix, i_line in enumerate( lines ):
                if ix < 10:
                    self.append_msg( f"{ix} >>{i_line}<<" )
                else:
                    self.append_msg( "skipping additional lines " )

        else:
            self.append_msg( "no lines to print")

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )

        msg    = "change context menu"
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # make some locals for inspection
        local_self            = self
        #parent_window = self.parent( ).parent( ).parent().parent()
        local_self_text_edit  = self.text_edit
        local_document        = self.text_edit.document()
        local_highlighter     = self.highlighter
        local_spell_dict      = self.spell_dict
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