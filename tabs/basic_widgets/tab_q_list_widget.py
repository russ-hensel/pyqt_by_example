#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""

KEY_WORDS:      list widget  dc
CLASS_NAME:     QListWidgetTab
WIDGETS:        QListWidget
STATUS:
TAB_TITLE:      QListWidget Reference
HOW_COMPLETE:   25  #  AND A COMMENT 2025-07-02:DAV


"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
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

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

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

#import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.



#  --------
class QListWidgetTab( tab_base.TabBase ) :
    def __init__(self):
        """
        the usual
        tab_list_widget.py
        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        self.help_file_name      =  "list_widget_tab.txt"
        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        # ---- QListWidget
        widget              = QListWidget(    )
        self.list_widget_1  = widget
        widget.setGeometry( 50, 50, 200, 200 )
        layout.addWidget( widget )

        widget.itemClicked.connect( self.list_clicked )

        values    =  [ "one", "two"]
        for value in values:
            item = QListWidgetItem( value )
            widget.addItem( item )

        widget.clear()

        values    =  [ "oneish", "twoish", "threeish"]
        for value in values:
            item = QListWidgetItem( value )
            widget.addItem( item )
            index_to_select = 2
            widget.setCurrentRow(index_to_select)

        # --- buttons
        layout.addLayout( button_layout,  )

        #button_layout.addWidget( widget )

        widget = QPushButton("mutate\n")
        self.button_ex_1         = widget
        widget.clicked.connect( lambda: self.mutate( ) )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget = QPushButton("inspect\n")
        widget.clicked.connect( self.inspect    )
        button_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton("breakpoint\n")
        widget.clicked.connect( self.breakpoint    )
        button_layout.addWidget( widget,   )

    # --------------------
    def list_clicked( self, item ):
        """
        when the list is clicked get the text
        """
        self.append_function_msg( "list_clicked" )

        widget        = self.list_widget_1
        row           = widget.row(item)

        text = item.text()
        self.append_msg( f"Clicked row: {row}, text: {text}")

        self.append_msg( "list_clicked done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        widget.setGeometry( 50, 50, 200, 200 )
      def hasHeightForWidth(…) # hasHeightForWidth(self) -> bool
      def height(…) # height(self) -> int
      def heightForWidth(…) # heightForWidth(self, a0: int) -> int
      def heightMM(…) # heightMM(self) -> int
      def maximumHeight(…) # maximumHeight(self) -> int
      def minimumHeight(…) # minimumHeight(self) -> int
      def setFixedHeight(…) # setFixedHeight(self, h: int)
      def setMaximumHeight(…) # setMaximumHeight(self, maxh: int)
      def setMinimumHeight(…) # setMinimumHeight(self, minh: int)

        """
        self.append_function_msg( "mutate_0" )

        # msg    = "so far not implemented "
        # self.append_msg( msg, clear = False )
        #self.list_widget_1  # = widget

        msg    = "self.list_widget_1.setMaximumHeight( 50 )"
        self.append_msg( msg, clear = False )
        self.list_widget_1.setMaximumHeight( 50 ) # setMaximumHeight(self, maxh: int)

        self.append_msg( "mutate_0 done" )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "self.list_widget_1.setMaximumHeight( 200 )"
        self.append_msg( msg, )
        self.list_widget_1.setMaximumHeight( 200 ) # setMaximumHeight(self, maxh: int)

        # sortingEnabled doesn't seem to do anything. It does nothing!

        msg    = "self.list_widget_1.sortingEnabled=True #"
        self.append_msg( msg, )
        self.list_widget_1.sortingEnabled=True #
        self.append_msg( f"{self.list_widget_1.isSortingEnabled()=}" )
        self.append_msg( "Note discrepancy -- isSortingEnabled() returns false, isn't that weird?")

        self.append_msg( "mutate_1 done" )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2" )

        # msg    = "so far not implemented "
        # self.append_msg( msg, clear = False )

        self.append_msg( f"{self.list_widget_1.sortingEnabled=}" )

        # msg    = "self.list_widget_1.sortingEnabled=False #"
        # self.append_msg( msg, )
        # self.list_widget_1.sortingEnabled=False #

        self.append_msg( f"{self.list_widget_1.sortingEnabled=}" )
        self.append_msg( f"{self.list_widget_1.isSortingEnabled()=}" )

        self.append_msg( "self.list_widget_1.addItem( item ) # Another thing on the list" )
        item = QListWidgetItem( "Another thing on the list" )
        self.list_widget_1.addItem( item )

        self.append_msg( "mutate_2 done" )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_3" )

        # msg    = "so far not implemented "
        # self.append_msg( msg, clear = False )



        msg    = "self.list_widget_1.sortItems() #"
        self.append_msg( msg, )
        self.list_widget_1.sortItems() #

        self.append_msg( "mutate_3 done" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        self_list_widget_1  = self.list_widget_1
        wat_inspector.go(
             msg            = "from inspect method",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "inspect done" )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( "breakpoint done" )

# ---- eof