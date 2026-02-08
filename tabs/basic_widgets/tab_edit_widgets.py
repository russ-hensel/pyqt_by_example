#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
Created on Sun Dec 15 12:41:16 2024
no it is one listed twice


KEY_WORDS:      basic edits often used for forms seems to be some confusion 2 versions custom or not
CLASS_NAME:     EditWidgetTab
WIDGETS:        LineEdit TextEdit  DateEdit
STATUS:         !! runs    runs_correctly  demo_partial   demo_complete
TAB_TITLE:      EditWidgets

         self.help_file_name     =  "find_this_file.txt"

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Documentation-Not-Written"

# ---- search
"""
    Search for
        QLineEdit
        QTextEdit
        readOnly
"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
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
from qtpy.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument
# sql
from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
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
import tab_base

# ---- end imports



# --------------------------------
def set_groupbox_style( groupbox ):
    """ """
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

#  --------
class EditWidgetTab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage
        self.help_file_name    =  uft.to_help_file_name( __name__ )

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

        lbl_stretch     = 0
        widget_stretch  = 3

        self.lbl_stretch     = lbl_stretch
        self.widget_stretch  = widget_stretch


        # groupbox_criteria   = QGroupBox( "Criteria" )
        # set_groupbox_style( groupbox_criteria )

        groupbox_edits      = QGroupBox( "Edits" )
        set_groupbox_style( groupbox_edits )

        button_layout       = QHBoxLayout( )

        layout.addWidget( groupbox_edits )
        g_layout            = QVBoxLayout( groupbox_edits  )

        # # ---- edits --------------------------------
        # layout.addWidget( groupbox_edits )
        # g_layout            = QVBoxLayout( groupbox_edits  )
        self._build_gui_in_gb_edit( g_layout )

        # # ---- criteria --------------------------------
        # layout.addWidget( groupbox_criteria )
        # g_layout            = QVBoxLayout( groupbox_criteria  )
        # self._build_gui_in_gb_criteria( g_layout )

        # ---- buttons
        layout.addLayout( button_layout )

        label       = "mutate\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.mutate )
        button_layout.addWidget( widget )

        # label       = "validate\n"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.validate )
        # button_layout.addWidget( widget )



        # label       = "examine_0\n"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.examine_0 )
        # button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to        = self.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = self.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

    # ------------------------
    def _build_gui_in_gb_edit(self, layout  ):
        """
        build some of the gui in a groupbox
        """
        lbl_stretch         = self.lbl_stretch
        widget_stretch      = self.widget_stretch

        # ---- CQLineEdit
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QLineEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = QLineEdit(  self,   )
        widget.setReadOnly( False )
        self.line_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQLineEdit_2
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QLineEdit_2")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.QLineEdit(  self,   )
        self.line_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQTextEdit
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QTextEdit")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget              = custom_widgets.QTextEdit(  self,  )
        self.text_edit_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )


        # ---- CQDateEdit_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QDateEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget              = custom_widgets.CQDateEdit(  self,   )
        self.date_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateEdit_n
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QDateEdit_n:")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.QDateEdit(  self,   )
        self.date_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = self.widget_stretch )

    # --------------------------
    def mutate_to_refactro( self, arg  ):
        """
        What it says
        """
        self.append_function_msg( f"mutate { self.mutate_ix = }" )

        max_mutate   = 3   # match to if.......
        mutate_ix    = self.mutate_ix

        if   mutate_ix == 0:

            self.text_edit_widget.setText( f"{mutate_ix=}" )
            data   = self.text_edit_widget.toPlainText()
            msg         = f"set then get from self.text_edit_widget {data = }"
            print( msg )

            self.line_edit_1_widget.setText(  f"{mutate_ix=}" )  #
            rdata    = self.line_edit_1_widget.text(  )
            msg         = f"set then get from line_edit_1 {data = }"
            self.append_msg( msg )

            # # this is the general method
            # in_data      = f"some string data {mutate_ix =}"
            # in_type      = "string"             # a list includes  string  "integer", "timestamp" ):
            # self.text_edit_widget.set_data(   in_data, in_type )

        elif mutate_ix == 1:

            self.text_edit_widget.setText( f"{mutate_ix=}" )

            data   = self.text_edit_widget.toPlainText()
            msg         = f"set then get from self.text_edit_widget {data = }"
            self.append_msg( msg )

            self.line_edit_1_widget.setText(  f"{mutate_ix=}" )  #
            rdata    = self.line_edit_1_widget.text(  )
            msg         = f"set then get from line_edit_1 {data = }"
            print( msg )


            # # this is the general method
            # in_data      = f"some string data {mutate_ix =}"
            # in_type      = "string"             # a list includes  string  "integer", "timestamp" ):
            # self.text_edit_widget.set_data(   in_data, in_type )

        elif self.mutate_ix == 2:
            msg      = "set to none and like"
            self.append_msg( msg )

            self.text_edit_widget.setText( f"{mutate_ix=} for set to None" )

            try:
                self.line_edit_1_widget.setText( None )

            except Exception as an_except:
                self.append_msg( " " )
                msg     = f"a_except    >>{an_except}<<  type  >>{type( an_except)}<<"
                self.append_msg( msg )

                msg     = "self.line_edit_1_widget.setText( None ) raised this "
                self.append_msg( msg )



        elif self.mutate_ix == 3:
            self.text_edit_widget.set_preped_data( f"{mutate_ix=} set -> xxx -> None" )

            self.text_edit_widget.set_preped_data( "xxx" )
            self.line_edit_1_widget.set_preped_data( None )
            raw_data    = self.line_edit_1_widget.get_raw_data(  )
            msg         = f"set then get from text_edit_widget {raw_data = }"
            self.append_msg(  msg )


            self.line_edit_1_widget.set_preped_data( "xxx" )
            self.line_edit_1_widget.set_preped_data( None )
            #self.line_edit_1_widget.setText( None  )   #
            raw_data    = self.line_edit_1_widget.get_raw_data(  )
            msg         = f"set then get from line_edit_1 {raw_data = }"
            self.append_msg( msg )

            # this is the general method
            in_data      = f"some string data {mutate_ix =}"
            in_type      = "string"             # a list includes  string  "integer", "timestamp" ):
            self.text_edit_widget.set_data(   in_data, in_type )

        self.mutate_ix         += 1
        if self.mutate_ix >= max_mutate:
            msg   = f"hit {max_mutate = } wrap to 0 *******"
            self.append_msg(  msg )
            self.mutate_ix  = 0



    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far just a little implemented "
        self.append_msg( msg, clear = False )

        msg    = "mess with first line edit "
        self.append_msg( msg, clear = False )

        widget     = self.line_edit_1_widget
        widget.setText( "some text from setText" )
        widget.setEnabled( True )
        widget.setPlaceholderText( "some placeholder text ")
        widget.setToolTip( "what is a tooltop setToolTip ")

        self.append_msg( "mutate_0 done" )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )
        msg    = "so far a bit  implemented "
        self.append_msg( msg, clear = False )

        msg    = "mess with QLineEdit_1 different than mutate_0"
        self.append_msg( msg, clear = False )

        widget     = self.line_edit_1_widget
        widget.setText( "some text from setText in mutatate_1" )

        msg    = "disable line edit 1"
        self.append_msg( msg, clear = False )

        widget.setEnabled( False )
        widget.setPlaceholderText( "some placeholder text mutate_1")
        widget.setToolTip( "setToolTip for mutate_1")

        self.append_msg( "mutate_1 done" )


    # --------------------------
    def set_to_nonexxx( self, arg  ):
        """
        !!What it says
        """
        self.append_function_msg( "set_to_none" )

        self.line_edit_1_widget.set_preped_data( "xxx" )
        self.line_edit_1_widget.set_preped_data( None )
        self.line_edit_1_widget.setText( None  )   #
        raw_data    = self.line_edit_1_widget.get_raw_data(  )
        msg         = f"set then get from line_edit_1 {raw_data = }"
        self.append_msg( msg )

        print()
        self.line_edit_2_widget.set_preped_data( "xxx" )
        self.line_edit_2_widget.set_preped_data( None )
        self.line_edit_2_widget.setText( None  )
        msg         = f"{self.line_edit_2_widget.get_raw_data(  ) = }"
        self.append_msg( msg )

        try:
            self.date_edit_1_widget.set_preped_data( None )

        except Exception as an_except:
            print()
            msg     = f"a_except    >>{an_except}<<  type  >>{type( an_except)}<<"
            self.append_msg( msg )

            msg     = "self.date_edit_1_widget.set_preped_data( None ) raised this "
            self.append_msg( msg )

        try:
            self.date_edit_2_widget.set_preped_data( None )

        except Exception as an_except:
            print()
            msg     = f"a_except    >>{an_except}<<  type  >>{type( an_except)}<<"
            self.append_msg( msg )

            msg     = "self.date_edit_1_widget.set_preped_data( None ) raised this "
            self.append_msg( msg )


    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        parent_window = self.parent( ).parent( ).parent().parent()

        self_line_edit_1_widget = self.line_edit_1_widget

        self_text_edit_1_widget = self.text_edit_widget

        self_date_edit_1_widget = self.date_edit_1_widget
        self_date_edit_2_widget = self.date_edit_2_widget


        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        self.append_function_msg( "breakpoint" )
        breakpoint()


# ---- eof