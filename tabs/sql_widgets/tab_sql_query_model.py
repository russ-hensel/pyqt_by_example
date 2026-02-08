#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
self.help_file_name     =  "sql_query_model_tab.txt"

KEY_WORDS:      sql query model select update delete crud rh
CLASS_NAME:     SqlQueryModelTab
WIDGETS:        QSqlQueryModel  QTableWidget
STATUS:         works -- but unclear what it is trying to do and seems incomplete --- possibly a dup, look before fixing
TAB_TITLE:      SqlQuery / Model
HOW_COMPLETE:   5  #  AND A COMMENT
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QSqlQuery"
"""
What We Know About QSqlQuery · russ-hensel/pyqt_by_example Wiki
https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QSqlQuery

or
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import mai
# --------------------

"""




import inspect
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from random import randint
from subprocess import PIPE, STDOUT, Popen, run

import pyqtgraph as pg  # import PyQtGraph after PyQt5
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
# sql
from qtpy.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
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

import utils_for_tabs as uft
import wat_inspector
import tab_base



# ---- end imports



basedir = os.path.dirname(__file__)

print( "salvaged but not functional is it a dup ??")

#  --------
class SqlQueryModelTab( tab_base.TabBase ) :
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

        # self.timer = QTimer()
        # self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()
        self._build_gui()

    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        table_widget        = QTableWidget(4, 5)  # row, column ??third arg parent
        self.table_widget   = table_widget
        layout.addWidget( table_widget )

        # ---- new row
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

     # --------------------------------
    def run_it( self, ):
        """
        from chat
        """
        #def loop_through_rows():
        """Loop through rows using QSqlQueryModel."""

        print( "need !! to set in db connect ")
        model = QSqlQueryModel( )

        # Set the query to fetch data from the 'people' table
        model.setQuery("SELECT * FROM people")

        # or
        model.setQuery("SELECT name, age FROM people")

        if model.lastError().isValid():
            print("Error: ", model.lastError().text())
            return

        for row in range(model.rowCount()):
            # Extract data from each column in the current row
            row_data = []
            for col in range(model.columnCount()):
                row_data.append( model.data(model.index(row, col)))

            print(f"Row {row + 1}: {row_data}")

    # ------------------------
    # def start(self):
    #     """ """
    #     print_func_header( "start" )
    #     return
    #     self.timer.start()

    # # ------------------------
    # def stop(self):
    #     """ """
    #     print_func_header( "stop" )
    #     return

    #     self.timer.stop()

    # # ------------------------
    # def update_plot_data(self):

    #     pass
    #     return

    #     self.x = self.x[1:]  # Remove the first y element.
    #     self.x.append(
    #         self.x[-1] + 1
    #     )  # Add a new value 1 higher than the last.

    #     self.y = self.y[1:]  # Remove the first
    #     self.y.append(randint(0, 100))  # Add a new random value.

    #     self.data_line.setData(self.x, self.y)  # Update the data.
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

        # self_graph_widget   = self.graphWidget
        # self_timer          = self.timer
        wat_inspector.go(
             msg            = "sql query model tab",
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