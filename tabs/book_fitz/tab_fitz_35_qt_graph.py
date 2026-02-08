#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----tof
"""
KEY_WORDS:      book a dynamic graph  fitzz
CLASS_NAME:     Fitz_5_Tab
WIDGETS:        QTimer pg.PlotWidget pg.mkPen
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      Fitz Chapt 35 / Dynamic Plot
DESCRIPTION:    Code motivated by Fitz 35 Dynamic Plot
HOW_COMPLETE:   25  #  AND A COMMENT

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Fitz-Chapt-35-Qt-Graph"
#WIKI_LINK     =  "https://github.com/russ-hensel/qt5_by_example/wiki/Fitz-Chapt-12-Events"

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
class Fitz_5_Tab( tab_base.TabBase ) :
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

        self.timer = QTimer()
        self.timer.setInterval(50)
        self._build_gui()

        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def _build_gui_widgets(self, main_layout  ):
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

        self.x = list(range(100))  # 100 time points
        self.y = [
            randint(0, 100) for _ in range(100)
        ]  # 100 data points

        self.graphWidget.setBackground("w")

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(
            self.x, self.y, pen=pen
        )  # <1>

        # ---- new row
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ---- PB "start\n"
        widget = QPushButton("start\n")
        widget.clicked.connect( self.start    )
        row_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton("stop\n")
        widget.clicked.connect( self.stop    )
        row_layout.addWidget( widget,   )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( row_layout )

    # ------------------------
    def start(self):
        """ """
        self.append_function_msg( "start" )

        self.timer.start()
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def stop(self):
        """ """
        self.append_function_msg( "stop" )

        self.timer.stop()
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(
            self.x[-1] + 1
        )  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )
        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )
        self.append_msg( tab_base.DONE_MSG )

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
        self_timer          = self.timer
        wat_inspector.go(
             msg            = "items to inspectr",
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