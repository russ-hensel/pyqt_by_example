#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:41:16 2024

"""
"""

KEY_WORDS:      main window, links back to gui for app
CLASS_NAME:     MainWindowTab
WIDGETS:        QMainWindow QIcon QTabWidget QAction QMessageBox
STATUS:         unknown
TAB_TITLE:      QMainWindow

         self.help_file_name     =  "find_this_file.txt"

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------


# ---- tof
# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import qt_fitz_book
#     qt_fitz_book.main()
# # --------------------


import glob
import inspect
import json
import math
import os
import subprocess
import sys
import time
from collections import namedtuple
from datetime import datetime
from functools import partial
from random import randint
from subprocess import PIPE, STDOUT, Popen, run

import pyqtgraph as pg  # import PyQtGraph after PyQt5
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
from PyQt5.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
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

import utils_for_tabs as uft
import wat_inspector
import custom_widgets
import global_vars




# ---- end imports

print_func_header   = uft.print_func_header



#  --------
class MainWindowTab( QWidget ) :
    def __init__(self):
        """
        the usual
        """
        super().__init__()
        self.help_file_name     =  uft.to_help_file_name( __name__ )

        #self.help_file_name     =  "find_this_file.txt"
        self._build_gui()


    def _build_gui(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int

        edits

        criteria

        """
        tab_page        = self
        lbl_stretch     = 0
        widget_stretch  = 3

        self.lbl_stretch     = lbl_stretch
        self.widget_stretch  = widget_stretch


        layout              = QVBoxLayout( tab_page )

        msg     = """
        This tab does not illustrate a main window,
        instead the main window of the whole application does.
        So mess with the application and use the inspect and
        breakpoint buttons which examine the main window, not this tab.
        """


        widget              = QLabel( msg )
        # connect_to          = global_vars.CONTROLLER.inspect
        # widget.clicked.connect( connect_to )
        layout.addWidget( widget )



        button_layout       = QHBoxLayout( )

        # ---- buttons
        layout.addLayout ( button_layout )






        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to          = global_vars.CONTROLLER.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = global_vars.CONTROLLER.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )




# ---- eof