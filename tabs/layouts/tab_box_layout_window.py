#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof

"""


KEY_WORDS:      column columnspan span  rh
CLASS_NAME:     BoxLayoutWindowsTab
WIDGETS:        QHBoxLayout  QVBoxLayout
STATUS:         new
TAB_TITLE:      BoxLayout / Windows
DESCRIPTION:    A reference for the QGridLayout widget
HOW_COMPLETE:   5  #  is grid, needs conversion AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QBoxLayout"



# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #qt_widgets.main( )
# --------------------

import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat


from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
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
                             QWidget )

import parameters
import tab_base
import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports


# these must be defined at import time in uft
INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.

print_func_header =  uft.print_func_header

def layout_at_str( layout_at ):
    return f"{layout_at[0] }, {layout_at[1] }, {layout_at[2] }, {layout_at[3] }"

def layout_widget( widget, layout, layout_at, widget_list ):
    """only for a grid
        self.line_edits.append(QLineEdit( "Edit 1") )
        layout_at    = 0, 0, 1, 2   # row coulum rowspan column_span
        text         = layout_at_str( layout_at )
        self.grid_layout.addWidget( self.line_edits[-1], *layout_at)  # spans 2 columns
        widget       = self.line_edits[-1]

     """
    text         = layout_at_str( layout_at )
    layout.addWidget( widget, * layout_at )
    widget.setText( text )
    widget_list.append( widget )


# ----------------------------
class BoxLayoutWindowsTab( tab_base.TabBase  ) :
    def __init__(self):
        """
        the usual
            grid_layout_tab.GridLayoutTab
        """
        super().__init__()
        self.module_file        = __file__
            # save for help file usage

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
        layout              = QHBoxLayout(   )

        main_layout.addLayout( layout )


        button_layout        = layout

        # # !! idea that did not get implemented ??  no just not valid
        # widget          = QPushButton("grid_window\n_0")
        # connect_to      = partial( self.open_grid_window, 0  )
        # widget.clicked.connect( connect_to  )
        # button_layout.addWidget( widget )

        # ---- layout 1
        widget = QPushButton("grid_window\n build_grid_chat")
        connect_to   = partial( self.open_grid_window, GridWindow.build_grid_chat )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        # ---- GridWindow.build_grid_chat_row_0
        widget = QPushButton("grid_window\n build_grid_chat_row_0.")
        connect_to   = partial( self.open_grid_window, GridWindow.build_grid_chat_row_0  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        # ---- build_grid_chat_row_0_spaced
        widget = QPushButton("grid_window\n build_grid_chat_row_0_spaced.")
        connect_to   = partial( self.open_grid_window, GridWindow.build_grid_chat_row_0_spaced  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        widget = QPushButton("grid_window\n build_grid_chat_refactored")
        connect_to   = partial( self.open_grid_window, GridWindow.build_grid_chat_refactored  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        main_layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #---------------------------
    def open_grid_window(self, layout_method ):
        """
        One the grid window using ones of its layout methods
        layout_method is a method in GridWindow that will be called
        from its init
        """
        self.grid_window = GridWindow( layout_method )  # No parent specified
        self.grid_window.show()

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
        self.append_function_msg( "inspect()" )

        # make some locals for inspection
        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )


class GridWindow( QWidget ):
    def __init__(self, layout_method ):  # Removed parent parameter
        super().__init__()  # No parent passed to super()

        # Set window properties
        self.setWindowTitle( f"GridWindow {layout_method}")
        self.setMinimumSize(400, 300)

        # Create grid layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        layout_method( self )

        # Ensure window is deleted when closed
        self.setAttribute(Qt.WA_DeleteOnClose)


    def  build_grid_chat_refactored( self,  ):
        """russ build """
        self.setWindowTitle( f"GridWindow build_grid_chat_refactored ")

        # Create and add 20 QLineEdits with varying column spans
        self.line_edits = []

        # Row 0  should have 5 columns like them all
        layout_at  =  ( 0, 0, 1, 2)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        layout_at  =  ( 0, 2, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        layout_at  =  ( 0, 3, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        layout_at  =  ( 0, 4, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        # Row 1
        layout_at  =  ( 1, 0, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        layout_at  =  ( 1, 1, 1, 3)  # spans 3 columns
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        layout_at  =  ( 1, 4, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        # Row 2
        #self.line_edits.append(QLineEdit("Edit 8"))
        layout_at  =  ( 2, 0, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 9"))
        layout_at  =  ( 2, 1, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 10"))
        layout_at  =  ( 2, 2, 1, 2)  # spans 2 columns
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 11"))
        layout_at  =  ( 2, 4, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        # ---- Row 3  --- adds to 5
        #self.line_edits.append(QLineEdit("Edit 12"))
        layout_at  =  (  3, 0, 1, 3)  # spans 3 columns
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 13"))
        layout_at  =  (  3, 3, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 14"))
        layout_at  =  (  3, 4, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )

        # --- Row 4 (adding extra row to complete 20 QLineEdits)
        #self.line_edits.append(QLineEdit("Edit 15"))
        layout_at  =  (   4, 0, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 16"))
        layout_at  =  (   4, 1, 1, 2)  # spans 2 columns
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 17"))
        layout_at  =  (   4, 3, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 18"))
        layout_at  =  (   4, 4, 1, 1)
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 19"))

        # ---- Row 5
        layout_at  =  (   5, 0, 1, 2)  # spans 2 columns
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )
        #self.line_edits.append(QLineEdit("Edit 20"))
        layout_at  =  (   5, 2, 1, 3)  # spans 3 columns
        layout_widget( QLineEdit( "---"), self.grid_layout, layout_at, self.line_edits )


    def  build_grid_chat_row_0_spaced( self,  ):
        """ add spacers to stabalize  """
        self.setWindowTitle( f"GridWindow build_grid_1 build_grid_chat_row_0_spaced")
        self.line_edits = []
        # ---- Row -1 the spacer trick, makd sure spaces are big enough
        for ix in range( 5 ):  # layout.col_max

            widget   = QSpacerItem( 200, 10, QSizePolicy.Minimum, QSizePolicy.Minimum ) # hsize, vsize hpolicy vpolicy
            self.grid_layout.addItem( widget, 0, ix  )  # row column


        # ---- Row 0
        self.line_edits.append(QLineEdit("Edit 1"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 0, 1, 2)  # spans 2 columns
        self.line_edits.append(QLineEdit("Edit 2"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 2, 1, 1)  # spans 1 column
        self.line_edits.append(QLineEdit("Edit 3"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 3, 1, 1)  # spans 1 column
        self.line_edits.append(QLineEdit("Edit 4"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 4, 1, 1)  # spans 1 column

    # -----------------
    def  build_grid_chat_row_0( self,  ):
        """inbetween 0 and 1 """
        self.setWindowTitle( f"GridWindow build_grid_1 build_grid_chat_row_0")
        self.line_edits = []
        # Row 0
        self.line_edits.append(QLineEdit("Edit 1"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 0, 1, 2)  # spans 2 columns
        self.line_edits.append(QLineEdit("Edit 2"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 2, 1, 1)  # spans 1 column
        self.line_edits.append(QLineEdit("Edit 3"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 3, 1, 1)  # spans 1 column
        self.line_edits.append(QLineEdit("Edit 4"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 4, 1, 1)  # spans 1 column


    def  build_grid_chat( self,  ):
        """what chat did with some alterations  """


        self.setWindowTitle( f"GridWindow build_grid_0 mostly chat ")


        # Create and add 20 QLineEdits with varying column spans
        self.line_edits = []

        # Row 0
        self.line_edits.append(QLineEdit("Edit 1"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 0, 1, 2)  # spans 2 columns
        self.line_edits.append(QLineEdit("Edit 2"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 2, 1, 1)  # spans 1 column
        self.line_edits.append(QLineEdit("Edit 3"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 3, 1, 1)  # spans 1 column
        self.line_edits.append(QLineEdit("Edit 4"))
        self.grid_layout.addWidget(self.line_edits[-1], 0, 4, 1, 1)  # spans 1 column

        # Row 1
        self.line_edits.append(QLineEdit("Edit 5"))
        self.grid_layout.addWidget(self.line_edits[-1], 1, 0, 1, 1)
        self.line_edits.append(QLineEdit("Edit 6"))
        self.grid_layout.addWidget(self.line_edits[-1], 1, 1, 1, 3)  # spans 3 columns
        self.line_edits.append(QLineEdit("Edit 7"))
        self.grid_layout.addWidget(self.line_edits[-1], 1, 4, 1, 1)

        # Row 2
        self.line_edits.append(QLineEdit("Edit 8"))
        self.grid_layout.addWidget(self.line_edits[-1], 2, 0, 1, 1)
        self.line_edits.append(QLineEdit("Edit 9"))
        self.grid_layout.addWidget(self.line_edits[-1], 2, 1, 1, 1)
        self.line_edits.append(QLineEdit("Edit 10"))
        self.grid_layout.addWidget(self.line_edits[-1], 2, 2, 1, 2)  # spans 2 columns
        self.line_edits.append(QLineEdit("Edit 11"))
        self.grid_layout.addWidget(self.line_edits[-1], 2, 4, 1, 1)

        # Row 3
        self.line_edits.append(QLineEdit("Edit 12"))
        self.grid_layout.addWidget(self.line_edits[-1], 3, 0, 1, 3)  # spans 3 columns
        self.line_edits.append(QLineEdit("Edit 13"))
        self.grid_layout.addWidget(self.line_edits[-1], 3, 3, 1, 1)
        self.line_edits.append(QLineEdit("Edit 14"))
        self.grid_layout.addWidget(self.line_edits[-1], 3, 4, 1, 1)

        # Row 4 (adding extra row to complete 20 QLineEdits)
        self.line_edits.append(QLineEdit("Edit 15"))
        self.grid_layout.addWidget(self.line_edits[-1], 4, 0, 1, 1)
        self.line_edits.append(QLineEdit("Edit 16"))
        self.grid_layout.addWidget(self.line_edits[-1], 4, 1, 1, 2)  # spans 2 columns
        self.line_edits.append(QLineEdit("Edit 17"))
        self.grid_layout.addWidget(self.line_edits[-1], 4, 3, 1, 1)
        self.line_edits.append(QLineEdit("Edit 18"))
        self.grid_layout.addWidget(self.line_edits[-1], 4, 4, 1, 1)
        self.line_edits.append(QLineEdit("Edit 19"))
        self.grid_layout.addWidget(self.line_edits[-1], 5, 0, 1, 2)  # spans 2 columns
        self.line_edits.append(QLineEdit("Edit 20"))
        self.grid_layout.addWidget(self.line_edits[-1], 5, 2, 1, 3)  # spans 3 columns

    def  build_grid_3( self,  ):
        """russ build """
        self.setWindowTitle( f"GridWindow build_grid_3")

    def  build_grid_4( self,  ):
        """russ build """
        self.setWindowTitle( f"GridWindow build_grid_4")


# ---- eof