#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""

tab_q_groupbox.py



KEY_WORDS:      group collect widgets
CLASS_NAME:     QGroupBoxTab
WIDGETS:        QGroupBox  StyleSheet
STATUS:         runs_correctly_5_10
TAB_TITLE:      QGroupBox / Reference
DESCRIPTION:    A reference for the QGroupBox widget
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby

"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QGroupBox "
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #qt_fitz_book.main()
# --------------------VERBOSE

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
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

# import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports



INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.




#  --------
class QGroupBoxTab( tab_base.TabBase  ) :
    def __init__(self):
        """
        setup except for gui
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

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )

        # ---- QGroupBox
        #groupbox   = QGroupBox()  # no title
        groupbox   = QGroupBox( "QGroupBox 1" )   # version with title

        groupbox.setStyleSheet("""
            QGroupBox {
                border: 2px solid blue;
                border-radius: 10px;
                margin-top: 15px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: white;
            }
        """)

        # layout the groupbox and make
        # another layout inside it

        layout.addWidget( groupbox )
        layout_b     = QHBoxLayout( groupbox  )

        self.build_gui_in_groupbox( layout_b )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # ---------------------------
    def build_gui_in_groupbox( self, layout ):
        """
        this is a bit of gui built inside another groupbos = QGroupBox()
        """
        widget = QPushButton("do_nothing\n")
        #widget.clicked.connect(  self.show_values  )
        layout.addWidget( widget )

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
        self.append_function_msg(  "inspect()" )

        # make some locals for inspection
        my_tab_widget = self
        #parent_window = self.parent( ).parent( ).parent().parent()

        wat_inspector.go(
             msg            = "self.text_edit from inspect method",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg(  "breakpoint()" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
