#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which should
# be named xxxxTab.py     among other things

KEY_WORDS:      pressed press PushBtton click connect rsh pushbutton
CLASS_NAME:     QPushButtonTab
WIDGETS:        QPushButton
STATUS:         June 2025 ok: but more content would be nice
TAB_TITLE:      QPushButton / Reference
DESCRIPTION:    A reference for the QPushButton widget
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QPushButtons"

"""
Some Notes:

Home · russ-hensel/qt5_by_example Wiki
https://github.com/russ-hensel/qt5_by_example/wiki


What We Know About QPushButtons · russ-hensel/qt5_by_example Wiki
https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QPushButtons


"""
# next lets us launch the app from the file
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

import wat
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
class QPushButtonTab( tab_base.TabBase ):
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
        self.mutate_dict[4]     = self.mutate_4

        self._build_gui()

    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        this is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        # ---- new row c
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row button_1 and _2 ....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # a label that points to q_pbutton_1
        widget          = QLabel( "q_pbutton_1 -> ", alignment=Qt.AlignRight)
            # no instance variable as we will not use after __init__

        # layout ( add to the windows ) the widget
        row_layout.addWidget( widget )

        # we use a local variable because it reduces the amount of code
        # and does not run any slower
        # we use this local variable idea in many places
        # because we will refer to the bu
        widget              = QPushButton( "q_pbutton_1" )
        self.q_push_button_1    = widget

            # save a reference for later use
        # this function will be called when the button is clicked
        # the code is a little indirect, do on one line if you wish
        connect_to          = self.pb_1_clicked
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        widget              = QLabel("q_pbutton_2 -> ", alignment=Qt.AlignRight)
        row_layout.addWidget( widget )

        widget              = QPushButton( "q_pbutton_2" )
        self.q_push_button_2    = widget
        connect_to          = self.pb_2_clicked
        widget.clicked.connect( connect_to    )
        row_layout.addWidget( widget,  )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
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
    def pb_1_clicked( self ):
        """
        What it says

            this function may be connected to a button normally
            q_push_button_1

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "pb_1_clicked()" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def pb_2_clicked( self ):
        """
        What it says

            this function may be connected to a button normally
            q_push_button_1

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "pb_2_clicked()" )

        self.append_msg( tab_base.DONE_MSG  )

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

        # ---- change widget
        msg    = "for q_push_button_1 we more or less reset it"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        widget          = self.q_push_button_1
        widget.setText( "text set in mutate_0()" )
        widget.width     = 300
        widget.setToolTip( None )
        widget.setStyleSheet( "" )

        # ---- change widget
        msg    = "for q_push_button_2 no mutations"
        self.append_msg( msg, )

        widget          = self.q_push_button_2
        # self.q_push_button_1.setDisabled( True )
        # self.q_push_button_2.setDisabled( False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_1()" )
        # msg    = "begin implementation"
        # self.append_msg( msg, clear     = False )
        # for self.q_push_button_1

        msg    = "mess with q_push_button_1"
        self.append_msg( msg, )

        widget        = self.q_push_button_1
            # it is often convenient to use a local variable,
            # you will see this a lot in our code, it does not seem to
            # be typical but we think it should be

        msg    = "q_push_button_1 set a tooltip"
        self.append_msg( msg, )

        widget.setToolTip( "this is a tool tip" )
        widget.setText( "text set in \nmutate_1()" )
            # note \n
        widget.width     = 200

        # ---- change widget
        msg    = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        # ---- self.q_push_button_2
        widget        = self.q_push_button_2
        # msg    = "setChecked(True )"
        # self.append_msg( msg, )


        # msg        = f"{self.q_push_button_1.isChecked() = } "
        # self.append_msg( msg, )


        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_2()" )

        msg    = "change some attributes..."
        self.append_msg( msg,  )


        widget     = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setVisible( False )

        msg    = "q_push_button_1 mess with checkable enabled..."
        self.append_msg( msg,  )

        self.q_push_button_1.setCheckable( True )
        self.q_push_button_1.setChecked( True )
        self.q_push_button_1.setDisabled( True )

        self.q_push_button_1.setVisible( True )

        # next does not seem to work
        self.q_push_button_1.setCheckable( True )

        # ---- change widget
        msg    = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        widget     = self.q_push_button_2
        widget.setCheckable( True )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_3()" )

        msg    = "re-enable some stuff -- change attributes"
        self.append_msg( msg, clear = False )

        # ---- first widget
        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setDisabled( False )
        self.q_push_button_1.setVisible( True )
        self.q_push_button_1.setCheckable( True )
        self.q_push_button_1.toggle()

        msg    = "add menu to q_push_button_1"
        self.append_msg( msg, clear = False )

        menu                = QMenu(self)
        menu.addAction("Option 1")
        menu.addAction("Option 2")
        widget.setMenu( menu )

        # ---- change widget
        widget      = self.q_push_button_2
        msg         = "\nsome changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        msg    = "q_push_button_2 mess with style sheet... hover ... color "
        self.append_msg( msg,  )

        widget.setCheckable( False )
        widget.setStyleSheet( self.get_button_style_sheet() )
        msg     = f"get style sheet from widget \n {widget.styleSheet()}"
        self.append_msg( msg,  )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "mutate_4()" )

        msg    = "undo many of earlier mutations"
        self.append_msg( msg, clear = False )

        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setDisabled( False )
        self.q_push_button_1.setVisible( True )
        self.q_push_button_1.setCheckable( True )

        # seems to make togable, how to turn off
        #self.q_push_button_1.toggle()

        msg    = "add menu to q_push_button_1"
        self.append_msg( msg, clear = False )
        menu                = QMenu(self)
        menu.addAction("Menu Option 1")
        menu.addAction("Menu Option 2")
        # try to clear the menu
        widget.setMenu( None )

        # ---- change widget
        widget      = self.q_push_button_2
        msg         = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        widget.setStyleSheet("")
            # no style sheet

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
        self_q_push_button_1    = self.q_push_button_1
        self_q_push_button_2    = self.q_push_button_1

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
