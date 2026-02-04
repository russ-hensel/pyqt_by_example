#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY_WORDS:      label widget
CLASS_NAME:     QLabelTab
WIDGETS:        QLabel
STATUS:         ??
TAB_TITLE:      QLabel salvage XXXXX
DESCRIPTION:    This is all wrong, for salvage only



TAB_HELPxx:       combo_box_widget_tab.txt


self.help_file_name     =  "combo_box_widget_tab.txt"
/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/docs/combo_box_widget_tab.txt
"""
# ---- tof

x = 1/0
# FIXME: merge into tab_label.py

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

import parameters
import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports


#  --------
class QLabelTab( tab_base.TabBase  ) :


    # ----------------------------------------------
    def _build_gui_widgets(self, main_layout  ):


        # ---- label_1
        widget        = QLabel( "label_1 ")
        self.label_1  = widget

        # these work but in some case seem only to work with a lambda
        # widget.currentIndexChanged.connect( self.conbo_currentIndexChanged )
        # widget.currentTextChanged.connect(  self.combo_currentTextChanged  )

        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        row_layout.addWidget( widget )

        # ---- label_1
        widget        = QLabel( "label_2 ")
        self.label_2  = widget

        # these work but in some case seem only to work with a lambda
        # widget.currentIndexChanged.connect( self.conbo_currentIndexChanged )
        # widget.currentTextChanged.connect(  self.combo_currentTextChanged  )

        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        row_layout.addWidget( widget )


        # ---- buttons
        # button_layout = QHBoxLayout(   )
        # layout.addLayout ( button_layout )
        # # --- buttons
        # label       = "combo\n_reload"
        # widget = QPushButton( label )
        # widget.clicked.connect( self.combo_reload )

        # button_layout.addWidget( widget )





    # --------------------------
    def inspect_old( self, arg  ):
        """
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        self.append_function_msg( "inspect_old" )
        self.append_msg( f"combo_info { '' }  --------", flush = True )

        widget         = self.combo_1

        info           = widget.count()
        msg            = f"widget.count() {info}"
        self.append_msg( msg )

        info           = widget.currentData()    # seem to always get None
        msg            = f"widget.currentData() {info}"
        self.append_msg( msg )

        # qt5 not working for me
        # info           = widget.editable
        # msg            = f".editable {info}"
        # print( msg )

        info           = widget.currentText()  # is good
        msg            = f".currentText() {info}"
        self.append_msg( msg )

        info           = widget.currentIndex()
        msg            = f".currentIndex() {info}"
        self.append_msg( msg )

        info           = widget.placeholderText()
        msg            = f".placeholderText() {info}"
        self.append_msg( msg )

        self.show_combo_values()   # move this code here

        self.append_msg( f"combo_info end { '' } --------", flush = True )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_0( self ):

        msg      = "set text for lable_1"
        self.append_msg( msg )
        self.label_1.setText( "mutate_0 self.label_1.setText" )

    # ------------------------------------
    def mutate_1( self ):
        

# ---- eof