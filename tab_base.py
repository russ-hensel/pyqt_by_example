#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof


"""
Base class for demo tabs

this is pretty much infrastructure for the application
not part of the widget examples

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------


#import inspect
#import json
import os
#import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run
import webbrowser
#import wat
from pathlib import Path
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
from PyQt5.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument, QIcon

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel

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
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import global_vars
# ---- imports neq qt
import logging

# ---- end imports

basedir     = os.path.dirname(__file__)

tick        = QImage(os.path.join("tick.png"))

logger      = logging.getLogger( )

# Color scale, which is taken from colorbrewer2.org.
# Color range -5 to +5; 0 = light gray
COLORS = [
    "#053061",
    "#2166ac",
    "#4393c3",
    "#92c5de",
    "#d1e5f0",
    "#f7f7f7",
    "#fddbc7",
    "#f4a582",
    "#d6604d",
    "#b2182b",
    "#67001f",
]

DONE_MSG        = ( "<<-- done\n" )
INSPECT_MSG     = ( "inspect()"  )
BREAK_MSG       = ( "breakpoint()" )
NO_MUTATE_MSG   = ( "no mutations for this tab")

# tab_base.DONE_MSG

#  --------
class TabBase( QWidget ):
    def __init__(self):
        """
        some var for later use
        """
        super().__init__()

        self.help_file_name     =  "unknown.txt"
        #self._build_model()
        self.web_link           = "web_link not set"
        self.mutate_dict        = {}
        self.mutate_ix          = 0    # set two plaes by mistahk !! ??
        self.help_file_set      = set()
        # self.module_file_name   = "not_set"
        # _build_gui(self,   ): call from child

    # -------------------------------
    def _build_gui(self,   ):
        """

        for the first 2 tabs
        layouts
            a vbox for main layout
            h_box for or each row of widgets
        """
        tab_page      = self
        layout        = QVBoxLayout( tab_page )

        self._build_gui_top(     layout )
        self._build_gui_widgets( layout )
        self._build_gui_bot(     layout )
        self.mutate_0()
        self.mutate_ix = 0   # this is the last run, next + 1

        self.set_help_file_name()

    # -------------------------------
    def _build_gui_top( self, layout ):
        """
        layouts
            a vbox for main layout
            h_box for or each row of widgets
        """
        # ---- new row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        widget              = QLabel( "classes...... on this tab" )
        self.class_widget   = widget  # widget showin calsses or widgets on tab
        row_layout.addWidget( widget,   )

    # -------------------------------
    def _build_gui_bot(self, layout  ):
        """
        make the bottom of the gui, mostly the large
        message widget
        layouts
            a vbox for main layout
        """
        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ----
        widget              = QTextEdit("load\nthis should be new row ")
        self.msg_widget     = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget,   )

    # -------------------------------
    def build_gui_last_buttons(self, row_layout  ):
        """
        self.build_gui_last_buttons(  row_layout  )
        """
        # ---- "copy\nmod fn"
        widget              = QPushButton("copy\nmodule fn")
        connect_to          = self.copy_module_file_name
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- wiki\nwiki
        widget              = QPushButton("wiki-\nwiki")
        connect_to          = self.wiki_wiki
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- mutate
        widget              = QPushButton("mutate-\nexamine")
        #self.button_ex_1    = widget
        widget.clicked.connect( lambda: self.mutate( ) )
        row_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("wat-\ninspect")
        connect_to          = self.inspect
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- PB breakpoint
        if global_vars.CONTROLLER.breakpoint_ok:
            widget              = QPushButton("breakpoint-\ndebug")
            connect_to          = self.breakpoint
            widget.clicked.connect( connect_to )
            row_layout.addWidget( widget )

    # ------------------------------------
    def set_help_file_name( self,   ):
        """
         read it
             check for dups and warn !!

         !! move help file to the dir where the class file is

         """

        splits                 = self.module_file .split( "/" )
        #self.help_file_name    = splits[ 1 ].replace( ".", "__") + ".txt"
        #self.help_file_name    = splits[ 1 ] + ".txt"

        file_path           = "/".join( splits[ 0:-1 ]  )
        print( f"{file_path =}" )
        file_name           = splits[ -1 ].split( "." )[0] + ".txt"
        print( f"{file_name =}" )
        #file_name           =  file_path + "/help/" + file_name
        file_name           =  file_path +  "/" + file_name
        print( f"{file_name =}" )

        self.help_file_name =  file_name

        msg    = (f"tab_checkbox.set_help_file_name() we have a "
                  f"help file {self.help_file_name = } ")
        logging.debug( msg )

    # ------------------------------------
    def mutate( self ):
        """
        read it
            loop throug the mutate functions
        """
        max_ix          = len( self.mutate_dict)
        self.mutate_ix   += 1
        if self.mutate_ix >= max_ix:
            self.mutate_ix = 0
        self.mutate_dict[ self.mutate_ix ]()

    #----------------------------
    def clear_msg( self,  ):
        """
        read it --

        """
        self.msg_widget.clear()

    #----------------------------
    def append_function_msg( self, msg, clear = True ):
        """
        read it --
            and print to console
        msg is just the name of the function
        """
        msg     = f"----==== {msg} ====----"
        if clear:
            self.clear_msg(  )

        self.msg_widget.append( msg )
        print( msg )

    #----------------------------
    def append_msg( self, msg, clear = False ):
        """
        read it --
            and print to console
        """
        if clear:
            self.clear_msg(   )
        self.msg_widget.append( msg )
        print( msg )

    #----------------------------
    def set_web_link( self, web_link ):
        """ """
        self.web_link   = web_link

    #----------------------------
    def wiki_wiki( self ):
        """
        open the wiki page for the tab
        """
        webbrowser.open( self.wiki_link, new = 0, autoraise = True )

    #----------------------------
    def copy_module_file_name( self ):
        """
        """
        file_path           = Path( self.module_file )
        full_file_name      = str( file_path.resolve( ) )
        QApplication.clipboard().setText( full_file_name  )
        # and put in message area
        msg      = ( f"module file name is ( in clipboard ) \n  >>> {full_file_name} <<<")
        self.append_msg( msg )

# ---- eof

