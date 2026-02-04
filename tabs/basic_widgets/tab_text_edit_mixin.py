#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which must
# be named tab_....py     among other things

KEY_WORDS:      russ mix in contextMenu
CLASS_NAME:     TextEditMixinTab
WIDGETS:        TextEditMixin
STATUS:         brand new
TAB_TITLE:      TextEditMixinTab / Mixin Experiment
DESCRIPTION:    Experiment with extending a text edit via a Mixin
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/Russ-Experiments"

"""
Some Notes:


"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------------------


import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run
import webbrowser


import wat


from PyQt5.QtWidgets import QApplication, QTextEdit, QMenu
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtCore import QPoint
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import (QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from PyQt5.QtGui import QColor, QPalette, QTextCursor, QTextDocument
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)



import os
import platform


import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header

SCAN_LINES          = 50
MARKER              = ">>"
LOG_LEVEL           = 15


# -------------------------------
class TextEditMixin(  ):
    """
    this demos adding some functionality to
    a qtextEdit
    it is still experimantal so read and try
    documentation probably not up to date
    some code about stuffdb will be removed

    """
    def __init__(self,
                 parent             = None, ):

        self.up_button              = None
        self.dn_button              = None
        self.search_text_widget     = None
        self.last_position          = 0
        self.set_custom_context_menu( self.show_context_menu_1 )

        # --- external optional services
        self.stuffdb                = None
        self.stuffdb_app_global     = None
        self.ext_logger             = None
        self.stuff_text_ext         = None

    #-------------------------------------------
    def set_stuff_db( self, stuffdb ):
        """
        get functions..... from stuffdb for stuffdb integration

        ?? migrate to property  """
        self.stuffdb                = stuffdb

        self.stuffdb_app_global     = stuffdb.app_global
        self.ext_logger             = stuffdb.app_global.logger
        self.stuff_text_ext         = self.stuffdb.get_stuff_text_edit_ext( self )


    def log( self, *, level = LOG_LEVEL, msg ):
        """
        self.log( msg = msg )
        self.log( level = logging.DEBUG, msg = msg  )
        """
        if self.ext_logger:
            #self.ext_logger( msg )
            self.ext_logger.log( level, msg  )
        else:
            print( f"self.log {msg}")

    # beware may be used multiple places
    def keyPressEvent(self, event):
        """
        capture all the key presses
        """
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:

            self.ctrl_f_search_down()
            return
        #super().keyPressEvent( event )
        self.keyPressEvent( event )

    #------------------------------
    def foo(self):
        print("Ctrl+F pressed!")
        self.append("foo() executed!")


    def make_search_widgets( self, ):
        """
        example:
        search_text_widget,  up_button,  dn_button  =  text_edit.make_search_wigets(  )
        """
        widget          = QPushButton( "⇑ Up ⇑")
        self.up_button  = widget
        widget.clicked.connect(  self.search_up  )

        widget          = QPushButton( "⇓ Down ⇓")
        self.dn_button  = widget
        widget.clicked.connect(  self.search_down )

        widget                  = QLineEdit()
        self.search_text_widget = widget

        return self.search_text_widget, self.up_button, self.dn_button

    # ---------------------
    def ctrl_f_search_down( self,   ):
        """
        what it says
        """
        selected_text    = self.capture_selected_text()
        #self.append( f"ctrl_f_search_down {selected_text = }")
        self.search_text_widget.setText( selected_text )


    # ---------------------
    def search_down( self,   ):
        """
        search for text see search up
            case insensitive
        """
        text_edit   = self
        search_text = self.search_text_widget.text()
        if search_text:
            cursor = text_edit.textCursor()
            cursor.setPosition( self.last_position )
            found = text_edit.find( search_text )

            if found:
                self.last_position = text_edit.textCursor().position()
                text_edit.ensureCursorVisible()  # Scroll to the found text

            else:
                # grok code
                self.last_position = 0
                cursor.setPosition(self.last_position)
                text_edit.setTextCursor(cursor)
                text_edit.ensureCursorVisible()  # Optional: Scroll to top if reset

    # ---------------------
    def search_up( self,  ):
        """case insensitive
        for an text edit search for a string
        the line_edit contains the string that is the target
        direction of search is up
        case insensitive
        may need to protect against trying to start beyond end !!
        as user may have deleted some text

        """
        text_edit   = self
        search_text = self.search_text_widget.text()
        if search_text:
            cursor = text_edit.textCursor()
            cursor.setPosition( self.last_position )

            found = text_edit.find( search_text, QTextDocument.FindBackward )

            if found:
                self.last_position = text_edit.textCursor().position()
                text_edit.ensureCursorVisible()  # Scroll to the found text

            else:
                # not found make another try or message ??
                #self.last_position = text_edit.document().characterCount()
                    # ng
                self.last_position = len( text_edit.toPlainText() )
                cursor.setPosition( self.last_position )
                text_edit.setTextCursor(cursor)
                text_edit.ensureCursorVisible()

    #----------------------------
    def fake_context_click( self,   ):
        """
        will this get rid of right click delay
        """
        pos = QPoint(10, 10)
        global_pos      = self.mapToGlobal(pos)
        ev              = QContextMenuEvent(
                             QContextMenuEvent.Mouse, pos, global_pos, )

        # choose one of the below
        # Post it so it's handled like a real user click (delayed)
        QApplication.postEvent( self, ev)
        # next seems to be alterantive to above ??
        # no this really makes a mess bad try
        # self.contextMenuEvent(ev)

    #----------------------------
    def set_custom_context_menu( self, show_context_function ):
        """
        what it says
        need disconnect if you connect more than once
        still may get a one right click delay afer you
        change the connection
        there are way around this ask a chatbot
        """

        try:
            self.customContextMenuRequested.disconnect()
        except TypeError:
            # no previous connection
            pass

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect( show_context_function )

        # Optionally emit once to ensure the connection is live
        # now we get a menu too soon so this is not a fix to one click delay
        #self.customContextMenuRequested.emit( QPoint(0, 0)  )

        # next does not fix the problem either seems to have no effect
        self.fake_context_click()

    # ---------------------------------------
    def show_context_menu_1( self, pos ):
        """
        from chat, refactor please !!
        !! needs extension

        """
        widget      = self
        menu        = QMenu( widget )

        # Add standard actions
        undo_action = menu.addAction("Undo")
        undo_action.triggered.connect(widget.undo)
        menu.addSeparator()

        cut_action = menu.addAction("Cut")
        cut_action.triggered.connect(widget.cut)

        copy_action = menu.addAction("Copy")
        # copy_action.triggered.connect(widget.copy)

        paste_action = menu.addAction("Paste")
        paste_action.triggered.connect( widget.paste )
        #menu.addSeparator()

        # ---- "Smart Paste"
        foo_action = menu.addAction("Smart Paste")
        #foo_action.triggered.connect(self.smart_paste_clipboard )
        menu.addSeparator()

        # ---- "Strip Sel"
        foo_action = menu.addAction("Strip Sel")
        #foo_action.triggered.connect( self.strip_lines_in_selection)
        #menu.addSeparator()

        # ---- "RStrip Sel"
        foo_action = menu.addAction("RStrip Sel")
        #foo_action.triggered.connect( self.strip_eol_lines_in_selection )
        #menu.addSeparator()

        # ---- ""Update Markup""
        foo_action = menu.addAction("Update Markup")
        #foo_action.triggered.connect( self.update_markup )
        menu.addSeparator()

        # ---- "Open Urls"
        foo_action = menu.addAction("Open Urls")
        #foo_action.triggered.connect( self.goto_urls_in_selection )
        menu.addSeparator()

        select_all_action = menu.addAction("Select All")
        select_all_action.triggered.connect(widget.selectAll)

        # ---- >>   go
        menu_action = menu.addAction(">>   go ...")
        menu_action.triggered.connect( self.cmd_exec )
        menu.addSeparator()

        # Enable/disable actions based on context
        cursor = widget.textCursor()
        has_selection   = cursor.hasSelection()
        can_undo        = widget.document().isUndoAvailable()
        can_paste       = QApplication.clipboard().text() != ""

        undo_action.setEnabled(can_undo)
        cut_action.setEnabled(has_selection)
        copy_action.setEnabled(has_selection)
        paste_action.setEnabled(can_paste)
        foo_action.setEnabled(can_paste)

        # Show the context menu
        menu.exec_(widget.mapToGlobal(pos))

    # ---------------------------------------
    def show_context_menu_2( self, pos ):
        """
        big difference from _1 is text in caps

        """
        widget      = self
        menu        = QMenu( widget )

        # Add standard actions
        undo_action = menu.addAction("UNDO")
        undo_action.triggered.connect(widget.undo)
        menu.addSeparator()

        cut_action = menu.addAction("CUT")
        cut_action.triggered.connect(widget.cut)

        copy_action = menu.addAction("COPY")
        # copy_action.triggered.connect(widget.copy)

        paste_action = menu.addAction("PASTE")
        paste_action.triggered.connect( widget.paste )
        #menu.addSeparator()

        # # ---- "Smart Paste"
        # foo_action = menu.addAction("Smart Paste")
        # #foo_action.triggered.connect(self.smart_paste_clipboard )
        # menu.addSeparator()

        # # ---- "Strip Sel"
        # foo_action = menu.addAction("Strip Sel")
        # #foo_action.triggered.connect( self.strip_lines_in_selection)
        # #menu.addSeparator()

        # # ---- "RStrip Sel"
        # foo_action = menu.addAction("RStrip Sel")
        # #foo_action.triggered.connect( self.strip_eol_lines_in_selection )
        # #menu.addSeparator()

        # # ---- ""Update Markup""
        # foo_action = menu.addAction("Update Markup")
        # #foo_action.triggered.connect( self.update_markup )
        # menu.addSeparator()

        # # ---- "Open Urls"
        # foo_action = menu.addAction("Open Urls")
        # #foo_action.triggered.connect( self.goto_urls_in_selection )
        # menu.addSeparator()

        select_all_action = menu.addAction("SELECT ALL")
        select_all_action.triggered.connect(widget.selectAll)

        # # ---- >>   go
        # menu_action = menu.addAction(">>   go ...")
        # menu_action.triggered.connect( self.cmd_exec )
        # menu.addSeparator()

        # Enable/disable actions based on context
        cursor = widget.textCursor()
        has_selection   = cursor.hasSelection()
        can_undo        = widget.document().isUndoAvailable()
        can_paste       = QApplication.clipboard().text() != ""

        undo_action.setEnabled(can_undo)
        cut_action.setEnabled(has_selection)
        copy_action.setEnabled(has_selection)
        paste_action.setEnabled(can_paste)
        # foo_action.setEnabled(can_paste)

        # Show the context menu
        menu.exec_(widget.mapToGlobal(pos))


    def capture_selected_text( self ):
        """Capture the currently highlighted (selected) text
        is this worth a function
        selected_text    = self.capture_selected_text()
        """
        cursor = self.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            print(f"Captured highlighted text: '{selected_text}'")
            # Call your function with the captured text
            #self.foo(selected_text)
        else:
            print("No text is currently highlighted/selected")

        return selected_text

    # ------------------------
    def cmd_exec( self   ):
        """
        execute command parsed out of text

        !! change to use marker
        py
        sh
        url
        shell
        text
        idle
        copy

        """
        text_edit        = self
        # ---- do some parsing
        code_lines       = self.get_snippet_lines( text_edit  )
        debug_msg        = ( code_lines )
        #self.logging( debug_msg )
        self.log(  msg = debug_msg  )
        # logging.debug( debug_msg )
        # self.app_global         = AppGlobal
        #stuff_db_app_global.logger( )

        code_lines       = self.undent_lines(code_lines)
        splits           = code_lines[0].split()
        splits_1         = code_lines[0].split( " ", 1 )
        if len( splits_1 ) > 1:
            arg_1 = splits_1[1].strip()   # ?? follow by remove of nl

        if len( splits) == 0:
            return

        if splits[0] == ">>":
            splits = splits[1:]        # toss the >>

        if splits[0].startswith( ">>" ):
            splits[0]  = splits[0][ 2: ]  # again toss the >>

        cmd         = splits[0].lower()
        cmd_args    = splits[ 1:]

        debug_msg   = ( f"cmd_exec {cmd = } \n {cmd_args = }")
        # need to fic
        #self.logging.log( LOG_LEVEL,  debug_msg, )
        self.log( msg = debug_msg )

        # ---- py
        if   cmd == "py":
            code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
            msg     = " ".join( cmd_args )
            if msg == "":
                msg  = "execute some python code"
            # !! fix me
            # #rint( code )
            # global   EXEC_RUNNER
            # if EXEC_RUNNER is None:
            #     EXEC_RUNNER      = exec_qt.ExecRunner( AppGlobal.q_app  )

            # EXEC_RUNNER.create_window(
            #             code       = code,
            #             a_locals   = locals(),
            #             a_globals  = globals(),
            #             msg        = msg,
            #             autorun    = True )

        elif cmd == "copy":
            #rint( "you need to implement >>idle")
            QApplication.clipboard().setText( " ".join( cmd_args )   )

        # ---- snippet  !! missing from docs ??
        elif cmd == "snippet":
            #rint( "you need to implement >>idle")
            # QApplication.clipboard().setText( " ".join( cmd_args )   )
            code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
            msg     = " ".join( cmd_args )

            QApplication.clipboard().setText( code   )

        # ---- idle and idle file
        elif cmd == "idle":   # want a one line and may line
            msg     = ( "  >>idle in process ................................")
            self.log( msg = msg, )


            self.idle_exe.idle_on_temp_file( code_lines )

        elif cmd == "idle_file":   # want a one line and may line
            file_name     = cmd_args[0]
            self.idle_exe.idle_file( file_name  )
            pass  # debug

        # ---- text
        elif cmd == "text":
            file_name     = cmd_args[0]
            if self.stuffdb_app_global:
                self.stuffdb_app_global.os_open_txt_file( file_name )

        elif cmd == "url":
            filename     = cmd_args[0]
            webbrowser.open( filename, new = 0, autoraise = True )

        # ---- bash
        elif cmd == "bash":
            #rint( f"you need to implement >>shell {code_lines}")
            print(f"need to fix bash{code_lines}" )
            if self.stuff_text_ext:
                TEXT_EDIT_EXT.run_shell( code_lines )

        # ---- shell
        elif cmd == "shell":
            #file_name     = cmd_args[0]  # older change to next t
            file_name     = arg_1
            self.shell_file( file_name )
    \
        # ---- search  !! should not have in this object move to stuff db
        # as a plugin of some source
        elif cmd.startswith( "search" ):
            # msg   = ( "implementing >>search")
            # logging.debug( msg )
            #breakpoint( )
            if  self.stuffdb  is None:
                msg   = ( f"cannot do search as STUFF_DB  = none  ")
                #self.logging.error( msg )
                self.log( msg = msg, )
                # !! put up dialog
                return

            else:
                self.stuffdb_app_global.mdi_management.do_db_search( cmd,  cmd_args )


            #     # msg   = ( f"you need to implement >>search {STUFF_DB  = }  ")
            #     # logging.debug( msg )
            #     new_args =  []  # drop after #
            #     for i_arg in cmd_args:
            #         if i_arg.startswith( "#" ):
            #             break
            #         new_args.append( i_arg )
            #         key_words   = " ".join( new_args )
            #     self.search_stuffdb( cmd,do_db_search
            # " ".join( new_args ))
            #     #STUFF_DB.main_window.search_me( " ".join( new_args ) )  # cmd_args rest of line
            # # = None  # may be monkey patched in
            # #                     # this wold be the app
            # #                     # STUFF_DB.main_window may be what you want
            # #                     # go_active_sub_window_func


        elif cmd == "xxx":
            pass

        else:
            msg   = ( f"{cmd = } \n {cmd_args = }" )
            print( msg )
            #logging.error( msg )
        # next case based on command cmd

    # ------------------------
    def get_snippet_lines( self, do_undent = True  ):
        """
        title is line 0
        often for code
        assume cursor in the body
        but there is a built in find function

        # ---- top of text
        >beginmarker    anything else on line

        >>py this is a title
        print( 1 )
        for ix in range( 10, 15 ):
            print( ix )

        >beginmarker    anything else on line

        # ---- end  of text

        start scanning up:
            stop if hit begin marker or top ( or blank lines?

        now scan down and collect lines ( rstripped, no spaces no \n )

            stop if  n_blank lines
            marker
            or end of text
        """
        lines                   = []
        cursor                  = self.textCursor()
        consective_blank_lines  = 0
        original_position       = cursor.position()
        cursor.movePosition( cursor.StartOfLine )
        prior_start_of_line     = cursor.position()

        # ---- upward scan
        for ix in range( SCAN_LINES ):

            cursor.movePosition( QTextCursor.StartOfLine )
            cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor )
            selected_text = cursor.selectedText()

            selected_text   = selected_text.rstrip()
            if   selected_text == "":
                consective_blank_lines  += 1

            else:
                consective_blank_lines  = 0

            if selected_text.strip().lower().startswith( MARKER ):
                #rint( f"hit the top of marked text {ix =}")
                break # leave curor at begin of marker line

            # lines.append( selected_text  )

            cursor.movePosition( cursor.Up )
            cursor.movePosition( QTextCursor.StartOfLine )
            position       = cursor.position()
            if position == prior_start_of_line:
                debug_msg = ( f"is error !! hit the top of all text {ix =}")
                # self.logging.log( LOG_LEVEL,  debug_msg, )
                self.log( msg = debug_msg, )
                break
            else:
                prior_start_of_line  = position

        # now at top of text
        #rint( f"found the top of  text {ix =}")

        # ---- start down collecting lines
        consective_blank_lines  = 0
        on_top_line             = True
        for ix in range( SCAN_LINES ):
            cursor.movePosition( cursor.EndOfLine, cursor.KeepAnchor )
            selected_text   = cursor.selectedText()
            selected_text   = selected_text.rstrip()

            if   selected_text == "":
                consective_blank_lines  += 1

            else:
                 consective_blank_lines  = 0

            if consective_blank_lines  > 3:
                #msg = f"scan down blank line limit {consective_blank_lines}"
                #rint( msg )
                break

            # hot on firs line down
            if not on_top_line and selected_text.strip().lower().startswith( MARKER ):
                #rint( f"hit the next line of marked text {ix =}")
                break # leave curor at begin of marker line
            else:
                on_top_line = False

            lines.append( selected_text  )

            # Move to the start of the next line 2 steps
            cursor.movePosition(cursor.Down)
            cursor.movePosition(QTextCursor.StartOfLine)
            position       = cursor.position()

            if position == prior_start_of_line:
                #rint( f"hit the end of text {ix =} ")
                break

            else:
                prior_start_of_line  = position

        if do_undent:
            lines   = self.undent_lines( lines )

        return lines


    # ---- statics
    # ------------------------
    def undent_lines( self, lines ):
        """
        static
        ?? perhaps a util
        delete leading spaces ( as per code )
        then return as a multiline string  that is a list of strings
            lines   is a list of lines


        """
        new_lines            = []
        if len( lines ) == 0:
            return new_lines

        num_leading_spaces   = len( lines[0] ) - len( lines[0].lstrip(' ') )
        #rint( f"{num_leading_spaces = }")
        leading_spaces       = " " * num_leading_spaces

        for i_line in lines:
            if i_line.startswith( leading_spaces ):
                i_line   = i_line[ num_leading_spaces : ]
            new_lines.append( i_line )

        return new_lines

    def shell_file( self, file_name ):
        """ """
        if platform.system() == 'Windows':
            os.startfile(file_name)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', file_name))
        else:  # Linux
            subprocess.call(('xdg-open', file_name ) )


# -------------------------------
class MixedTextEdit( QTextEdit, TextEditMixin ):
    """

    """
    def __init__(self,
                 parent                 = None, ):

        # Initialize QTextEdit properly
        QTextEdit.__init__( self, parent )  # Call QTextEdit constructor with parent

#  --------
class TextEditMixinTab( tab_base.TabBase ):
    """
    Reference examples for QPushButton


    this is also the place for documentation on the methods normally found
    in a tab_.... file and should display its naming and other coding conventions
    other tab_xxx files may not be as well commented, you should be familiar with
    the conventions and be able to read the code.
    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4

        self._build_gui()


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
        #text_edit       = QTextEdit()
        text_edit       = MixedTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit

        print( f"{text_edit.minimumSize( ) =} ")
        text_edit.setMinimumHeight( 100 )
        # print(  ia_qt.q_text_edit( text_edit, msg = "QTextEditTab.text_edit" ) )

        ix_row     = 0
        ix_col     = 0
        row_span   = 1
        col_span   = 3

        layout.addWidget( text_edit, ix_row, ix_col, row_span, col_span )  # rowSpan, columnSpan Alignment  # args are
            # widget: The widget you want to add to the grid.
            # row: The row number where the widget should appear (starting from 0).
            # column: The column number where the widget should appear (starting from 0).
            # rowSpan (optional): The number of rows the widget should span (default is 1).
            # columnSpan (optional): The number of columns the widget should span (default is 1).
            # alignment (optional): The ali

        search_text_widget,  up_button,  dn_button  =  text_edit.make_search_widgets(  )

        ix_row     += 1
        ix_col     = 0
        row_span   = 1
        col_span   = 1

        layout.addWidget( search_text_widget, ix_row, ix_col, row_span, col_span )

        #ix_row     += 1
        ix_col     += 1
        row_span   = 1
        col_span   = 1

        layout.addWidget( up_button, ix_row, ix_col, row_span, col_span )

        #ix_row     += 1
        ix_col     += 1
        row_span   = 1
        col_span   = 1

        layout.addWidget( dn_button, ix_row, ix_col, row_span, col_span )

        # # ---- search
        # ix_row     += 1
        # ix_col     = 0
        # row_span   = 1
        # col_span   = 1

        # widget             = QLineEdit()
        # self.line_edit     = widget

        # # ---- see if these are legal
        # #widget.setHeight( 10 )   # ng
        # widget.setText( "Python")
        # # widget.append(  "append a bit" )
        # widget.setReadOnly( False )  # but this is default
        # # too soon to call
        #self.set_custom_context_menu( widget )


        # widget.maximumHeight(…) # maximumHeight(self) -> int
        # widget.maximumSize(…) # maximumSize(self) -> QSize
        # widget.maximumViewportSize(…) # maximumViewportSize(self) -> QSize
        # widget.maximumWidth(  ) # maximumWidth(self) -> int


        # ---- new row
        button_layout = QHBoxLayout( )
        ix_row     += 1
        ix_col      = 0
        col_span    = 2
        layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )


        # # ---- new row
        # button_layout = QHBoxLayout(   )
        # ix_row    += 1
        # layout.addLayout ( button_layout, ix_row, ix_col, row_span,  col_span )

        self.build_gui_last_buttons( button_layout )



    #----------------------------
    def get_button_style_sheet( self ):
        """
        what it says

        when applied to a button changes a bit of its appearance

        this is important content for the widgets referenced on this tab
        """
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """
        # i do not know what the default state, perhaps wat_inspector can tell
    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find ???

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "signal_sent()" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( tab_base.DONE_MSG )

    # ---- connects signals...   --------
    # --------------------------
    def return_pressed( self ):
        """
        what is says  -- not connected, delete?

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "return_pressed()" )

        self.append_msg( tab_base.DONE_MSG )



    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
            these mutations will try to mimic a typical default state
            of a widget for the first push button the
            second will not be modified by mutate_0

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_0()" )
        self.append_msg( "default_context_menu" )
        widget          = self.text_edit


        widget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)


        self.append_msg( tab_base.DONE_MSG )

        return

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_1()" )
        widget          = self.text_edit
        self.append_msg( "context_1 custom in mixed case, first click ignored error " )

        foo     = partial( widget.set_custom_context_menu, widget.show_context_menu_1 )
        widget.set_custom_context_menu( foo )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_2()" )

        widget          = self.text_edit
        self.append_msg( "context_2  custom in CAP case, first click ignored error" )

        foo     = partial( widget.set_custom_context_menu, widget.show_context_menu_2 )
        widget.set_custom_context_menu( foo )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_3()" )

        self.append_msg( "no_context_menu" )

        widget = self.text_edit
        widget.setContextMenuPolicy( QtCore.Qt.NoContextMenu )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "mutate_4()" )


        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them
        self_text_edit    = self.text_edit

        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tab's code

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
