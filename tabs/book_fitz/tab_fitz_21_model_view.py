#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof


"""
KEY_WORDS:    chapter      simple Model View  Todo List   rsh
CLASS_NAME: Fitz_4_Tab
WIDGETS:    QAbstractListModel QListView DecorationRole
STATUS:     STATUS:      runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:  Fitz Chapt 21 / Model View
DESCRIPTION:    Code motivated by Fitz Chapt 21 A simple Model View — a Todo List
HOW_COMPLETE:   15  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Fitz-21-Model-View"
"""
Notes:
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_1.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_1b.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_2.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_3.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_4.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_5.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/model-views/todo_6.py"

largely the last


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------


import inspect
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat
from qtpy import QtGui
from qtpy.QtCore import (QAbstractListModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument
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
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
                             QListView,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QSlider,
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- imports neq qt



# ---- end imports



basedir = os.path.dirname(__file__)

tick = QImage(os.path.join("tick.png"))


class TodoModel( QAbstractListModel ):
    def __init__(self, *args, todos=None, **kwargs):
        super().__init__(*args, **kwargs)

        # the todos are the underlying data in the model
        self.todos = todos or []

    def data(self, index, role):
        """
        data()
        the data is the data from the model in the format
        as requested by the role
        For a list view column can be ignored.
        More on roles
            Qt Namespace | Qt Core 5.15.18
            https://doc.qt.io/qt-5/qt.html#ItemDataRole-enum

        """
        if role == Qt.DisplayRole:
            status, text = self.todos[index.row()]
            return text

        if role == Qt.DecorationRole:
            # role determine what sort of data is returned
            # it is requested for some purpose in the model
            # Instead of an icon you can also return a color, e.g.
            # QtGui.QColor('green') which will be drawn as solid square.

            status, text = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        """
        """
        return len(self.todos)


#  --------
class Fitz_4_Tab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK


        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_model()
        self._build_gui()

    # -------------------------------
    def _build_guixxx(self,   ):
        """
        layouts
            a vbox for main layout
            h_box for or each row of widgets
        """
        tab_page      = self
        layout        = QVBoxLayout( tab_page )

    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        # ---- new row
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        widget    =  self.todoView
        row_layout.addWidget( widget,   )

        # ---- new row,
        row_layout = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- PB
        widget = QPushButton("delete\n")
        widget.clicked.connect( self.delete   )
        row_layout.addWidget( widget,   )

        # ---- PB
        widget = QPushButton("complete\n")
        widget.clicked.connect( self.complete    )
        row_layout.addWidget( widget,   )

        # ---- new row,
        row_layout = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- Line Edit
        widget = QLineEdit("new items here")
        self.todoEdit  = widget
        #widget.clicked.connect( self.inspect    )
        row_layout.addWidget( widget,   )

        # # ---- new row,
        # button_layout = QHBoxLayout(   )
        # layout.addLayout( button_layout,  )

        # ---- "add\n_todo"
        widget = QPushButton("add\n_todo")
        widget.clicked.connect( self.add    )
        row_layout.addWidget( widget,   )

        # ---- new row,
        row_layout = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- PB self.load
        widget = QPushButton("load\n")
        widget.clicked.connect( self.load    )
        row_layout.addWidget( widget,   )

        # ---- PB self.save
        widget = QPushButton("save\n")
        widget.clicked.connect( self.save    )
        row_layout.addWidget( widget,   )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # -------------------------------
    def _build_model(self,   ):
        """
        and the view
        """
        self.model      = TodoModel()

        widget          = QListView()
        self.todoView   = widget

        widget.setModel( self.model )


    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """

        self.append_function_msg( "add" )

        text = self.todoEdit.text()
        # Remove whitespace from the ends of the string.
        text = text.strip()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()  # <1>
            # Empty the input
            self.todoEdit.setText("")

    def delete(self):
        """ """
        self.append_function_msg( "delete" )

        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a single-item list in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()

    def complete(self):
        """
        mark selected row as complete
        """
        self.append_function_msg( "complete" )

        indexes = self.todoView.selectedIndexes()
        if indexes:
            index           = indexes[0]
            row             = index.row()
            msg             = f"completing {row = }"
            self.append_msg( msg )
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
        else:
            msg    = "no selection to complete"
            self.append_msg( msg )

    # tag::loadsave[]
    def load(self):
        """ """
        self.append_function_msg( "load" )

        try:
            with open("data.json", "r") as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

        self.model.layoutChanged.emit() # This triggers a refresh of the entirety of the view. I

    def save(self):
        """ """
        self.append_function_msg( "save" )

        with open("data.json", "w") as f:
            data = json.dump(self.model.todos, f)

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )
        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        self_model         = self.model
        self_todo_view     = self.todoView

        wat_inspector.go(
             msg            = "locals for model and view",
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

# ---- eof