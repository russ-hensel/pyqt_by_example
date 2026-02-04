#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 07:39:59 2024

@author: russ
"""
# ---- tof

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import qt_sql_widgets
    qt_sql_widgets.main()
# --------------------

import inspect
#from   ex_qt import ia_qt
#import ia_qt
import subprocess
import sys
#import adjust_path
import time
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
# widgets bigger
# widgets -- small
# layouts
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
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
import qt_widgets
import utils_for_tabs as uft
import wat_inspector

# ---- end imports


print_func_header   = uft.print_func_header


class DateDelegate( QStyledItemDelegate ):
    """
    example from chat of a delegate
    for DelegateTab

    in db dob is text '1985-11-30'  ... see tab_qsql_database '1985-11-30'

    """

    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setDisplayFormat('yyyy-MM-dd')
        editor.setCalendarPopup(True)
        return editor

    def setEditorData(self, editor, index):
        # Get the current data from the model and set it into the editor
        date_str = index.model().data(index, Qt.EditRole)
        date = QDate.fromString(date_str, 'yyyy-MM-dd')
        editor.setDate(date)

    def setModelData(self, editor, model, index):
        # When the editor is done, save the data back to the model
        date = editor.date().toString('yyyy-MM-dd')
        model.setData(index, date, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        # Position the editor correctly within the cell
        editor.setGeometry(option.rect)



#-----------------------------------------------
class DelegateTab( QWidget ):
    """
    here build a tab in its own class to hide its variables
    and have its own namespace
    this delegate interacts with a view
    """
    def __init__(self, ):
        """
        """
        super().__init__( )

        self.build_tab()
        self.model.select()

    #-----------------------------------------------
    def build_tab(self,   ):
        """
        the usual widget construct and init
        """
        tab_page        = self
        layout          = QVBoxLayout( tab_page )

        model           = QSqlTableModel(  self, uft.EXAMPLE_DB  )
        self.model      = model
        model.setTable('employee')
        model.select()  # Load data into the model

        table_view = QTableView()
        table_view.setModel(model)

        # Apply the date delegate to the 'dob' column (column index 1)
        date_delegate = DateDelegate()
        table_view.setItemDelegateForColumn( 1, date_delegate )

        table_view.show()

        layout.addWidget( table_view )

        # ---- QLineEdit  can it hold some data, the date?
        widget          = QLineEdit()
        widget.setText( "QLineEdit use set text to set value")
        layout.addWidget( widget )

        # ---- QPushButton
        widget              = QPushButton("QPushButton x")
        self.button_ex_1    = widget
        # widget.clicked.connect(lambda: self.print_message(widget.text()))
        a_widget        = widget
        widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        layout.addWidget( widget )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        # ---- PB inspect
        widget = QPushButton("inspect\n")
        widget.clicked.connect( self.inspect    )
        button_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton("breakpoint\n")
        widget.clicked.connect( self.breakpoint    )
        button_layout.addWidget( widget,   )



    # def create_tab_connection( self ):
    #     # Setup a connection to an SQLite database (for example)
    #     db = QSqlDatabase.addDatabase('QSQLITE')
    #     self.db    = db
    #     db.setDatabaseName(':memory:')  # In-memory database, for demo purposes
    #     if not db.open():
    #         print("Unable to open database")
    #         return False

    #     # Create a sample table and insert data
    #     query = db.exec_("""
    #         CREATE TABLE people (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             name TEXT,
    #             dob TEXT,
    #             occupation TEXT
    #         );
    #     """)

    #     query = db.exec_("""
    #         INSERT INTO people (name, dob, occupation) VALUES
    #         ('Alice', '1990-04-20', 'Engineer'),
    #         ('Bob', '1985-11-30', 'Designer'),
    #         ('Charlie', '1992-06-15', 'Developer');
    #     """)

    #     return True



    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        self_widgets_list   = self.widgets_list
        wat_inspector.go(
             msg            = "see self_widgets_list",
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        print_func_header( "breakpoint" )

        breakpoint()
