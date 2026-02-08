#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
this is a second approach using two threads
lots of code from gemeeni only lightly tested and restyled

KEY_WORDS:      progress dialog to threads message box
CLASS_NAME:     ProgressDialogGuiIteratorTab
WIDGETS:        QWidget QThread
STATUS:         dec 2025 seems ok
TAB_TITLE:      Progress Dialog / Gui Iterator
DESCRIPTION:    A demonstration of a progress dialog tracking a task running in a worker thread
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      = "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Progress-Dialogs"
WIKI_LINK      = "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Progress-Dialogs-Gui-Iterator"
"""


gemeni and i worked this out, I edited, gemeni said ( befor editing )

Here is the complete, integrated application. In this version, the **MainWindow**
acts as both the user interface and the **Iterator** object itself.

By calling `init_iterator`, you reset the window's internal state for a fresh run.
The `ProgressDialog` then uses **Window Modality** to lock the main
interface while it "pumps" the window's own iterator logic.



---

### Key Features of this Revised Version:

* **Initialization & Cleanup:** The `init_iterator` method explicitly resets the counter
and resets the labels (turning them blue and clearing text) so the second run doesn't
look like a continuation of the first.
* **Window Modality:** The `setWindowModality(Qt.WindowModal)` ensures that while the loop
is running, the Main Window ignores all mouse clicks and keyboard input, effectively disabling it without needing to manually disable every single widget.
* **Direct Widget Access:** In `run_loop`, the code calls `self.main_win.status_label.setText()`.
Since everything is on the same thread, this is instantaneous and safe.
* **Linear Simplicity:** The logic remains a standard `for item in self.iterator` loop, which is much easier to maintain than a state-based timer system.
* **Zero-Parameter Logic:** Notice that `__next__` uses `self.current`.
No data needs to be passed between the window and the iterator because they are the same object.



"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------------------

# ---- import
import inspect
#import subprocess
import os
import sys
import time
#from   datetime import datetime
from   functools import partial
from   subprocess import PIPE, STDOUT, Popen, run
#from   pathlib import Path
import wat



from qtpy.QtCore import QCoreApplication
from qtpy import QtGui


from qtpy.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QDialog, QTextEdit, QHBoxLayout
    )

#from qtpy.QtCore import QThread, pyqtSignal

from qtpy.QtCore import (QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QPalette, QTextCursor, QTextDocument

# from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

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

# ---------------------------------------------------------
class ProgressDialog( QDialog ):
    def __init__(self, iterator_ref, parent):
        super().__init__(parent)
        self.iterator = iterator_ref # This is the MainWindow
        self.main_win = parent       # Also the MainWindow (for widget access)

        self.setWindowTitle("Processing Items...")
        self.setFixedSize(350, 180)

        # Control Flags
        self._is_paused = False
        self._is_halted = False

        # Layout
        self.layout     = QVBoxLayout(self)
        self.info_label = QLabel("Preparing to scan...")
        self.layout.addWidget(self.info_label)

        self.btn_layout = QHBoxLayout()
        self.pause_btn  = QPushButton("Pause")
        self.halt_btn   = QPushButton("Halt")

        self.btn_layout.addWidget(self.pause_btn)
        self.btn_layout.addWidget(self.halt_btn)
        self.layout.addLayout(self.btn_layout)

        # Connect Buttons
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.halt_btn.clicked.connect(self.halt_process)

    #------------------------
    def toggle_pause(self):
        self._is_paused = not self._is_paused
        self.pause_btn.setText("Continue") if self._is_paused else self.pause_btn.setText("Pause")

        if self._is_paused:
            self.main_win.status_label.setText("Status: PAUSED")

    def halt_process(self):
        self._is_halted = True

    def run_loop(self):
        """
        Standard linear loop running over the Parent Window's iterator.
        Uses processEvents() to keep the GUI alive.
        """
        try:
            # The 'for' loop triggers the MainWindow's __next__ method
            for item in self.iterator:

                # --- Halt Check ---
                if self._is_halted:
                    self.main_win.status_label.setText("Status: HALTED")
                    break

                # --- Pause Check (Nested processEvents loop) ---
                while self._is_paused:
                    QCoreApplication.processEvents()
                    if self._is_halted:
                        break
                    time.sleep(0.02) # Ease CPU usage

                # --- UI Updates ---
                # Update Dialog
                self.info_label.setText(f"Processing: <b>{item}</b>")

                # Update MainWindow (Direct Coupling)
                self.main_win.status_label.setText(f"Status: Working on {item}")
                self.main_win.count_label.setText(f"Items Processed: {self.iterator.current}")

                # --- Refresh GUI ---
                # Allows the 'Pause' and 'Halt' clicks to be registered
                QCoreApplication.processEvents()

                # Simulate work time
                time.sleep(0.04)

            # Final Cleanup
            if not self._is_halted:
                self.main_win.status_label.setText("Status: FINISHED")
                self.main_win.status_label.setStyleSheet("color: green; font-weight: bold;")

        except Exception as e:
            QMessageBox.critical(self, "Runtime Error", f"An error occurred: {str(e)}")

        finally:
            self.prepare_to_close()

    def prepare_to_close(self):
        self.info_label.setText("Session Complete.")
        self.pause_btn.setEnabled(False)
        self.halt_btn.setText("Close Window")
        self.halt_btn.clicked.disconnect()
        self.halt_btn.clicked.connect(self.accept)

#-------------------------------------
class ProgressDialogGuiIteratorTab( tab_base.TabBase ):
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
        #self.mutate_dict[1]         = self.mutate_1
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

        # ---- new Row buttons .....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

       #  widget              = QLabel("Status: Idle")
       #  self.status_display =  widget
       #  layout.addWidget(self.status_display)

       #  widget                  = QPushButton( "open_progress_dialog" )
       # # self.q_push_button_1    = widget
       #  self.launch_btn         = widget
       #  connect_to              = self.open_progress_dialog
       #  widget.clicked.connect( connect_to )
       #  row_layout.addWidget( widget )

        #------------------------------
        # Status displays that the iterator will update directly
        self.title_label = QLabel("File Processor System")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        row_layout.addWidget( self.title_label)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("color: #555; font-style: italic;")
        row_layout.addWidget( self.status_label)

        self.count_label = QLabel("Items Processed: 0")
        row_layout.addWidget( self.count_label)

        self.start_btn = QPushButton("Launch Process")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect( self.start_process)
        row_layout.addWidget( self.start_btn)

        # Internal state variables for iteration
        self.current   = 0
        self.limit     = 0

        #------------------------------

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

    # ---- Iterator Interface ---
    def init_iterator( self, limit=50 ):
        """
        Resets the iteration state and cleans up UI elements
        for a fresh run.
        """
        self.current     = 0
        self.limit       = limit

        # UI Cleanup
        self.status_label.setText("Status: Initializing...")
        self.count_label.setText("Items Processed: 0")
        self.status_label.setStyleSheet("color: blue; font-style: normal;")


    # ------------------------------------    # ------------------------------------
    def __iter__(self):
        return self

    # ------------------------------------
    def __next__(self):
        """The logic for each 'step' of the process."""

        if self.current < self.limit:
            # Simulate finding a file or data point
            result = f"Data_Package_{self.current:03d}.dat"
            self.current += 1
            return result

        # When exhausted, signal the loop to stop
        raise StopIteration


    # --- Execution Logic for itterator
    def start_process(self):
        # Prepare the 'Self' iterator
        self.init_iterator(limit=100)

        # Setup the Dialog
        # We pass 'self' so the dialog has a reference to the iterator
        # and the window widgets simultaneously.
        self.dial = ProgressDialog(iterator_ref=self, parent=self)

        # WindowModal prevents clicking the MainWindow but keeps the code running
        self.dial.setWindowModality(Qt.WindowModal)
        self.dial.show()

        # Hand off control to the Dialog's loop
        self.dial.run_loop()

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


        msg    = tab_base.NO_MUTATE_MSG
        self.append_msg( msg, clear = False )

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
