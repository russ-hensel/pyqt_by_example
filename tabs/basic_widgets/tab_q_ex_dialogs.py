#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which must
# be named tab_....py     among other things

KEY_WORDS:      dialog questionBox  Message Box
CLASS_NAME:     QDialogsTab
WIDGETS:        QMessageBox QDialog
STATUS:         2025 dec draft
TAB_TITLE:      QDialogsTab / various
DESCRIPTION:    A few examples of dialogs
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Misc-Dialogs"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------------------

# ---- import
import inspect
import subprocess
import os
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run
from pathlib import Path
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

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
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

# class FileDialogMemoryMixin:
#     """
#     Mixin class that remembers the last directory used in file dialogs.
#     Can be used with any QWidget-based class.

#     code deleted ask a chatbot if you want
#     """


from qtpy.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
from qtpy.QtCore import Qt

class ExQDialog( QDialog ):
    """
    An example dialog from chat then edited """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        # Set the dialog title
        self.setWindowTitle("My Custom Dialog")

        # Explicitly set the size (width, height)
        self.resize(400, 250)

        # Optional: Set minimum and maximum sizes
        self.setMinimumSize(300, 200)
        self.setMaximumSize(600, 400)

        # Create layout
        layout = QVBoxLayout()

        # Add some widgets
        label = QLabel("Enter your name:")
        self.name_input = QLineEdit()

        # Add buttons
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        # Connect buttons
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        # Add widgets to layout
        layout.addWidget(label)
        layout.addWidget(self.name_input)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        # Set the layout
        self.setLayout(layout)

    def get_name(self):
        """Return the entered name"""
        return self.name_input.text()


#  --------
class QDialogsTab( tab_base.TabBase ):
    """
    Reference examples for QFileDialogTab and


    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link              = WIKI_LINK

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]         = self.mutate_0
        self.mutate_dict[1]         = self.mutate_1
        self.current_default_dir    = "~"  # change as dilog used -- seems not to work
        self.current_default_dir    = "../"   # seems to work "

        self._build_gui()

    #---------------------------
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

        # we use a local variable because it reduces the amount of code
        # and does not run any slower
        # we use this local variable idea in many places
        # because we will refer to the bu
        widget              = QPushButton( "open_message_box" )
        self.q_push_button_1    = widget

        connect_to          = self.open_message_box
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        widget              = QPushButton( "open_ex_qdialog" )
        self.q_push_button_2    = widget
        connect_to          = self.open_ex_qdialog
        widget.clicked.connect( connect_to    )
        row_layout.addWidget( widget,  )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # ------------------------------------
    def signal_sentxxx( self, msg ):
        """
        when a signal is sent, use find ???

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "signal_sent()" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( tab_base.DONE_MSG )


    # ------------------------------------
    def open_ex_qdialog( self ):
        """
        What it says

        """

        dialog = ExQDialog()
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.get_name()
            print(f"Name entered: {name}")
        else:
            print("Dialog cancelled")



    # ------------------------------------
    def open_message_box( self ):
        """
        What it says
            add some returns
        """

        from qtpy.QtWidgets import (  QMessageBox, )


        msg_box_msg    = "this is a message"
        msg_box             = QMessageBox()
        msg_box.setIcon( QMessageBox.Information )
        msg_box.setText(  msg_box_msg  )
        msg_box.setWindowTitle( "Sorry that is a No Go " )
        msg_box.setStandardButtons( QMessageBox.Ok )

        ret    = msg_box.exec_()
        print( f"{ret = }" )


    # ------------------------------------
    def open_directory_dialog( self ):
        """
        What it says
            add some returns !!
            code written as if we could return multiples, but we cannot
        """


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

        # # ---- change widget
        # msg    = "for q_push_button_1 we more or less reset it"
        # self.append_msg( msg, clear = False )
        #     # we use a local variable because it reduces the amount of code
        #     # and does not run any slower
        #     # we use this local variable idea in many places
        # widget          = self.q_push_button_1
        # widget.setText( "text set in mutate_0()" )
        # widget.width     = 300
        # widget.setToolTip( None )
        # widget.setStyleSheet( "" )

        # # ---- change widget
        # msg    = "for q_push_button_2 no mutations"
        # self.append_msg( msg, )

        # widget          = self.q_push_button_2
        # # self.q_push_button_1.setDisabled( True )
        # # self.q_push_button_2.setDisabled( False )

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

        # msg    = "mess with q_push_button_1"
        # self.append_msg( msg, )

        # widget        = self.q_push_button_1
        #     # it is often convenient to use a local variable,
        #     # you will see this a lot in our code, it does not seem to
        #     # be typical but we think it should be

        # msg    = "q_push_button_1 set a tooltip"
        # self.append_msg( msg, )

        # widget.setToolTip( "this is a tool tip" )
        # widget.setText( "text set in \nmutate_1()" )
        #     # note \n
        # widget.width     = 200

        # # ---- change widget
        # msg    = "some changes to q_push_button_2"
        # self.append_msg( msg, clear = False )

        # # ---- self.q_push_button_2
        # widget        = self.q_push_button_2
        # # msg    = "setChecked(True )"
        # self.append_msg( msg, )


        # msg        = f"{self.q_push_button_1.isChecked() = } "
        # self.append_msg( msg, )


        self.append_msg( tab_base.DONE_MSG )


    # ------------------------------------
    def inspect(self):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them
        # self_q_push_button_1    = self.q_push_button_1
        # self_q_push_button_2    = self.q_push_button_1

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
