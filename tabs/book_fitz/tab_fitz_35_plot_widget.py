#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
could use a rename to chapter of the book


KEY_WORDS:      line graph  with points of static data chapter     rsh
CLASS_NAME:     Fitz_6_Tab
WIDGETS:        PlotWidget PyQtGraph pg.PlotWidget pg.mkPen  Grid Range
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      Fitz_Chapt 35 / Plot Widget x A_Tab
DESCRIPTION:    Code motivated by Fitz 35 Dynamic Plot
HOW_COMPLETE:   15  #  AND A COMMENT

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Documentation-Not-Written"
"""


in chapter 35
Listing 181. plotting/pyqtgraph_1.py
Listing 182. plotting/pyqtgraph_2.py
Listing 183. plotting/pyqtgraph_3.py


probably not
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

#import parameters
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports



basedir = os.path.dirname(__file__)


#  --------
class Fitz_6_Tab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_gui()

    def _build_gui_widgets( self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        #button_layout        = QHBoxLayout(   )

        widget              = pg.PlotWidget()
        self.graphWidget    = widget
        layout.addWidget( self.graphWidget )

        self.graphWidget.setBackground("w")

        pen = pg.mkPen(color=(255, 0, 0))

        # Add Background color to white
        self.graphWidget.setBackground("w")  # w = white

        self.graphWidget.setTitle(
            "Your Title Here", color="b", size="30pt"
        )
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Temperature (°C)", **styles)
        self.graphWidget.setLabel("bottom", "Hour (H)", **styles)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        self.graphWidget.setXRange(0,  10, padding=0)
        self.graphWidget.setYRange(20, 55, padding=0)

        # ---- new row
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- PB clear
        widget = QPushButton("clear_data\n")
        widget.clicked.connect( self.clear_data        )
        row_layout.addWidget( widget,   )

        # ---- PB plot
        widget = QPushButton("plot\n")
        widget.clicked.connect( self.plot    )
        row_layout.addWidget( widget,   )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( row_layout )





    def plot(self,  ):
        """ """
        self.append_function_msg( "plot" )

        hour            = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature_1   = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        temperature_2   = [50, 35, 44, 22, 38, 32, 27, 38, 32, 44]

        self.plot_data(hour, temperature_1, "Sensor1", "r")
        self.plot_data(hour, temperature_2, "Sensor2", "b")

        self.append_msg( tab_base.DONE_MSG )

    #-------------------------------
    def clear_data(self, x, y, plotname, color):
        """ """
        self.append_function_msg( "clear_data" )
        self.graphWidget.clear()
        self.append_msg( "clear_data complete" )

        self.append_msg( tab_base.DONE_MSG )

    #-------------------------------
    def plot_data(self, x, y, plotname, color):
        """ """
        self.append_function_msg( "plot_data" )

        pen = pg.mkPen(color=color)
        self.graphWidget.plot(
            x,
            y,
            name=plotname,
            pen=pen,
            symbol="+",
            symbolSize=30,
            symbolBrush=(color),
        )

        self.append_msg( tab_base.DONE_MSG )

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

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        self_graph_widget   = self.graphWidget

        wat_inspector.go(
             msg            = "items to inspect",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
