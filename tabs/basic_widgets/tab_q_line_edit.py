#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

KEY_WORDS:      lineEdit     text
CLASS_NAME:     QLineEditTab
WIDGETS:        QLineEdit
STATUS:         revie me
TAB_TITLE:      QLineEdit / Reference
DESCRIPTION:    A reference for the QLineEdit widget
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QLineEdit"



# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------


import traceback
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
#import custom_widgets
import tab_base

# ---- end imports



#  --------
class QLineEditTab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage

        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        self.mutate_dict[2]    = self.mutate_2
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
        #button_layout        = QHBoxLayout(   )

        # lbl_stretch     = 0
        # widget_stretch  = 3

        # self.lbl_stretch     = lbl_stretch
        # self.widget_stretch  = widget_stretch
        # ---- new row
        row_layout       = QHBoxLayout( )
        layout.addLayout( row_layout )

        # # ---- edits --------------------------------
        # layout.addWidget( groupbox_edits )
        # g_layout            = QVBoxLayout( groupbox_edits  )
        widget            = QLabel( "QLineEdit_1")
        row_layout.addWidget( widget,  ) # stretch = lbl_stretch )

        widget            = QLineEdit(  self,   )
        widget.setReadOnly( False )
        self.line_edit_1_widget = widget
        row_layout.addWidget( widget,  ) # stretch = lbl_stretch )

        # ---- new row
        row_layout        = QHBoxLayout( )
        layout.addLayout( row_layout )

        widget            = QLabel( "QLineEdit_2")
        row_layout.addWidget( widget,  ) # stretch = lbl_stretch )

        widget            = QLineEdit(  self,   )
        self.line_edit_2_widget = widget
        row_layout.addWidget( widget,  ) # stretch = lbl_stretch )

        # ---- new row
        row_layout        = QHBoxLayout( )
        layout.addLayout( row_layout )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( row_layout )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        msg    = "so far just a little implemented "
        self.append_msg( msg, clear = False )

        # ---- change widget
        msg    = "mess with first line edit "
        self.append_msg( msg, clear = False )

        widget     = self.line_edit_1_widget
        widget.setText( "some text from setText" )
        widget.setEnabled( True )
        widget.setPlaceholderText( "some placeholder text ")
        widget.setToolTip( "what is a tooltop setToolTip ")

        # ---- change widget
        widget     = self.line_edit_2_widget
        msg     = "leave line_edit_2_widget in this mutation  "
        self.append_msg( msg,  )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )

        msg    = "so far a bit  implemented "
        self.append_msg( msg, clear = False )

        # ---- new widget
        widget     = self.line_edit_1_widget
        widget.setText( "some text from setText in mutate_1()" )

        msg    = "disable line edit 1"
        self.append_msg( msg, clear = False )

        widget.setEnabled( False )

        widget.setPlaceholderText( "some placeholder text mutate_1()")
        widget.setToolTip( "setToolTip for mutate_1()")

        # ---- new widget
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2()" )
        msg    = "so far a bit  implemented "
        self.append_msg( msg, clear = False )

        msg    = "mess with QLineEdit_1 different than mutate_0()"
        self.append_msg( msg, clear = False )
        # ---- new widget
        widget     = self.line_edit_1_widget
        widget.setText( "some text from setText in mutate_1()" )

        msg    = "enable line edit 1"
        self.append_msg( msg, clear = False )

        widget.setEnabled( True )

        # ---- new widget
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect()" )

        # make some locals for inspection

        parent_window = self.parent( ).parent( ).parent().parent()

        self_line_edit_1_widget = self.line_edit_1_widget
        self_line_edit_2_widget = self.line_edit_2_widget

        wat_inspector.go(
             msg            = "for your inspection, inc. locals and globals",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        self.append_function_msg( "breakpoint()" )
        breakpoint()

        self.append_msg( tab_base.DONE_MSG )
# ---- eof
