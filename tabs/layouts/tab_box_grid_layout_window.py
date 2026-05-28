#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof

"""


KEY_WORDS:      stretch hbox vbox rowspan columnspan colspan
CLASS_NAME:     BoxGridLayoutWindowsTab
WIDGETS:        QHBoxLayout  QVBoxLayout, QGridLayout,  QSpacerItem
STATUS:         new
TAB_TITLE:      BoxGridLayout / Windows
DESCRIPTION:    An example of box layouts containing grid layouts.
HOW_COMPLETE:   5  #     -- <10 major probs or early dev  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-BoxGridLayouts"

"""
Notes, not carefully checked
t

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    pass
# --------------------

from functools import partial



from qtpy.QtWidgets import QSpacerItem, QSizePolicy
from qtpy.QtCore import (Qt)
from qtpy.QtGui import QColor, QPalette


from qtpy.QtWidgets import (QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QSizePolicy,
                             QVBoxLayout,
                             QWidget )

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
        layout_at    = 0, 0, 1, 2   # row column rowspan column_span
        text         = layout_at_str( layout_at )
        self.grid_layout.addWidget( self.line_edits[-1], *layout_at)  # spans 2 columns
        widget       = self.line_edits[-1]

     """
    text         = layout_at_str( layout_at )
    layout.addWidget( widget, * layout_at )
    widget.setText( text )
    widget_list.append( widget )

# ----------------------------
class BoxGridLayoutWindowsTab( tab_base.TabBase  ) :
    def __init__(self):
        """
        the usual

        """
        super().__init__()
        self.module_file        = __file__
            # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.layout_args        = [ ( "yellow", 2 ),
                                    ( "blue",   0),
                                    ( "white",  0),
                                    ( "red",    0),
                                  ]

        self.mutate_dict[0]      = self.mutate_0
        self.mutate_dict[1]      = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_gui()

    #---------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QHBoxLayout(   )

        main_layout.addLayout( layout )

        button_layout        = layout

        # ---- BoxWindows.build_box_layout_1
        widget = QPushButton("boxgrid_window\n build_box_layout_1")
        connect_to   = partial( self.open_window,
                                BoxGridWindows.build_box_layout_1,
                                tab  = self )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        # # ---- BoxWindows.build_box_layout_2
        # widget = QPushButton("box_window\n build_box_layout_2")
        # connect_to   = partial( self.open_window,
        #                        BoxGridWindows.build_box_layout_2,
        #                        tab  = self )
        # widget.clicked.connect( connect_to  )
        # button_layout.addWidget( widget )

        # # ---- BoxWindows.build_box_layout_mutate
        # widget = QPushButton("box_window\n build_box_layout_mutate")
        # connect_to   = partial( self.open_window,
        #                        BoxGridWindows.build_box_layout_mutate,
        #                        tab  = self )
        # widget.clicked.connect( connect_to  )
        # button_layout.addWidget( widget )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        main_layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #---------------------------
    def open_window(self, layout_method, tab ):
        """
        Open window using the layout method layout_method
        """
        self.box_window = BoxGridWindows( layout_method = layout_method,
                                       tab           = tab )  # No parent specified
        self.box_window.show()

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0()" )

        msg    = "implemented "
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

        msg    = "implemented "
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

#------------------------------
class BoxGridWindows( QWidget ):
    def __init__( self, layout_method, tab ):
        """
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

        return

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
        self.line_edits     = []

        # widget              = QLineEdit("Edit 1")
        # self.line_edits.append( widget )
        # self.main_layout.addWidget( widget )  #

        layout_across       = QHBoxLayout( )
        self.main_layout.addLayout( layout_across )     #  QVBoxLayout()

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
