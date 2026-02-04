#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
this is a second approach using only one thread, so I hope the whole gui will be available
lots of code from gemeeni only lightly tested and restyled

KEY_WORDS:      progress dialog modal helper message box processEvents QCoreApplication
CLASS_NAME:     ProgressDialogOneThreadTab
WIDGETS:        QWidget QCoreApplication processEvents StopIteration
STATUS:         dec 2025 seems working well
TAB_TITLE:      Progress Dialog / OneThread
DESCRIPTION:    A demonstration of a progress dialog tracking a task running in the gui thread
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-Progress-Dialogs"
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-Progress-Dialogs-One-Thread"


"""
I prefer the approach where the gui is its onwn itterator look at that example
"""

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



from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtGui


from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QDialog, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal


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

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
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

# ------------
class CounterIterator:
    def __init__(self, limit=50):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.limit:
            val = str(self.current)
            self.current += 1
            return val
        raise StopIteration

# -------------------------. The Progress Dialog (Using Linear Loop logic)
class ProgressDialog(QDialog):

    def __init__(self, iterator, main_label_ref, parent = None ):
        """ """
        super().__init__(parent)
        self.iterator    = iterator
        self.main_label  = main_label_ref

        # Flags for control flow
        self._is_paused = False
        self._is_halted = False

        self.setWindowTitle("Direct Loop Controller")
        self.setFixedSize(350, 180)

        # UI Setup
        self.layout = QVBoxLayout(self)
        self.status_label = QLabel("Ready to start...", self)
        self.layout.addWidget(self.status_label)

        self.btn_layout     = QHBoxLayout()
        self.pause_btn      = QPushButton("Pause")
        self.halt_btn       = QPushButton("Halt")

        self.btn_layout.addWidget(self.pause_btn)
        self.btn_layout.addWidget(self.halt_btn)
        self.layout.addLayout(self.btn_layout)

        self.pause_btn.clicked.connect(self.toggle_pause)
        self.halt_btn.clicked.connect(self.halt_process)

    #------------------------
    def toggle_pause(self):
        self._is_paused = not self._is_paused
        self.pause_btn.setText("Continue") if self._is_paused else self.pause_btn.setText("Pause")

    #------------------------
    def halt_process(self):
        self._is_halted = True

    #------------------------
    def run_loop(self):
        """
        The core logic. This runs a standard loop but manually
        pumps the Qt event queue.
        """
        try:
            for item in self.iterator:
                # --- CHECK HALT ---
                if self._is_halted:
                    self.main_label.setText("Main Status: Halted")
                    break

                # --- CHECK PAUSE ---
                while self._is_paused:
                    # We MUST process events here, or the 'Continue' button won't work!
                    QCoreApplication.processEvents()
                    if self._is_halted: break
                    time.sleep(0.01) # Avoid 100% CPU usage during pause

                # --- UPDATE UI ---
                self.status_label.setText(f"Processing: {item}")
                self.main_label.setText(f"Main Status: Running ({item})")

                # --- THE MAGIC LINE ---
                # This keeps the UI responsive and allows clicks to be registered
                QCoreApplication.processEvents()

                # Artificial delay so we can see it happen
                time.sleep(0.1)

            if not self._is_halted:
                self.status_label.setText("Process Finished.")
                self.main_label.setText("Main Status: Idle")

        except Exception as e:
            QMessageBox.critical(self, "Iterator Error", str(e))

        finally:
            self.pause_btn.setEnabled(False)
            self.halt_btn.setText("Close")
            # Disconnect old signals and set to close the dialog
            self.halt_btn.clicked.disconnect()
            self.halt_btn.clicked.connect(self.accept)


#-------------------------------------
class ProgressDialogOneThreadTab( tab_base.TabBase ):
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

        # ---- new row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row buttons .....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget              = QLabel("Status: Idle")
        self.status_display =  widget
        layout.addWidget(self.status_display)

        widget                  = QPushButton( "open_progress_dialog" )
       # self.q_push_button_1    = widget
        self.launch_btn         = widget
        connect_to              = self.open_progress_dialog
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


    def open_progress_dialog(self):
        """ """
        self.launch_btn.setEnabled(False) # CRITICAL: Prevent re-entrancy

        it = CounterIterator(limit=50)
        self.dial = ProgressDialog(it, self.status_display, self)

        # Show the dialog non-modally
        self.dial.show()

        # Start the loop manually
        self.dial.run_loop()

        self.launch_btn.setEnabled(True)

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
