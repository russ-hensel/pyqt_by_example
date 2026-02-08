#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof


"""


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #qt_fitz_book.main()
# --------------------


#import inspect
#import json
import os
#import subprocess
import sys
import time
from   datetime import datetime
from   functools import partial
from   subprocess import PIPE, STDOUT, Popen, run
import webbrowser
import wat
from qtpy import QtGui
from qtpy.QtCore import (QAbstractListModel,
                          QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument, QIcon
# sql
from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
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
import tab_base

# ---- end imports

basedir = os.path.dirname(__file__)

tick    = QImage(os.path.join("tick.png"))

logger          = logging.getLogger( )

# Color scale, which is taken from colorbrewer2.org.
# Color range -5 to +5; 0 = light gray
# COLORS = [
#     "#053061",
#     "#2166ac",
#     "#4393c3",
#     "#92c5de",
#     "#d1e5f0",
#     "#f7f7f7",
#     "#fddbc7",
#     "#f4a582",
#     "#d6604d",
#     "#b2182b",
#     "#67001f",
# ]

# DONE_MSG        = ( "<<-- done\n" )
# INSPECT_MSG     = ( "inspect()"  )
# BREAK_MSG       = ( "breakpoint()" )

# tab_base.DONE_MSG

#  --------
class TabReBase( tab_base.TabBase ):
    def __init__(self):
        """
        some var for later use
        """
        super().__init__()

        self.help_file_name     =  "unknown.txt"
        #self._build_model()

        self.mutate_dict    = {}

        self.mutate_ix      = 0

        self.build_dict     = {}  # a list would suffice
        self.build_dict_msg = {}  # a list would suffice
        self.post_build_msg = []
        self.build_ix       = 0
        self.web_link_text       = "web_link not set"
        self.web_link   = "confusion continues"
        self.tab_layout     = None
        self.class_widget_text = "rebase_not_set"
        #self.help_file_set  = set()
        # _build_gui(self,   ): call from child
        self.ix_recursion   = 0
        self.my_next_layout_function  = None
            # replace with function that builds
            # desired part of gui

    #------------------------
    def post_init(self):
        """
        more init after child
        """
        # max_build_dict   = len( )
        self.set_help_file_name()
        self.next_gui_build()


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
        self.class_widget   = widget  # widget show classes or widgets on tab
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
        widget              = QTextEdit("load\nthis should be new row  build should change")
        self.msg_widget     = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget,   )

    # -------------------------------
    def build_gui_last_buttons(self, row_layout  ):
        """
        Builds the last buttons on the gui, part of the boilerplate


        self.build_gui_last_buttons(  row_layout  )

        Note this is a bit more verbose than it needs to be
        """

        # ---- "copy\nmod fn"
        widget              = QPushButton("copy\nmod fn")
        connect_to          = self.copy_module_file_name
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- wiki\nwiki
        widget              = QPushButton("wiki-\nwiki")
        connect_to          = self.wiki_wiki
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- "rebuild\ngui"
        widget = QPushButton("rebuild-\ngui")
        connect_to          = self.next_gui_build
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- inspect
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



    #---------------------
    def clear_layout( self, layout ):
        self.ix_recursion =+ 1
        if self.ix_recursion > 100:
            breakpoint()


        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            # Handle widgets
            if widget := item.widget():
                widget.disconnect()     # Disconnect all signals
                widget.setParent(None)  # Detach widget from layout
                widget.deleteLater()    # Schedule for deletion




            # Handle sub-layouts
            if item.layout():
                self.clear_layout( item.layout() )  # Recursively clear nested layout
            # Handle spacers or other items
            if item.spacerItem():
                # No need to delete spacers explicitly, just remove them
                pass
        # Delete the layout itself
        layout.deleteLater()

    #---------------------
    def replace_top_layout( self ):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        # self.tab_layout = layout
        # Step 1: Delete all widgets in the existing layout
        old_layout = self.layout
        self.clear_layout( self.layout() )
        # if old_layout is not None:
        #     self.setLayout(None)

        #self.finish_replace()
        QTimer.singleShot( 0, self.finish_replace )
        # #tab_page            = self
        # layout              = QVBoxLayout( self )
        # self.tab_layout     = layout
        # self.main_layout    = layout   # bit of confusion here

    # Now you can add new widgets to new_layout
    def finish_replace( self ):
        """ """
        layout              = QVBoxLayout(   )
        self.setLayout( layout )
        self.tab_layout     = layout
        self.main_layout    = layout   # bit of confusion here
        #layout     =  self.tab_layout  # from replace

        self._build_gui_top( layout )

        self.build_dict[ self.build_ix ]()

        row_layout = QHBoxLayout()
        layout.addLayout( row_layout )
        self.build_ntl_buttons( layout )   # next to last  expected in child
        self.build_gui_last_buttons( row_layout )

        self._build_gui_bot( layout )

        #self.build_dict_msg[ self.build_ix ]()
        self.class_widget.setText( self.class_widget_text )
        print( f"setText {self.class_widget_text}")
        self.display_post_build_msg()


        # ready for next post increment
        self.build_ix   += 1
        if self.build_ix >= len( self.build_dict ):
            self.build_ix = 0

    # ------------------------------------
    def display_post_build_msg( self,   ):
        """
        """
        if self.post_build_msg is not None:
            for ix_msg, i_msg in enumerate( self.post_build_msg ):
                if ix_msg == 0:
                    self.append_function_msg( i_msg, )
                else:
                    self.append_msg( i_msg )
            self.post_build_msg  = None
        else:
            return
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
    def next_gui_build( self ):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        # max_build_dict   = len( self.build_dict )

        self.replace_top_layout()

        # cannot continue build need to do in finish_replace
        # layout     =  self.tab_layout  # from replace

        # self._build_gui_top( layout )

        # self.build_dict[ self.build_ix ]()

        # row_layout = QHBoxLayout()
        # layout.addLayout( row_layout )
        # self.build_gui_last_buttons( row_layout )

        # self._build_gui_bot( layout )

        # # ready for next post increment
        # self.build_ix   += 1
        # if self.build_ix >= len( self.build_dict ):
        #     self.build_ix = 0

    # ------------------------------------
    def mutate( self ):
        """
        read it
            may not be used may come back
            loop throug the mutate functions
        """
        max_ix          = len( self.mutate_dict)
        self.mutate_dict[ self.mutate_ix ]()
        self.mutate_ix   += 1
        if self.mutate_ix >= max_ix:
            self.mutate_ix = 0

    #----------------------------
    def clear_msgxxx( self,  ):
        """
        read it --

        """
        self.msg_widget.clear()

    #----------------------------
    def append_function_msgxxxxx( self, msg, clear = True ):
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
    def append_msgxxxx( self, msg, clear = False ):
        """
        read it --
            and print to console
        """
        if clear:
            self.clear_msg(   )
        self.msg_widget.append( msg )
        print( msg )

    def set_web_linkxxxx( self, web_link ):
        """
        """
        breakpoint()
        self.web_link   = web_link


    # def wiki_wiki( self ):
    #     """
    #     """
    #     #webbrowser.open( self.web_link, new = 0, autoraise = True )
    #     webbrowser.open( self.wiki_link, new = 0, autoraise = True )


    #----------------------------
    def copy_module_file_name( self ):
        """
        """
        file_path           = Path( self.module_file )
        full_file_name      = str( file_path.resolve( ) )
        QApplication.clipboard().setText( full_file_name  )



# ---- eof