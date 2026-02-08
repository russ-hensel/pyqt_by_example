#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

tab_context_menu.py

KEY_WORDS:      context menu custom right click
CLASS_NAME:     ContextMenuTab
WIDGETS:        QMenu QtCore.Qt.CustomContextMenu
STATUS:         seem fairly complete
TAB_TITLE:      QMenu / as a context menu
DESCRIPTION:    A QMenu as a context menu
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-CustomContextMenu"



# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------------------


import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat

from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtCore import (QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QPalette, QTextCursor, QTextDocument
# sql
from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# widgets biger
# widgets -- small
# layouts
from qtpy.QtWidgets import (QAction,
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

#import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class ContextMenuTab( tab_base.TabBase ):
    """
    Now i have a doc string.


    see
    """
    def __init__(self):
        """
        mostly for buttons
        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        self.mutate_dict[4]     = self.mutate_4
        self.mutate_dict[5]     = self.mutate_5

        self.right_click_menu   = False

        self._build_gui()

    #----------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        """
        layout              = QVBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )



        # ---- new row c
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row button_1 and _2
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- the QTextEdit
        widget       = QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = widget   # later we will need to know this

        row_layout.addWidget( widget,  )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        self.build_gui_last_buttons( button_layout )

    #-------------------------
    def default_context_menu(self, widget ):
        """
        set to use the default contex menu
        """
        self.append_msg( "default_context_menu" )
        widget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    #-------------------------
    def no_context_menu(self, widget ):
        """
        what it says

        """
        self.append_msg( "no_context_menu" )
        # Option 1: Revert to default context menu
        #widget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # Option 2: Disable context menu entirely
        widget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    #----------------------------
    def mouseDoubleClickEvent(self, event ):
        """does not seem to be connected to widget """
        msg    = ("Double-click detected")
        self.append_msg( msg )
        super().mouseDoubleClickEvent(event)

    #----------------------------
    def custom_context_menu( self, widget ):
        """
        what it says
            configure for the custom context widget
        """
        msg    = ("custom_context_menu")
        self.append_msg( msg )
        widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # need to disconnect existing if any
        try:
            self.customContextMenuRequested.disconnect()
        except TypeError:
            # no previous connection
            pass

        widget.customContextMenuRequested.connect(self.show_context_menu)

    #----------------------------
    def foo(self):
            """
            Example function to be called from context menu
            """
            msg   = ("foo action triggered!")
            self.append_msg( msg )

    #----------------------------
    def mousePressEvent( self, event ):
        """
        override the builtin then forward
        by capturing the right click we could
        also capture the event for a context menu
        """
        msg = ("mousePressEvent" )
        self.append_msg( msg )

        if event.button() == Qt.RightButton:
            msg = ("Right-click detected")
            self.append_msg( msg )

            if self.right_click_menu:
                msg = ( f"{self.right_click_menu = }")
                self.append_msg( msg )
                # had trouble getting the right position
                #pos  = event.globalPos()
                #pos  = self.mapToGlobal(event.pos())
                # pos  = self.text_edit.mapToGlobal(event.pos())
                # pos  = event.pos()
                pos = self.text_edit.mapFrom(self, event.pos())

                self.show_context_menu( pos )

        elif event.button() == Qt.LeftButton:
            msg = ("Left-click detected")
            self.append_msg( msg )

        msg = ("continue to default in ancestor super....")
        self.append_msg( msg )

        super().mousePressEvent(event)  # continue to default behavior

    #----------------------------
    def show_context_menu( self, pos):
        """
        actually show the menu

        """
        self.append_msg( "begin show_context_menu" )

        widget = self.text_edit
        menu   = QMenu( widget )   # maybe widget ??

        # Add standard actions
        undo_action = menu.addAction("UN-DOO")
        undo_action.triggered.connect(widget.undo)
        menu.addSeparator()

        cut_action = menu.addAction("CUT")
        cut_action.triggered.connect(widget.cut)
        copy_action = menu.addAction("COPY")
        copy_action.triggered.connect(widget.copy)
        paste_action = menu.addAction("PASTE")
        paste_action.triggered.connect(widget.paste)
        menu.addSeparator()

        # Add custom action
        foo_action = menu.addAction("Foo")
        foo_action.triggered.connect(self.foo)


        export_submenu = menu.addMenu("Export As...")

        # Add actions to the submenu
        pdf_action   = export_submenu.addAction("Export to PDF")
        csv_action   = export_submenu.addAction("Export to CSV")
        json_action  = export_submenu.addAction("Export to JSON")




        # Enable/disable actions based on context
        cursor = widget.textCursor()
        has_selection = cursor.hasSelection()
        can_undo = widget.document().isUndoAvailable()
        can_paste = QApplication.clipboard().text() != ""

        undo_action.setEnabled(can_undo)
        cut_action.setEnabled(has_selection)
        copy_action.setEnabled(has_selection)
        paste_action.setEnabled(can_paste)

        # Show the context menu
        menu.exec_(widget.mapToGlobal(pos))

    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find
        """
        self.append_function_msg( "signal_sent" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def put_in_clipboard( self, a_string ):
        """
        what it says:
        """
        self.append_function_msg( "put_in_clipboard" )

        clipboard = QApplication.clipboard()

        # Set a string into the clipboard
        clipboard.setText( a_string )
        self.append_msg(  f"put_in_clipboard { a_string = }" )

        get_text_out   =   clipboard.text()

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        widget    = self.text_edit
        self.default_context_menu( widget )

        self.right_click_menu   = False
        msg                     = f"{self.right_click_menu = }"
        self.append_msg( msg, )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        widget    = self.text_edit

        self.no_context_menu( widget )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2" )

        self.custom_context_menu( self.text_edit )

        self.right_click_menu       = False
        self.append_msg( f"{self.right_click_menu = }", )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_3" )

        self.no_context_menu( self.text_edit )

        self.right_click_menu       = True
        msg                         = f"{self.right_click_menu = }"
        self.append_msg( msg, )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_4" )

        self.right_click_menu       = False
        msg                         = f"{self.right_click_menu = }"
        self.append_msg( msg, )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_5( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_5" )

        self.right_click_menu       = True
        msg                         = f"{self.right_click_menu = }"
        self.append_msg( msg, )

        self.custom_context_menu( self.text_edit )
        self.append_msg( tab_base.DONE_MSG )

    # ---- connects -----------------------
    # --------------------------
    def return_pressed( self ):
        """
        what is says
        """
        self.append_msg( "return_pressed" )

        self.append_msg( "\n" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        self_text_edit          = self.text_edit

        wat_inspector.go(
             msg            = "variables for inspection ",
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



