#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""

KEY_WORDS:      book many misc simple widgets ddl rsh
CLASS_NAME:     FitzWidgetListTab
WIDGETS:        QCheckBox QComboBox QDateEdit QDateTimeEdit QDial QDoubleSpinBox QFontComboBox QLCDNumber QLineEdit
STATUS:         file name seems good
TAB_TITLE:      Fitz Chapt  7 / Widgets widgets_list
DESCRIPTION:    Code motivated by Fitz section 7 Widgets widgets_list.py
HOW_COMPLETE:   25  #  AND A COMMENT
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Fitz-7-Widgets-List"


"""
Fitz 7.Widgets widgets_list.py · russ-hensel/pyqt_by_example Wiki
https://github.com/russ-hensel/pyqtby_example/wiki/Fitz-7.Widgets-widgets_list.py

Use as model for Fitz tabs
from:
/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/widgets_list.py
  widgets_list.py

Create GUI Applications with Python & Qt5
The hands-on guide to making apps with Python
Martin Fitzpatrick
Version 4.0, 2020-09-12

search for Fitz 7.Widgets widgets_list.py

rename to tab_fitz_7_widgets_list.py  ??


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------

# ---- imports
#import inspect
#import subprocess
#import sys
#import time
#from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run


from qtpy import QtGui
from qtpy.QtCore import (QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QPalette, QTextCursor, QTextDocument
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

import wat

# ---- local imports
import parameters
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports


#  --------
class FitzWidgetListTab( tab_base.TabBase ) :
    def __init__(self):
        """
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()

        self.module_file       = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

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

        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        self.widgets_list   = widgets   # for inspection later

        for w in widgets:
            layout.addWidget(w())

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        self.build_gui_last_buttons( button_layout )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        msg    = "no implementation planned for this tab, because book does not contain that content "
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
        self.append_function_msg( "inspect" )

        self_widgets_list   = self.widgets_list
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