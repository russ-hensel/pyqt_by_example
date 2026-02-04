#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof

"""

KEY_WORDS:      QPushButton, QLabel, QHBoxLayout  QGridLayout RealPython rh
CLASS_NAME:     RealPython1Tab
WIDGETS:        QHBoxLayout QVBoxLayout QGridLayout QFormLayout
STATUS:         July 2025  runs incomplete
TAB_TITLE:      RP: python-pyqt- / gui-calculator
DESCRIPTION:    RP: Python and PyQt: Building a GUI Desktop Calculator
HOW_COMPLETE:   20  #  AND A COMMENT
"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/Building-a-GUI-Desktop-Calculator"



chat = """


"""
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
                             QFormLayout,
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
# ---- constants
ERROR_MSG       = "ERROR"
WINDOW_SIZE     = 235
DISPLAY_HEIGHT  = 35
BUTTON_SIZE     = 40

# # these must be defined at import time in uft
# INDENT          = uft.INDENT
# INDENT          = uft.BEGIN_MARK_1
# INDENT          = uft.BEGIN_MARK_2
# #INDENT          = qt_sql_widgets.

# print_func_header =  uft.print_func_header

# def layout_at_str( layout_at ):
#     return f"{layout_at[0] }, {layout_at[1] }, {layout_at[2] }, {layout_at[3] }"

# def layout_widget( widget, layout, layout_at, widget_list ):
#     """only for a grid
#         self.line_edits.append(QLineEdit( "Edit 1") )
#         layout_at    = 0, 0, 1, 2   # row coulum rowspan column_span
#         text         = layout_at_str( layout_at )
#         self.grid_layout.addWidget( self.line_edits[-1], *layout_at)  # spans 2 columns
#         widget       = self.line_edits[-1]

#      """
#     text         = layout_at_str( layout_at )
#     layout.addWidget( widget, * layout_at )
#     widget.setText( text )
#     widget_list.append( widget )


# ----------------------------
class RealPython1Tab( tab_base.TabBase  ) :
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


        widget       = QPushButton("Vertical\nLayout")
        connect_to   = partial( self.open_example_window, ExampleWindow.build_v_layout  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        widget       = QPushButton("Grid\nLayout")
        connect_to   = partial( self.open_example_window, ExampleWindow.build_grid  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )


        widget       = QPushButton("Form\nLayout")
        connect_to   = partial( self.open_example_window, ExampleWindow.build_form  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        widget       = QPushButton("Signals\nandSlots")
        connect_to   = partial( self.open_example_window, ExampleWindow.build_signals_and_slots  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        # ---- Calculator
        widget       = QPushButton("Calculator\n")
        connect_to   = partial( self.open_example_window, ExampleWindow.build_calc  )
        widget.clicked.connect( connect_to  )
        button_layout.addWidget( widget )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        main_layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #---------------------------
    def open_example_window( self, build_method ):
        """

        """
        self.grid_window = ExampleWindow( self, build_method )  # No parent specified
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
             msg            = "gridlayouttab",
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


class ExampleWindow( QWidget ):
    def __init__(self, tab,  build_method ):
        """
        build method is called to build after
        basics, not sure why we do not just have seperate
        windows
        guess this is experiment

        """
        super().__init__()  # No parent passed to super()

        # Set window properties
        self.setWindowTitle( f"GridWindowOne {build_method}")
        #self.setMinimumSize(400, 300)
        #self.move(800, 200)  # x y top left is 0 0

        self.setGeometry(800, 200, 400, 300)  # x=100, y=100, width=800, height=600


        self.tab     = tab
        build_method( self )

        # Ensure window is deleted when closed
        self.setAttribute( Qt.WA_DeleteOnClose )


    # ---- v layout
    def  build_v_layout( self,  ):
        """

        """
        what                 = "Vertical Box Layout"
        self.setWindowTitle(  f"{what}" )
        self.tab.append_function_msg( f"{what}" )

        # main_layout     = self.main_layout
        # layout          = QVBoxLayout()
        # main_layout.addLayout( layout )

        layout = QGridLayout( self )

        layout.addWidget(QPushButton("Top 2"))
        layout.addWidget(QPushButton("Center 3"))
        layout.addWidget(QPushButton("Bottom 4"))

        self.tab.append_msg( tab_base.DONE_MSG )

    # ---- grid code
    #-------------------
    def build_grid( self, ):
        """
        inspired by g_layout.py

        Grid layout example
        content of the excercise
        """
        self.tab.append_function_msg( "Grid Layout" )
        self.setWindowTitle(   "Grid Layout" )

        layout = QGridLayout( self )
        # main_layout.addLayout( layout )

        layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
        layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
        layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
        layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
        layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
        layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)
        layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)
        layout.addWidget(
               QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2
                   )
        self.tab.append_msg( tab_base.DONE_MSG )
       # self.append_msg( tab_base.DONE_MSG )

    # ---- form code
    def build_form( self, ):
    #def build_gui_widgets_3( self, ):
        """

        content of the excercise
        """
        # self.post_build_msg  = [ "code from build_gui_widgets_3",
        #                          "Like RP f_layout.py" ]

        self.setWindowTitle( f"A Form Layout")

        #main_layout     = self.main_layout
        layout          = QFormLayout( self )
        #main_layout.addLayout( layout )

        # widgets like RP
        layout.addRow( "Name:",      QLineEdit())
        layout.addRow( "Age:",       QLineEdit())
        layout.addRow( "Job:",       QLineEdit())
        layout.addRow( "Hobbies:",   QLineEdit())

        self.tab.append_msg( "...done" )

    # ---- signals and slots code  was 4
    def build_signals_and_slots( self, ):

    #def build_gui_widgets_4( self, ):
        """
        skip
             dialog with form --- did we have a form
             main window
             application

        then

        Signals and slots example.
        signals_slots.py


        content of the excercise
        """
        self.tab.append_function_msg( "Signals and Slots" )
        self.setWindowTitle( f"Signals and Slots")

        main_layout         = QVBoxLayout( self )
        self.main_layout    = main_layout


        layout = QVBoxLayout()
        main_layout.addLayout( layout )

        widget = QPushButton("greet_no_arg")
        widget.clicked.connect(  self.greet_no_arg, )
        layout.addWidget(widget)

        widget = QPushButton("greet_with_arg")
        widget.clicked.connect( partial(self.greet_with_arg, "North Hemi. partial World!"))
        layout.addWidget(widget)

        widget         = QLabel("")
        self.msg_label = widget
        layout.addWidget( widget )

        self.tab.append_function_msg( "...done" )

    # ------------------------
    def greet_with_arg( self, name ):
        """ """
        if self.msg_label.text():
            self.msg_label.setText("")
        else:
            self.msg_label.setText(f"Hello, from greet_with_arg -- {name = }")
    # ------------------------
    def greet_no_arg( self, ):
        """ """
        if self.msg_label.text():
            self.msg_label.setText("")
        else:
            self.msg_label.setText(f"Hello, from greet_no_arg -- World")


    # ---- calc code
    def build_calc( self, ):
        """
        really build the calculator here


        """
       # self.post_build_msg  = [ "code from build_gui_widgets_5",
       #                            "work still to be done on this excercise " ]
        self.tab.append_function_msg( "Calculator" )
        self.setWindowTitle( f"Calculator")
        #layout = QGridLayout( self )


        #main_layout         = QVBoxLayout( self )
        #self.main_layout    = main_layout
        layout              = QVBoxLayout( self )
        # main_layout.addLayout( layout )
        self.calc_layout    = layout
        self.create_calc_display()
        self.create_calc_buttons()

        # self.msg_label = widget
        # layout.addWidget( widget )

        # ---- controller
        self.controller   = PyCalc( model       =evaluateExpression,
                                     view       = self )


        self.tab.append_msg( "...done" )

    # ------------------------
    def create_calc_display(self):
        """
        this is the data entry and results widget
        """
        widget          = QLineEdit()
        self.display    = widget
        widget.setFixedHeight(DISPLAY_HEIGHT)
        widget.setAlignment(Qt.AlignmentFlag.AlignRight)
        widget.setReadOnly(True)
        self.calc_layout.addWidget( widget )

    # ------------------------
    def create_calc_buttons(self):
        """
        what it says

        """
        self.buttonMap   = {}
        button_layout    = QGridLayout()
        self.calc_layout.addLayout(button_layout)

        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                button_layout.addWidget(self.buttonMap[key], row, col)

    def setDisplayText(self, text):
        """
        Set the display's text.
        """
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """
        Get the display's text.
        """
        return self.display.text()

    def clearDisplay(self):
        """
        Clear the display.
        """
        self.setDisplayText("")


def evaluateExpression(expression):
    """Evaluate an expression (Model)."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


class PyCalc:
    """PyCalc's controller class."""

    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)



# ---- eof