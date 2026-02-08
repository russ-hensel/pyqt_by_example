#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

tab_context_menu.py

KEY_WORDS:      hover
CLASS_NAME:     ToolTipTab
WIDGETS:        QToolTip
STATUS:         seem fairly complete
TAB_TITLE:      QToolTip / and Hover
DESCRIPTION:    ToolTips and other Hover Code
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Documentation-Not-Written"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------------------


import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat

from qtpy import QtCore
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

#from qtpy.QtWidgets import QLabel

class HoverLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background: lightgray;")

    def enterEvent(self, event):
        self.setStyleSheet("background: yellow;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("background: lightgray;")
        super().leaveEvent(event)





#  --------
class ToolTipTab( tab_base.TabBase ):
    """
    Now i have a doc string.


    see
    """
    def __init__(self):
        """
        set up except for gui
        """
        super().__init__()
        self.module_file       = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]     = self.mutate_2
        # self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4
        # self.mutate_dict[5]     = self.mutate_5

        self._build_gui()

    #----------------
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
        row_layout          = QVBoxLayout(   )
        layout.addLayout( row_layout )


        # ---- the QTextEdit
        widget       = QLineEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.line_edit  = widget   # later we will need to know this

        row_layout.addWidget( widget,  )

        # ---- the QHoverLabel
        widget       = HoverLabel( "this is a HoverLabel")
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.hover_label  = widget   # later we will need to know this

        row_layout.addWidget( widget,  )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        self.build_gui_last_buttons( button_layout )


    #-------------------------
    def no_tool_tip(self, widget ):
        """


        """
        self.append_msg( "no_tool_tip" )
        # Option 1: Revert to default context menu
        #widget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # Option 2: Disable context menu entirely
        #widget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        widget.setToolTip( None )


    #----------------------------
    def a_tool_tip( self, widget ):
        """
        what it says

        """
        msg    = ("a_tool_tip")
        self.append_msg( msg )
        widget.setToolTip( "a_tool_tip" )


    #----------------------------
    def foo(self):
            """
            Example function to be called from context menu
            """
            msg   = ("foo action triggered!")
            self.append_msg( msg )

    #----------------------------
    def mousePressEventNot( self, event ):
        """
        override the builtin then forward
        by capturing the right click we could
        also capture the event for a context menu
        """
        msg = ("mousePressEvent" )
        self.append_msg( msg )

        if event.button() == Qt.RightButton:
            msg = ("Right-click detected")
            self.append_msg( msg )

            if self.right_click_menu:
                msg = ( f"{self.right_click_menu = }")
                self.append_msg( msg )
                # had trouble getting the right position
                #pos  = event.globalPos()
                #pos  = self.mapToGlobal(event.pos())
                # pos  = self.text_edit.mapToGlobal(event.pos())
                # pos  = event.pos()
                pos = self.text_edit.mapFrom(self, event.pos())

                self.show_context_menu( pos )

        elif event.button() == Qt.LeftButton:
            msg = ("Left-click detected")
            self.append_msg( msg )

        msg = ("continue to default in ancestor super....")
        self.append_msg( msg )

        super().mousePressEvent(event)  # continue to default behavior


    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        widget    = self.line_edit

        self.no_tool_tip( widget )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )



        self.a_tool_tip( self.line_edit )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2" )

        self.custom_context_menu( self.text_edit )

        self.right_click_menu       = False
        self.append_msg( f"{self.right_click_menu = }", )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_3" )



        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_4" )

        self.append_msg( tab_base.DONE_MSG )


    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        self_line_edit          = self.line_edit
        self_hover_label        = self.hover_label

        wat_inspector.go(
             msg            = "variables for inspection ",
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



