#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof
"""
KEY_WORDS:      dialog boxes of various forms modal browse for file or directory path   new_base
CLASS_NAME:     DialogEtcTab
WIDGETS:        QMessageBox  QFileDialog
STATUS:         !! runs    runs_correctly  demo_partial   demo_complete
TAB_TITLE:      Dialog Boxes
TAB_HELP:       use  self.help_file_name     =  "dialog_boxes_tab.txt"


 /mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/docs/date_edit_widget_tab.txt

/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/docs/date_edit_widget_tab.txtper_tab.txt

see also the wat window and the python execute window in stuffdb

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    # qt_widgets.main( )
# --------------------


#import inspect
#import subprocess
#import sys
#import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat
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
                             QDialog,
                             QFileDialog,
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


from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit,
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QDialogButtonBox)
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base
# ---- imports neq qt


# ---- end imports


INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.


#  --------
class DialogEtcTab( tab_base.TabBase  ):
    def __init__(self):
        """
        q_dialog_etc_tab.py
        """
        super().__init__()
        self.help_file_name     =  "dialog_boxes_tab.txt"


        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_gui()   # in base class



    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        # ---- New Row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- QPushButton("Open Messagebox")
        widget          = QPushButton("show_message\n_box")
        widget.setCheckable(True)
        widget.clicked.connect( lambda: self.show_message_box( ) )
        row_layout.addWidget( widget )

        # ---- dialog_for_data
        widget = QPushButton("dialog_for_data")
        widget.clicked.connect( self.dialog_for_data    )
        row_layout.addWidget( widget,   )

        # ---- PB inspect
        widget = QPushButton("browse_for\nfile")
        widget.clicked.connect( self.browse_for_file    )
        row_layout.addWidget( widget,   )

        # ---- PB inspect
        widget = QPushButton("browse_for\ndirectory")
        widget.clicked.connect( self.browse_for_directory    )
        row_layout.addWidget( widget,   )

        widget = QPushButton("mutate\n")
        self.button_ex_1         = widget
        widget.clicked.connect( lambda: self.mutate( ) )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget = QPushButton("inspect\n")
        widget.clicked.connect( self.inspect    )
        row_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton("breakpoint\n")
        widget.clicked.connect( self.breakpoint    )
        row_layout.addWidget( widget,   )

    # ------------------------------------
    def show_message_box( self ):
        """
        what is says
        """
        self.append_function_msg( "show_message_box" )

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Make a Choice")
        msg_box.setText("Please choose one:")

        choice_a = msg_box.addButton("Choice A", QMessageBox.ActionRole)
        choice_b = msg_box.addButton("Choice B", QMessageBox.ActionRole)

        # Set the dialog to be modal (blocks interaction with other windows)
        msg_box.setModal(True)

        msg_box.exec_()

        if msg_box.clickedButton() == choice_a:
            self.append_msg( "Choice A selected")
        elif msg_box.clickedButton() == choice_b:
            self.append_msg( "Choice B selected")

        QMessageBox.information( self, "a title",
                                "additional message")

        self.append_msg( "-- done" )
    # ------------------------
    def dialog_for_data( self, ): #open_input_dialog_ds(self):
        """ """

        self.append_function_msg( "dialog_for_data" )

        # Mutable object to pass data to and from the dialog
        data = {"initial_value": "Default Value"}  # Optional: Set initial value

        # Create and show the dialog
        dialog = InputDialogDS (data, self)
        result = dialog.exec()

        # Check if the dialog was accepted or rejected
        if result == QDialog.Accepted:
            msg     = f"Entered data: {data['return_value']}"
            #QMessageBox.information(self, "Result", msg )
            self.append_msg( msg )

        else:
            msg     = "Dialog was canceled"
            #QMessageBox.information(self, "Result",  msg )
            self.append_msg( msg )


    # ------------------------
    def message_box_2( self, msg = "this is a default message " ):
        """
        not hooked up
        what it says
        could i have some simple python code to give the user a message
        write it as a method which takes the message as an argument
        pretty much the same as my example
        """
        self.append_function_msg( "message_box_2" )
        msg_box = QMessageBox()
        msg_box.setIcon( QMessageBox.Information )
        msg_box.setText( msg )  # Set the message text
        msg_box.setWindowTitle( "Sorry that is a No Go " )
        msg_box.setStandardButtons( QMessageBox.Ok )

        # Show the message box and wait for the user to close it
        msg_box.exec_()

    # ------------------------
    def browse_for_file(self):
        """
        what it says
        """
        self.append_function_msg( "browse_for_file" )

        initial_dir     = "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/__pycache__"

        file_dialog     = QFileDialog(self, "Select Files")

        file_dialog.setFileMode(QFileDialog.ExistingFiles) #multiple file selection
        file_dialog.setFileMode(QFileDialog.ExistingFile)  # Single file selection
        #file_dialog.setNameFilter("All Files (*);;Python Files (*.py)")  # File filters
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")
        file_dialog.setDirectory( initial_dir )
        # file_dialog.setWindowTitle(  title      )
        # #file_dialog.setNameFilter(   file_types  )

        if file_dialog.exec_():
            #files = file_dialog.selectedFiles()   # multiple files
            files = file_dialog.getOpenFileName()             # single file
            self.append_msg( "browse Selected files:")
            for file in files:
                self.append_msg( file)
                row_data     = [ file, "1", "2"]

        # ---- also work this in
        # Configure the QFileDialog for a single file
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            caption="Select a File",            # Window title
            directory=".",                      # Initial directory
            filter="All Files (*);;Python Files (*.py)"  # File type filters
        )

        # Print the selected file path
        if file_path:
            self.append_msg( f"Selected file: {file_path}")
        else:
            self.append_msg(  "No file selected.")

        self.append_msg( "-- done" )

    # ------------------------
    def new_main(self):
        """
        what it says
        """
        self.append_function_msg( "new_main" )

        1/0    # writer me !!

    # ------------------------
    def browse_for_directory(self):
        """
        what it says
        """
        self.append_function_msg( "browse_for_directory" )

        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.append_msg( f"Selected Directory: {directory}")
        else:
            self.append_msg( "No directory selected")

        self.append_msg( "-- done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( "-- done" )
    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( "mutate_1 done" )


    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        wat_inspector.go(
             msg            = "DialogEtcTab",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "-- done" )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

# class InputDialogDS(QDialog):
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class InputDialogDS(QDialog):
    """
    deep seek did draft fixed a bit
    """
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data  # dict
        self.initUI()

    def initUI(self):
        """ """

        self.setWindowTitle("Input Dialog")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        # Label
        label = QLabel("Enter some data:")
        layout.addWidget(label)

        # Line Edit for input
        self.line_edit = QLineEdit(self)
        if "initial_value" in self.data:
            self.line_edit.setText(self.data["initial_value"])
        layout.addWidget(self.line_edit)

        # OK Button
        widget = QPushButton("OK", self)
        widget.clicked.connect(self.on_ok)
        layout.addWidget(widget)

        # Cancel Button
        widget = QPushButton("Cancel", self)
        widget.clicked.connect(self.on_cancel)
        layout.addWidget(widget)

        self.setLayout(layout)

    def on_ok(self):
        """
        what it says
        """
        self.data["return_value"] = self.line_edit.text()
        self.accept()  # Close the dialog and return QDialog.Accepted

    def on_cancel(self):
        """
        what it says
        """
        self.reject()  # Close the dialog and return QDialog.Rejected


# ---- eof