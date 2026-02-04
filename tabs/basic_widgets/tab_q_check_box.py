#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""


KEY_WORDS:      QCheckBox  checkbox check box dc
CLASS_NAME:     QCheckBoxTab
WIDGETS:        QCheckBox
STATUS:         new
TAB_TITLE:      QCheckBox Reference
HOW_COMPLETE:   25  #  AND A COMMENT

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

#import parameters


import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class QCheckBoxTab(  tab_base.TabBase  ):
    def __init__(self):
        """
        from misc widgets
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage
        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        self.mutate_dict[2]    = self.mutate_2
        self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        self._build_gui()

    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )
        main_layout.addLayout( layout )
       # button_layout        = QHBoxLayout(   )

        # ---- New Row button_1 and _2
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- qlabel_1 an _2
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- QCheckBoxs
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel("cbox_0 - 2 -> ")
        row_layout.addWidget( widget )

        widget          = QCheckBox( "cbox_0 label"  )
        self.cbox_0     = widget
        widget.setChecked(True)
        widget.toggled.connect( self.cbox_clicked )
        row_layout.addWidget( widget, stretch = 0 )

        widget          = QCheckBox( "cbox_1 label"  )
        self.cbox_1     = widget
        widget.setChecked(True)
        widget.toggled.connect( self.cbox_clicked )
        widget.stateChanged.connect(self.checkbox_state_changed)

        row_layout.addWidget( widget, stretch = 0 )

        widget          = QCheckBox( "cbox_2 label"  )
        self.cbox_2     = widget
        widget.setChecked(True)
        widget.toggled.connect( self.cbox_clicked )
        row_layout.addWidget( widget, stretch = 0 )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        self.build_gui_last_buttons( button_layout )


    # ------------------------------------
    def signal_sent_xxx( self, msg ):
        """
        when a signal is sent, use find
        """
        self.append_function_msg( "signal_sent" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg(  f"signal_sent {msg}" )



    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "check everything "
        self.append_msg( msg, clear = False )

        state  = True
        self.cbox_0.setChecked( state )
        self.cbox_1.setChecked( state )
        self.cbox_2.setChecked( state )

        self.cbox_2.setLayoutDirection( Qt.LeftToRight )
        
        
        self.append_msg( f"{str(self.cbox_1.isChecked()) = }" )
        self.append_msg( f"{str(self.cbox_2.isChecked()) = }" )


        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        state  = False
        self.cbox_0.setChecked( state )
        self.cbox_1.setChecked( state )
        self.cbox_2.setChecked( state )

        msg    = "un- check everything "
        self.append_msg( msg, clear = False )

        
        
        self.append_msg( f"{str(self.cbox_1.isChecked()) = }" )
        self.append_msg( f"{str(self.cbox_2.isChecked()) = }" )



        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2" )

        state  = False
        self.cbox_0.setChecked( not state )
        self.cbox_1.setChecked(     state )
        self.cbox_2.setChecked( not state )
        msg    = "make cbox_1 differenly checked "
        self.append_msg( msg,  )

        self.cbox_0.setLayoutDirection(Qt.LeftToRight )
        self.cbox_1.setLayoutDirection(Qt.LeftToRight )
        self.cbox_2.setLayoutDirection(Qt.LeftToRight )
        msg    = "mess with setLayoutDirection "
        self.append_msg( msg,  )



        self.append_msg( f"{str(self.cbox_1.isChecked()) = }" )
        self.append_msg( f"{str(self.cbox_2.isChecked()) = }" )



        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        
        FIXME: how else can I change checkboxes?
        """
        self.append_function_msg( "mutate_3" )

        self.cbox_1.setChecked(not self.cbox_1.isChecked())

        msg    = "toggle check on  cbox_1"
        self.append_msg( msg, clear = False )

        self.cbox_0.setLayoutDirection(Qt.RightToLeft )
        self.cbox_1.setLayoutDirection(Qt.RightToLeft )
        self.cbox_2.setLayoutDirection(Qt.RightToLeft )
        msg    = "mess with setLayoutDirection "
        self.append_msg( msg,  )


        self.append_msg( f"{str(self.cbox_1.isChecked()) = }" )
        self.append_msg( f"{str(self.cbox_2.isChecked()) = }" )



        self.append_msg( tab_base.DONE_MSG )




    def checkbox_state_changed( self, state ):
        """Handles changes in the  checkbox
        for 2 or 3 state boxes
        triggere even if change is progamatic
        else see _clicked
        """
        self.append_msg( "checkbox_state_changed" )
        sender = self.sender()     # which check box

        msg   = (f"{sender.text()} changed to {state}")
        self.append_msg( msg )

        if state == Qt.Unchecked:
            msg      = ("Tri-State: Unchecked")
        elif state == Qt.PartiallyChecked:
            msg      = ("Tri-State: Partially Checked")
        elif state == Qt.Checked:
            msg      = ("Tri-State: Checked")
        self.append_msg( msg )

        #self.append_msg( "<<-- done" )

    # --------
    def cbox_clicked( self ):
        """
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)
        """
        self.append_msg( "cbox_clicked()" )

        cbox = self.sender()   # look into self.sender() looks like it might be standard !!

        self.append_msg(  f"check box text() = { cbox.text()}\n")

        #self.append_msg( "<<-- done" )

    # ---- signals sent -----------------------

    # --------------------------
    def return_pressed_xxx( self ):
        """
        what is says
        """
        self.append_function_msg( "return_pressed\n" )

\
    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect()" )


        self_cbox_0  = self.cbox_0
        self_cbox_1  = self.cbox_1
        self_cbox_2  = self.cbox_2

        #my_tab_widget = self
        #parent_window = self.parent( ).parent( ).parent().parent()

        wat_inspector.go(
             msg            = "for your inspection, inc. locals and globals",
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
