#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof


"""
KEY_WORDS:      chapter   C  Generic queries with QSqlQueryModel sql where  fitzz
CLASS_NAME:     Fitz_23_C_Tab
WIDGETS:        QTableView QSqlQueryModel QSqlQuery
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      Fitz Chapt 23 / SqlModel
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
DESCRIPTION:    Code motivated by Fitz Chapt 23 Sql with QSqlQueryModel
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Fitz-23-Query_Model"

"""
looked at

"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/chinook.sqlite",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/Chinook_Sqlite.sqlite",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/_snippet_connection.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/databases/_snippet_relational.py",
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
from qtpy import QtGui
from qtpy.QtCore import (QAbstractListModel,
                          QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument, QIcon
# sql
from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
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


# ---- end imports


basedir = os.path.dirname(__file__)

tick = QImage(os.path.join("tick.png"))





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
class Fitz_23_C_Tab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self._build_model()
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        self.mutate_ix   = 0
        self.ix_sort     = 0   # for sorting

        self._build_gui()



    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        #button_layout        = QHBoxLayout(   )



        # ---- new row
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        widget    =  self.view
        row_layout.addWidget( widget,   )

        # ---- new row,
        row_layout = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- PB
        widget = QPushButton("select_all\n")
        widget.clicked.connect( self.select_all  )
        row_layout.addWidget( widget,   )

        # # ----set_headers
        # widget = QPushButton("set_headers\n")
        # widget.clicked.connect( self.set_headers    )
        # row_layout.addWidget( widget,   )

        # # ----remove_columns
        # widget = QPushButton("remove_columns\n")
        # widget.clicked.connect( self.remove_columns    )
        # row_layout.addWidget( widget,   )

        # # ---- new row,
        # row_layout = QHBoxLayout(   )
        # layout.addLayout( row_layout,  )

        # ---- "
        widget = QPushButton("select_with_where\n" )
        widget.clicked.connect( self.select_with_where   )
        row_layout.addWidget( widget,   )

        # # ---- new row,
        # row_layout = QHBoxLayout(   )
        # layout.addLayout( row_layout,  )

        # # ---- PB self.load
        # widget = QPushButton("load\n")
        # widget.clicked.connect( self.load    )
        # row_layout.addWidget( widget,   )

        # # ---- PB self.save
        # widget = QPushButton("save\n")
        # widget.clicked.connect( self.save    )
        # row_layout.addWidget( widget,   )
        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # -------------------------------
    def _build_model(self,   ):
        """        print_func_header(
        and the view
        """

        self.view       = QTableView()

        self.model      = QSqlQueryModel( )   # no db connection that comw thru query
        self.view.setModel( self.model )

        sql         = "SELECT name   FROM persons "
        query       = QSqlQuery( sql, db = global_vars.EX_DB )
            # error reporta are missing
            # insetad of self.model.setTable( "persons" )
        self.model.setQuery( query )

        # print( "button code from other example may reacivate some ")


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
            print( msg )
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
        else:
            msg    = "no selection to complete"
            print( msg )

    def set_headers( self ):
        """ """
        self.append_function_msg( "set_headers()" )

        model    = self.model      # would think in view but no

        model.setHeaderData(1, Qt.Horizontal, "SetCol1")
        model.setHeaderData(2, Qt.Horizontal, "SetCol2")

    def remove_columns( self ):
        """ """
        self.append_msg( "remove_columns()" )
        msg                 = "here remove by column name"
        print( msg )
        model               = self.model
        columns_to_remove   = ['name', 'something']
        for c_name in columns_to_remove:
            idx = model.fieldIndex( c_name )
            model.removeColumns( idx, 1 )  # what is 1

    def select_with_where( self ):
        """ """
        self.append_msg( "select_with_where()" )


        a_name          = "%a%"
        msg             = f" where like   {a_name =} "
        print( msg )
        sql             =  "SELECT name, age  FROM persons "
        filter_str      = f"WHERE persons.name  LIKE :a_name"
        sql             = sql +  filter_str
        print( f"{sql =}" )

        query = QSqlQuery( db = global_vars.EX_DB )
        query.prepare( sql )
        query.bindValue(":a_name", a_name )
        query.exec_()
        self.model.setQuery(query)


    def select_all( self ):
        """ """
        self.append_function_msg( "select_all  is a nop " )

        # self.ix_sort    += 1
        # if self.ix_sort > 1:
        #     self.ix_sort = 0

        # if self.ix_sort == 0:
        #     sort_order   = Qt.DescendingOrder
        # else:
        #     sort_order   = Qt.AscendingOrder

        # msg      = f"{sort_order = }"
        # print( msg )

        # self.model.setFilter( "" )  'QSqlQueryModel' object has no attribute 'setFilter'
        # idx = self.model.fieldIndex( "age" )
        # self.model.setSort( idx, sort_order )

        # self.model.select()  'QSqlQueryModel' object has no attribute 'select'

        #self.model.layoutChanged.emit() # This triggers a refresh of the entirety of the view. I


    def save(self):
        self.append_msg( "save()" )

        with open("data.json", "w") as f:
            data = json.dump(self.model.todos, f)



    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )
        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect()" )

        self_model         = self.model
        self_view     = self.view

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
        self.append_function_msg( "breakpoint()" )

        breakpoint()


# ---- eof