#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which must
# be named tab_....py     among other things

KEY_WORDS:      progress dialog QThread thread helper message box
CLASS_NAME:     ProgressDialogTab
WIDGETS:        QWidget QThread
STATUS:         dec 2025 seems working well
TAB_TITLE:      Progress Dialog / Two Threads
DESCRIPTION:    A demonstration of a progress dialog tracking a task running in a helper thread,
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Progress-Dialogs-Two-Threads"

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


from qtpy.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QDialog, QTextEdit, QHBoxLayout
)
from qtpy.QtCore import QThread, Signal


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


#--------------------------------------
class HelperThread( QThread ):
    update_signal       = Signal(str)
    finished_signal     = Signal()

    #-------------------------
    def __init__(self, task_function, task_function_arg ):
        super().__init__()
        self._running = True

        self.task_function     = task_function
        self.task_function_arg = task_function_arg


    #-------------------------
    def run(self):
        """



        """
        self._running = True

        # for ix in range(5):
        #     if not self._running:
        #         break
        #     self.update_signal.emit( str(ix) )
        #     time.sleep(0.5)

        self.task_function( self, self.task_function_arg )
            # self =HelperThread, so we can send back messages

        #self.cleanup()
        self.finished_signal.emit()

    #-------------------------
    def stop(self):
        """ """
        #self.cleanup()
        self._running = False




#-------------------------------------
class ProgressDialog( QDialog ):


    def __init__(self, parent=None, *, dialog_args = {}, task_function = None, task_function_arg = None ):

        super().__init__(parent)

        self.task_function      = task_function
        self.task_function_arg  = task_function_arg

        title   = dialog_args.get( "title", None )
        if title is None:
            title  = "default_progress_dialog"



        self.setWindowTitle( title )
        self.resize(300, 200)

        # Layout
        main_layout         = QVBoxLayout(self)
        widget              = QTextEdit(self)
        self.text_area      = widget
        widget.setReadOnly(True)
        main_layout.addWidget( widget )

        button_layout = QHBoxLayout()

        widget              = QPushButton("Stop", self)
        self.stop_button    = widget
        # Connect stop button
        widget.clicked.connect( self.stop_thread )
        button_layout.addWidget( widget )
        main_layout.addLayout(button_layout)

        # Thread setup
        self.thread = HelperThread( task_function     = self.task_function,
                                    task_function_arg = self.task_function_arg )

        self.thread.update_signal.connect(self.update_text)
        self.thread.finished_signal.connect(self.close)


    #-------------------------
    def start_thread(self):
        """ """
        self.text_area.clear()
        if not self.thread.isRunning():
            self.thread.start()

    #-------------------------
    def stop_thread(self):
        """ """
        msg     = "ProgressDialog.stop_thread()"
        print( msg )
        if self.thread.isRunning():
            self.thread.stop()

    #-------------------------
    def update_text(self, text):
        self.text_area.append(text)

    #-------------------------
class ProgressDialogTab( tab_base.TabBase ):
    """
    get code from
    /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/qt5_by_example/chat_dialog_4.py

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

    #-------------------------
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
        widget              = QPushButton( "open_counter_dialog" )
        self.q_push_button_1    = widget

        connect_to          = self.open_progress_dialog
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # widget              = QPushButton( "open_directory_dialog" )
        # self.q_push_button_2    = widget
        # connect_to          = self.open_directory_dialog
        # widget.clicked.connect( connect_to    )
        # row_layout.addWidget( widget,  )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

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

    # ------------------------------------
    def open_progress_dialog(self):
        """ """
        task_function_arg   = ( 20, 24 )

        dialog_args    = {
                            "title": "title from dialog_args"
                            }

        dlg = ProgressDialog(self,
                             dialog_args         = dialog_args,
                             task_function       = self.task_function,
                             task_function_arg   = task_function_arg )
        dlg.show()
        dlg.start_thread()

    # ------------------------------------
    def task_function( self, helper_thread, task_function_arg = None ):
         """ """
         #for ix in range( 100, 103 ):
         for ix in range( *task_function_arg ):
             msg    = f"task_function{ix}"
             print( msg   )
             helper_thread.update_signal.emit( msg )
             time.sleep( .5 )

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

        # # we set local variables to make it handy to inspect them
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


