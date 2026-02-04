#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof

"""
KEY_WORDS:      book mouse events right click context menu fitzz

CLASS_NAME:     Fitz_3_Tab
WIDGETS:        QMenu Qt.LeftButton contextMenuEvent
STATUS:         2025  06 27 wip   contents needs review

TAB_TITLE:      Fitz Chapt 12 / MouseEvents

HOW_COMPLETE:   25  #  AND A COMMENT 2025  06 27 wip   contents needs review
DESCRIPTION:    Code motivated by Fitz Chapt 12 Events, needs completion...

"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/Fitz-Chapt-12-Events"
"""
chapt 12
Listing 61. basic/events_1.py
Listing 63. basic/events_3.py
Listing 64. basic/events_4.py


"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/events_1.py",
.../basic/events_1b.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/events_2.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/events_3.py",
"/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/events_4.py"
"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------


import inspect
import subprocess
import sys
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
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
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
# import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports


#  --------
class Fitz_3_Tab( tab_base.TabBase  ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link         = WIKI_LINK

        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_gui()


    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        # ----
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        widget          =  QLabel("Mouse around; Mouse Events ---> ")
        row_layout.addWidget( widget )

        widget         = QLabel( "mouse events come here 1 " )
        self.label_1   = widget
        row_layout.addWidget( widget )

        widget         = QLabel( "mouse events come here 2" )
        self.label_2   = widget
        row_layout.addWidget( widget )

        # mouse tracking on the whole tab page
        self.setMouseTracking(True)

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )


    def contextMenuEvent( self, e):
        """ """
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec_(e.globalPos())


    def mouseMoveEvent(self, e):

        self.label_1.setText("mouseMoveEvent")
        # deeper analysis in lable_2
        pos         = e.pos()
        global_pos  = e.globalPos()
        self.label_2.setText( "mouseMoveEvent: %s %s " % ( pos, global_pos ))


    def mousePressEvent(self, e):
        """ """
        self.label_1.setText("mousePressEvent")
        # deeper analysis in lable_2
        if e.button() == Qt.LeftButton:
            # handle the left-button press in here
            self.label_2.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            # handle the middle-button press in here.
            self.label_2.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            # handle the right-button press in here.
            self.label_2.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        """ """
        self.label_1.setText("mouseReleaseEvent")
        # deeper analysis in lable_2

        if e.button() == Qt.LeftButton:
            self.label_2.setText("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.label_2.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.label_2.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        """ """
        self.label_1.setText("mouseDoubleClickEvent")
        # deeper analysis in lable_2
        if e.button() == Qt.LeftButton:
            self.label_2.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.label_2.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.label_2.setText("mouseDoubleClickEvent RIGHT")

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        msg    = "so far not implemented "
        self.append_msg( msg,  )

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

        #self_widgets_list   = self.widgets_list
        wat_inspector.go(
             msg            = "see self_widgets_list",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )
    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint()" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof