#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

to make this work base on one of the layout which creates its own windows



# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which should
# be named xxxxTab.py     among other things

KEY_WORDS:      color ToolBar
CLASS_NAME:     QToolbarTab
WIDGETS:        QToolbar QIcon
STATUS:         June 2025 ok: but more content would be nice
TAB_TITLE:      QToolbar / Reference
DESCRIPTION:    A reference for the QToolBar widget -- when more work is complete
HOW_COMPLETE:   5  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QToolbar"

"""
Some Notes:

Home · russ-hensel/qt5_by_example Wiki


"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------------------

import inspect
import subprocess
import sys
import time
from   datetime import datetime
from   functools import partial
from   subprocess import PIPE, STDOUT, Popen, run

import wat
from qtpy import QtGui
from qtpy.QtCore import ( QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from qtpy.QtGui import QColor, QPalette, QTextCursor, QTextDocument

from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from qtpy.QtGui import QIcon, QIntValidator, QStandardItem, QStandardItemModel

from qtpy.QtWidgets import ( QAction,
                             QApplication,
                             QButtonGroup,
                             QSpacerItem,
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
                             QToolBar,
                             QWidget )

#import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class QToolbarTab( tab_base.TabBase ):
    """
    Reference examples for QToolbar


    this is also the place for documentation on the methods normally found
    in a tab_.... file and should display its naming and other coding conventions
    other tab_xxx files may not be as well commented, you should be familiar with
    the conventions and be able to read the code.
    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK


        self.layout_args        = [ ( "yellow", 2 ),
                                    ( "blue",   0),
                                    ( "white",  0),
                                    ( "red",    0),
                                  ]

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]     = self.mutate_2
        # self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4

        self._build_gui()

    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        this is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        # ---- new row c
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row button_1 and _2 ....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- BoxWindows.build_box_layout_1
        widget = QPushButton("ExampleWindow\n ..... ")
        connect_to   = partial( self.open_window,
                                ExampleWindows.build_box_layout_1,
                                tab  = self )
        widget.clicked.connect( connect_to  )
        row_layout.addWidget( widget )


        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #---------------------------
    def open_window(self, layout_method, tab ):
        """
        Open window using the layout method layout_method
        """
        self.box_window = ExampleWindows( layout_method = layout_method,
                                       tab           = tab )  # No parent specified
        self.box_window.show()

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        msg    = "implementation comming -- but not yet "
        self.append_msg( msg, clear = False )

        self.layout_args        = [ ( "yellow", 0 ),
                                    ( "blue",   1 ),
                                    ( "white",  2 ),
                                    ( "red",    3 ),
                                  ]

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1()" )

        msg    = "implementation comming -- but not yet "
        self.append_msg( msg, clear = False )

        self.layout_args        = [ ( "yellow", 1 ),
                                    ( "blue",   0 ),
                                    ( "white",  1 ),
                                    ( "red",    0 ),
                                  ]

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them
        self_q_push_button_1    = self.q_push_button_1
        self_q_push_button_2    = self.q_push_button_1

        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tab's code

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

#------------------------------
class ExampleWindows(  QMainWindow ):
    def __init__( self, layout_method, tab ):
        """
        This works, but should be extended and may have
        old dead code.


        layout_method: method to call to layout the window
        tab  the tab controlling this module
        """
        super().__init__()  # No parent passed to super()

        self.tab           = tab
        self.layout_args   = tab.layout_args
        self.setWindowTitle( f"BoxLayout {layout_method}")
        self.setMinimumSize(400, 300 )

        # main layout for all other layouts
        self.main_layout = QVBoxLayout()
        self.setLayout( self.main_layout )

        layout_method( self )   # the layout to customize the window

        # # ---- can we do it no a tab cannot do it -- we need to make another window of some sort
        toolbar = QToolBar("My Toolbar")
        self.addToolBar( toolbar )

        # Create actions with icons
        action1 = QAction( QIcon.fromTheme("document-new"), "Choice 1", self )
        #action1.triggered.connect( self.show_message1 )
        toolbar.addAction(action1)

        action = QAction( QIcon.fromTheme( "printer" ), "Choice 1", self )
        #action.triggered.connect( self.show_message1 )
        toolbar.addAction(action)

        # ----
        action          = QAction(  "Add", self )
        # connect_to      = functools.partial(  self.go_active_sub_window_func,
        #                                       "add_default"     )
        # action.triggered.connect( connect_to )
        toolbar.addAction(action)

        # Ensure window is deleted when closed
        self.setAttribute(Qt.WA_DeleteOnClose)

    #------------------------------
    def add_to_grid_1( self,  grid_layout ):
        """
        add spacers to stabilize
        """
        line_edits = []
        # ---- Row -1 the spacer trick, make sure spaces are big enough
        for ix in range( 5 ):  # layout.col_max
            widget   = QSpacerItem( 200, 10, QSizePolicy.Minimum, QSizePolicy.Minimum ) # hsize, vsize hpolicy vpolicy
            grid_layout.addItem( widget, 0, ix  )  # row column

        # ---- Row 0
        line_edits.append(QLineEdit("Edit 1"))
        grid_layout.addWidget(line_edits[-1], 0, 0, 1, 2)  # spans 2 columns
        line_edits.append(QLineEdit("Edit 2"))
        grid_layout.addWidget(line_edits[-1], 0, 2, 1, 1)  # spans 1 column
        line_edits.append(QLineEdit("Edit 3"))
        grid_layout.addWidget(line_edits[-1], 0, 3, 1, 1)  # spans 1 column
        line_edits.append(QLineEdit("Edit 4"))
        grid_layout.addWidget(line_edits[-1], 0, 4, 1, 1)  # spans 1 column

    # -----------------
    def  build_box_layout_1( self,  ):
        """
        this is a window with a box layout
        across the top are 3 colored widgets
            inside each widget is its own layout
            all this should probably be put in some sort of list,
            and perhaps they should be in a class, tbc
        """
        self.setWindowTitle( f"BoxGridWindows.build_box_layout_1")
        self.line_edits     = []

        # widget              = QLineEdit("Edit 1")
        # self.line_edits.append( widget )
        # self.main_layout.addWidget( widget )  #

        layout_across       = QHBoxLayout( )
        self.main_layout.addLayout( layout_across )     #  QVBoxLayout()

        # ---- widget_across_1
        widget_across_1     = QWidget()
        palette             = widget_across_1.palette()
        palette.setColor(QPalette.Window, QColor("blue"))
        widget_across_1.setAutoFillBackground( True )
        widget_across_1.setPalette(palette)

        layout_across.addWidget( widget_across_1 )
        layout_across_1     = QHBoxLayout( )
        widget_across_1.setLayout( layout_across_1 )

        widget              = QLineEdit("Edit 1")
        self.line_edits.append( widget )
        layout_across_1.addWidget( widget )  #

        # ---- widget_across_2
        widget_across_2     = QWidget()
        palette             = widget_across_2.palette()
        palette.setColor(QPalette.Window, QColor("red"))
        widget_across_2.setAutoFillBackground( True )
        widget_across_2.setPalette(palette)

        layout_across.addWidget( widget_across_2 )
        layout_across_2     = QHBoxLayout( )
        widget_across_2.setLayout( layout_across_2 )

        # ---- widget_across_3
        widget_across_3     = QWidget()
        palette             = widget_across_3.palette()
        palette.setColor(QPalette.Window, QColor("yellow"))
        widget_across_3.setAutoFillBackground( True )
        widget_across_3.setPalette(palette)

        layout_across.addWidget( widget_across_3 )
        layout_across_3     = QHBoxLayout( )
        widget_across_3.setLayout( layout_across_3 )

        # ---- widget_across_  build  using a method return it an its layout
        #self.build_a_top_widget( layout_across, "white" )
        widget, layout       = self.build_a_top_widget_with_grid( layout_across, "white" )
        self.add_to_grid_1( grid_layout = layout )

    # -----------------
    def  build_box_layout_2( self,  ):
        """
        similar to build_box_layout_1
        but more compressed, easier to experiment with
        this is a window with a box layout
        across the top are colored widgets
            inside each widget is its own layout
            all this should probably be put in some sort of list,
            and perhaps they should be in a class, tbc
        """
        self.setWindowTitle( f"BoxWindows.build_box_layout_2")
        self.line_edits  = []

        layout_across    = QHBoxLayout( )
        self.main_layout.addLayout( layout_across )     #  QVBoxLayout()

        # these could all have a generic name like widget
        # ---- widget_across_1 build across using a method
        widget_across_1  = self.build_a_top_widget( layout_across,
                                                    "white",
                                                    stretch = 0 )

        # ---- widget_across_2
        widget_across_2     =  self.build_a_top_widget( layout_across,
                                                    "red",
                                                    stretch = 1 )

        # ---- widget_across_3
        widget_across_3     =  self.build_a_top_widget( layout_across,
                                                    "yellow",
                                                    stretch = 0)

        # ---- widget_across_4
        widget_across_4     =  self.build_a_top_widget( layout_across,
                                                    "blue",
                                                    stretch = 1 )

        return

    # -----------------
    def build_box_layout_mutate( self,  ):
        """
        similar to build_box_layout_2
        but more compressed, easier to experiment with
        this is a window with a box layout
        across the top are 3 colored widgets
            inside each widget is its own layout

        """
        self.setWindowTitle( f"BoxWindows.build_box_layout_mutate")
        self.line_edits     = []

        # widget              = QLineEdit("Edit 1")
        # self.line_edits.append( widget )
        # self.main_layout.addWidget( widget )  #

        layout_across       = QHBoxLayout( )
        self.main_layout.addLayout( layout_across )     #  QVBoxLayout()

        widget_list   = []
        for color, stretch in self.layout_args:

            widget_across  = self.build_a_top_widget( layout_across,
                                                        color   = color,
                                                        stretch = stretch )
            self.line_edits.append( widget_across )

    #------------------------------
    def build_a_top_widget_with_grid( self, layout_across, color, stretch = 1 ):
        """
        build one of the top widgets meant to go a
            across the layout_across
            put a grid layout in it, return widget and its layout

        """
        # ---- widget_across
        widget_across       = QWidget()
        palette             = widget_across.palette()
        palette.setColor( QPalette.Window, QColor( color ))
        widget_across.setAutoFillBackground( True )
        widget_across.setPalette(palette)

        layout_across.addWidget( widget_across, stretch = stretch )  # > Stretches more 0 = No stretch
        layout_across     = QGridLayout( )
        widget_across.setLayout( layout_across )

        # let the caller add widgets
        # widget            = QLabel( f"{stretch = }" )
        # layout_across.addWidget( widget )

        return widget_across, layout_across

    #------------------------------
    def build_a_top_widget( self, layout_across, color, stretch = 1 ):
        """
        build one of the top widgets meant to go a
            across the layout_across

        """
        # ---- widget_across
        widget_across       = QWidget()
        palette             = widget_across.palette()
        palette.setColor( QPalette.Window, QColor( color ))
        widget_across.setAutoFillBackground( True )
        widget_across.setPalette(palette)

        layout_across.addWidget( widget_across, stretch = stretch )  # > Stretches more 0 = No stretch
        layout_across     = QHBoxLayout( )
        widget_across.setLayout( layout_across )

        widget            = QLabel( f"{stretch = }" )
        layout_across.addWidget( widget )

        return widget_across

# ---- eof



