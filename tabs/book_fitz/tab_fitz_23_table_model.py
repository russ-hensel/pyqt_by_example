#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof


"""
KEY_WORDS:      Querying SQL databases with Qt models   rsh
CLASS_NAME:     Fitz_23_A_Tab
WIDGETS:        QTableView() QSqlTableModel
STATUS:         june 2025 runs_functionally not in good shape
TAB_TITLE:      Fitz Chapt 23 / TableModel
DESCRIPTION:    This needs review
HOW_COMPLETE:   15  #  AND A COMMENT
"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QPushButtons"
"""
looked at

"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_filterproxy_widget_mapper_controls.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_querymodel.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_querymodel_parameter.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_querymodel_search.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_relationalmodel.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_relationalmodel_delegate.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel_filter.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel_filter_clean.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel_sort.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel_sortname.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel_titles.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/tableview_tablemodel_titlesname.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/widget_mapper.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/widget_mapper_controls.py"


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #qt_fitz_book.main()
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
from PyQt5 import QtGui
from PyQt5.QtCore import (QAbstractListModel,
                          QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from PyQt5.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument, QIcon
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
# widgets biger
# widgets -- small
# layouts
from PyQt5.QtWidgets import (QAction,
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
                             QHeaderView,
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
import global_vars
import tab_base
# ---- imports neq qt



# ---- end imports

print_func_header       = uft.print_func_header

basedir                 = os.path.dirname(__file__)

tick                    = QImage(os.path.join("tick.png"))

# append_msg              = global_vars.CONTROLLER.append_msg        #( self.msg_widget, msg )
# append_function_msg     = global_vars.CONTROLLER.append_function_msg          #( self, msg_widget, msg, clear = True ):

WIDTH_MULP              = 10   # change to donctant

# Color scale, which is taken from colorbrewer2.org.
# Color range -5 to +5; 0 = light gray
COLORS = [
    "#053061",
    "#2166ac",
    "#4393c3",
    "#92c5de",
    "#d1e5f0",
    "#f7f7f7",
    "#fddbc7",
    "#f4a582",
    "#d6604d",
    "#b2182b",
    "#67001f",
]



#  --------
class Fitz_23_A_Tab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage



        global WIKI_LINK
        self.wiki_link          = WIKI_LINK


        # self._build_model()
        #self._build_gui()
        # self.mutate_ix   = 0
        self.ix_sort     = 0   # for sorting

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        self.mutate_dict[2]    = self.mutate_2
        self.mutate_dict[3]    = self.mutate_3
        self.mutate_dict[4]    = self.mutate_4

        self._build_model()
        # self._pre_gui()
        self._build_gui()


    #------------------------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )



        # # ---- new row
        # row_layout    = QHBoxLayout(   )
        # layout.addLayout( row_layout,  )

        # widget              = QLabel( "classes...... on this tab" )
        # self.class_widget   = widget
        # row_layout.addWidget( widget,   )

        # ---- new row
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        widget    =  self.view
        row_layout.addWidget( widget,   )

        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ----
        widget              = QTextEdit("load\nthis should be new row ")
        self.msg_widget     = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget,   )

        # ---- new row,
        row_layout = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- PB
        widget = QPushButton("select_all\n")
        widget.clicked.connect( self.select_all  )
        row_layout.addWidget( widget,   )

        # ----set_headers
        widget = QPushButton("set_headers\n")
        widget.clicked.connect( self.set_headers    )
        row_layout.addWidget( widget,   )

        # ----remove_columns
        widget = QPushButton("remove_columns\n")
        widget.clicked.connect( self.remove_columns    )
        row_layout.addWidget( widget,   )



        # ---- "
        widget = QPushButton("select_with_filter\n" )
        widget.clicked.connect( self.select_with_filter   )
        row_layout.addWidget( widget,   )

        # ---- new row,
        row_layout = QHBoxLayout(   )
        layout.addLayout( row_layout,  )


        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( row_layout )

    # -------------------------------
    def _build_model(self,   ):
        """
        and the view
        """
        self.view               = QTableView()

        model                   = QSqlTableModel( self, global_vars.EX_DB   )
        self.model              = model
        self.persons_model      = model
        model.setTable('persons')

        self.view.setModel( self.model )

        # #query       = QSqlQuery( "SELECT Name,   FROM persons ", db = global_vars.EX_DB )
        # self.model.setTable( "persons" )


    print( "button code from other example may reacivate some ")

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        self.append_function_msg( "add()" )

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
        self.append_function_msg( "delete()" )

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
        self.append_function_msg( "complete()" )

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

    def set_headers( self ):
        """ """
        self.append_function_msg( "set_headers()" )

        model    = self.model      # would think in view but no

        model.setHeaderData(1, Qt.Horizontal, "SetCol1")
        model.setHeaderData(2, Qt.Horizontal, "SetCol2")

    def remove_columns( self ):
        """ """
        self.append_function_msg( "remove_columns from what is visible " )
        msg                 = "here remove by column name"
        self.append_msg( msg )
        model               = self.model
        columns_to_remove   = ['name', 'something']
        for c_name in columns_to_remove:
            idx = model.fieldIndex( c_name )
            model.removeColumns( idx, 1 )  # what is 1

    def select_with_filter( self ):
        """ """
        self.append_function_msg( "select_with_filter()" )
        a_name     = "a"
        filter_str = f"Name LIKE %{ a_name }%"
        self.model.setFilter( filter_str )



    def select_all( self ):
        """ """
        self.append_function_msg( "select_all()" )



        self.ix_sort    += 1
        if self.ix_sort > 1:
            self.ix_sort = 0

        if self.ix_sort == 0:
            sort_order   = Qt.DescendingOrder
        else:
            sort_order   = Qt.AscendingOrder

        msg      = f"{sort_order = }"
        self.append_msg( msg )

        self.model.setFilter( "" )
        idx = self.model.fieldIndex( "age" )
        self.model.setSort( idx, sort_order )

        self.model.select()

        #self.model.layoutChanged.emit() # This triggers a refresh of the entirety of the view. I
        self.append_msg( "<<-- done" )

    def save(self):
        self.append_function_msg( "save" )

        with open("data.json", "w") as f:
            data = json.dump(self.model.todos, f)
        self.append_msg( "<<-- done" )


    #----------------------------
    def mutate_0( self  ):
        """
        read it
        getText get text
        """
        self.append_function_msg( "mutate_0  headers and width  " )
        #self.append_function_msg( "mutate_0" )

        # table   = self.table_widget
        # table.hideRow( 1 )
        # table.hideColumn( 1 )

        model    = self.model      # would think in view but no

        model.setHeaderData(1, Qt.Horizontal, "SetCol1")
        model.setHeaderData(2, Qt.Horizontal, "SetCol2")

        view     = self.view
        # beware of units for width multiply for character width ?

        view.setColumnWidth( 1, 20  * WIDTH_MULP )
        view.setColumnWidth( 2, 20  * WIDTH_MULP )

        self.append_msg( "<<-- done" )

    #----------------------------
    def mutate_1( self  ):
        """
        read it
        """
        self.append_function_msg( "mutate_1 change width" )

        view     = self.view
        view.setColumnWidth( 1, 50 * WIDTH_MULP )
        view.setColumnWidth( 2, 50 * WIDTH_MULP )

        self.append_msg( "<<-- done" )
    #----------------------------
    def mutate_2( self  ):
        """
        read it
        """
        self.append_function_msg( "mutate_2" )

        # table   = self.table_widget
        # table.showRow( 1 )
        # table.showColumn( 1 )

        self.append_msg( "<<-- done" )
    #----------------------------
    def mutate_3( self  ):
        """


        """
        self.append_function_msg( "mutate_3 -- change headers" )

        # table       = self.table_widget
        # table.setHorizontalHeaderLabels( [ "xxxx", "yyy", ])
        # table.setColumnWidth(2, 100)  # Set specific width for a column
        self.append_msg( "<<-- done" )
    #----------------------------
    def mutate_4( self  ):
        """
        read it -- right now does nothing new

        """
        self.append_function_msg( "mutate_4 -- change headers" )

        # table            = self.table_widget
        # table_widget     = table

        self.append_msg( "<<-- done" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        #print_func_header( "inspect" )
        self.append_msg( "inspect", clear = True )

        self_model          = self.model
        self_view           = self.view

        wat_inspector.go(
             msg            = "locals for model and view",
             a_locals       = locals(),
             a_globals      = globals(), )
        self.append_msg( "<<-- done" )
    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( "<<-- done" )

# ---- eof