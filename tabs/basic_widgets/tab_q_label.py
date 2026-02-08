#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

tab_label.py

KEY_WORDS:      pressed press push button click connect dc
CLASS_NAME:     QLabelTab
WIDGETS:        QLabel
STATUS:
TAB_TITLE:      QLabel Reference
DESCRIPTION:    QLabel Reference material demo


"""

"""
FIXME: merge from tab_label_dc_salvage.py if there's anything useful.
"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------------------


import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat

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

print_func_header   = uft.print_func_header

#  --------
class QLabelTab( tab_base.TabBase ):
    """
    Now i have a doc string.


    see
    """
    def __init__(self):
        """
        mostly for buttons
        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage
        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        self.mutate_dict[2]    = self.mutate_2
        self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        self._build_gui()

    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        """
        layout              = QVBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        #button_layout        = QHBoxLayout(   )

        # main_layout.addLayout( layout )
        # button_layout        = QHBoxLayout(   )

        # ---- new row c
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row button_1 and _2
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel( "qlabel_1" )
        self.qlabel_1   = widget
        row_layout.addWidget( widget )

        widget              = QLabel("qlabel_2 -> ")
        self.qlabel_2   = widget
        row_layout.addWidget( widget )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )


        self.build_gui_last_buttons( button_layout )

    #----------------------------
    def get_label_style_sheet( self ):
        """
        ??>?????
        what it says
        """
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """

    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find
        """
        self.append_function_msg( "signal_sent" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def put_in_clipboard( self, a_string ):
        """
        what it says:
        """
        self.append_function_msg( "put_in_clipboard" )

        clipboard = QApplication.clipboard()

        # Set a string into the clipboard
        clipboard.setText( a_string )
        self.append_msg(  f"put_in_clipboard { a_string = }" )

        get_text_out   =   clipboard.text()

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def clear_values( self ):
        """
        There is much more info to show
        """
        self.append_function_msg( "clear_values" )

        self.append_msg(  "\n\nclear_values")
        self.append_msg(  "clear_values self.line_edit_1 " )  # setText()   ??
        self.line_edit_1.setText( "" )
        # print( f"{self.little_widget_line_edit_1.isEnabled() = }" )  # setEnabled()
        # print( f"{self.little_widget_qlabel_1.text() = }" )  # setText() ??
        self.append_msg( "<<-- done" )

    # ------------------------------------
    def set_values( self ):
        """
        What it says
        """
        self.append_function_msg( "set_values" )

        self.append_msg(  "set_values  self.line_edit_1 " )  # setText()   ??
        self.line_edit_1.setText( "xxxxx" )
        # print( f"{self.little_widget_line_edit_1.isEnabled() = }" )  # setEnabled()
        # print( f"{self.little_widget_qlabel_1.text() = }" )  # setText() ??
        self.append_msg( "<<-- done" )
    # ------------------------------------
    def pb_1_clicked( self ):
        """
        What it says
        """
        self.append_msg( "pb_1_clicked" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def pb_2_clicked( self ):
        """
        What it says
        """
        self.append_msg( "pb_2_clicked" )

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets


        """
        self.append_function_msg( "mutate_0" )

        # msg    = "initial mutate"
        # self.append_msg( msg, clear = False )

        # self.q_push_button_1.setDisabled( True )
        # self.q_push_button_2.setDisabled( False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )
        # msg    = "begin implementation"
        # self.append_msg( msg, clear     = False )
        # widget        = self.q_push_button_1
        # widget.setText( "two\nlines")
        # widget.width     = 200


        # self.q_push_button_1.setText( "two\nlines")
        # self.q_push_button_1.width     = 200
        # self.q_push_button_1.setDisabled( True )
        # self.q_push_button_1.setToolTip( "this is a tool tip" )
        # self.q_push_button_1.setVisible( True )

        # msg    = "setChecked(True )"
        # self.append_msg( msg, )
        # self.q_push_button_1.setCheckable( True )
        # self.q_push_button_1.setChecked(True )

        # msg        = f"{self.q_push_button_1.isChecked() = } "
        # self.append_msg( msg, )


        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2" )
        msg    = "change some attributes..."
        self.append_msg( msg, clear = False )

        # self.q_push_button_1.setText( "one line")
        # self.q_push_button_1.width     = 500
        # self.q_push_button_1.setVisible( False )

        # # next does not seem to work
        # self.q_push_button_1.setCheckable( True )
        #     # does not seem to work
        # self.q_push_button_1.toggle()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_3" )

        msg    = "re-enable some stuff -- change attributes"
        self.append_msg( msg, clear = False )

        # self.q_push_button_1.setText( "one line")
        # self.q_push_button_1.width     = 500
        # self.q_push_button_1.setDisabled( False )
        # self.q_push_button_1.setVisible( True )
        # self.q_push_button_1.setCheckable( True )
        # self.q_push_button_1.toggle()

        # msg    = "add menu to q_push_button_1"
        # self.append_msg( msg, clear = False )
        # menu                = QMenu(self)
        # menu.addAction("Option 1")
        # menu.addAction("Option 2")
        # self.q_push_button_1.setMenu( menu )


        self.append_msg( tab_base.DONE_MSG )

    # ---- connects -----------------------
    # --------------------------
    def return_pressed( self ):
        """
        what is says
        """
        self.append_function_msg( "return_pressed" )

        self.append_msg( "\n" )


    # ------------------------
    def show_values(self):
        """
        the usual sort of thing, just read it
        """
        self.append_function_msg( tab_base.BREAK_MSG  )

        #self.append_msg( f"{self.qwidget_1 = }")

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        self_qlabel_1    = self.qlabel_1
        self_qlabel_2   = self.qlabel_2



        wat_inspector.go(
             msg            = "some locals for inspection ",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
