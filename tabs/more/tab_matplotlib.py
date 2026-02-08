#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
KEY_WORDS:      Example of a matplotlib  matplot mathplot mathplotlib math  mat plot lib graph
CLASS_NAME:     QMatplotlibTab
WIDGETS:        QWidget imports from matplotlib
STATUS:         ok add to mutations
TAB_TITLE:      Matplotlib / Integration
DESCRIPTION:    A way to use MatPlotLib in QT
HOW_COMPLETE:   20  #  AND A COMMENT
Matplotlib Integration · russ-hensel/qt5_by_example Wiki
https://github.com/russ-hensel/qt5_by_example/wiki/Matplotlib-Integration

"""
WIKI_LINK      = "https://github.com/russ-hensel/pyqt_by_example/wiki/Matplotlib-Integration"

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main

# --------------------


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


# import sys
# from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports



INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.



class MatplotlibWidget( QWidget ):
    def __init__(self, parent=None):
        """


        """
        super(MatplotlibWidget, self).__init__(parent)

        # Create a Figure and Canvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_example(self):
        """


        """

        # Clear the axes
        self.axes.clear()

        # Create a simple plot
        x = [0, 1, 2, 3, 4, 5]
        y = [0, 1, 4, 9, 16, 25]
        self.axes.plot(x, y, 'r-')
        self.axes.set_title('y = x²')
        self.axes.grid(True)

        # Refresh the canvas
        self.canvas.draw()

    def update_plot(self, new_x, new_y):
        """


        """
        self.axes.clear()
        self.axes.plot(new_x, new_y)
        self.canvas.draw()

#  --------
class QMatplotlibTab( tab_base.TabBase ) :
    def __init__(self):
        """
        the usual



        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        # State variable to track search position
        self.last_position      = 0
        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        # button_layout        = QHBoxLayout(   )

        ix_row     = 0
        ix_col     = 0
        row_span   = 1
        col_span   = 1


        # Create the Matplotlib widget
        plot_widget         = MatplotlibWidget()
        self.plot_widget    = plot_widget
        layout.addWidget( plot_widget )
        # # Set as central widget
        # self.setCentralWidget(self.plot_widget)

        # Plot an example
        self.plot_widget.plot_example()

        # widget             = QLineEdit()
        # self.line_edit     = widget

        # # ---- see if these are legal
        # #widget.setHeight( 10 )   # ng
        # widget.setText( "widget.setText ")
        # # widget.append(  "append a bit" )
        # widget.setReadOnly( True )

        chat = """  """


        button_layout    = QHBoxLayout()
        layout.addLayout( button_layout )

        # # ---- lower buttons


        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )



    # ---------------  end of button actions and class
    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        !! we may phase out for print_string  or the reverse ??
             make one call the other
        print to message area, with scrolling and
        log if we are configured for it

        parameters.gui_text_log_fn    = False  # "gui_text.log"
                                               # a file name or something false


        parameters.log_gui_text       = False # True or false to log text
        parameters.log_gui_text_level = 10    # logging level for above

        !! add parameter clear_msg = True or false

        """

        self.append_function_msg( "display_string" )

        self.append_msg(  f"in display_string, with a_string = {a_string}")
        # return
        #   try  !!!  QTextEdit.clear()
        cursor = self.text_edit.textCursor()
        # cursor.movePosition( QTextCursor::End )
        cursor.insertText( a_string )

        self.append_msg( "display_string done" )
    #  --------
    def print_message(self, text):
        """
        what is says
        """
        self.append_function_msg( "print_message" )

        self.append_msg( "Button clicked:", text)
        self.append_msg( "print_message done" )

    #  --------
    def clear_text( self ):
        """
        """
        self.append_function_msg( "clear_text" )

        self.text_edit.clear()
        self.append_msg( "clear_text done" )

    #  --------
    def copy_text(self, text_edit):
        """
        what is says
        """
        self.append_function_msg( "copy_text" )

        self.append_msg( "QTextEditTab.copy_text"   )
        selected_text      = text_edit.toPlainText()
        QApplication.clipboard().setText(selected_text)
        self.append_msg(  f" copy_text -> {selected_text }" )
        self.append_msg( "copy_text done" )

    #  --------
    def copy_all_textxxx( self, text_edit ):
        """
        what it says
        """
        self.append_function_msg( "copy_all_text" )

        # text_edit not used
        all_text = self.text_edit.toPlainText()
        self.append_msg( f"{all_text = }")

        self.copy_all_text_b( None )

        self.append_msg( "copy_all_text done" )

        return all_text  # return not used

    #  --------
    def copy_all_text_bxxxx( self, text_edit ):
        """
        what it says
        """
        self.append_function_msg( "copy_all_text_b" )

        text_edit   = self.text_edit

        all_text = text_edit.toPlainText()
        self.append_msg( "text_edit.toPlainText()  {all_text}" )



        # Save current cursor position
        cursor      = text_edit.textCursor()
        original_position = cursor.position()

        # Select all text and copy to the clipboard
        text_edit.selectAll()
        text_edit.copy()   # think goes to clipboard

        all_text = self.text_edit.toPlainText()

        # Restore cursor to its original position
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)

        self.append_msg( "all text copied to clipboard" )
        self.append_msg( "copy_all_text_b done" )

        return  all_text

    # ----
    def set_text_ver_1xxx(self,  ):
        """
        what is says
        """
        self.append_function_msg( "set_text_ver_1" )

        a_string    = 1 * (

        """
        More than 20 years have passed since I authored the Python
 e of the most popular
programming languages in the world. Python programmers also
have a wealth of information at their fingertips in the form of
advanced editors, IDEs, notebooks, web pages, and more. In fact,
there’s probably little need to consult a reference book when almost
any reference material you might want can be conjured to appear
before your eyes with the touch of a few keys.

        """ )

        self.text_edit.setText( a_string )

        self.append_msg( "set_text_ver_1 done" )

    #---------------
    def set_text_ver_2xxx(self,  ):
        """
        what is says
        """
        self.append_function_msg( "set_text_ver_2" )

        a_string    = 22  * (

        """
        HOMEXCEL Sponges Kitchen 24pcs, Non-Scratch Scrub Dish Sponges,
        Safe on Non-Stick Cookware,Dual Sided Cleaning Sponges
        for Kitchen,Household,Bathroom and More

        """ )

        self.text_edit.setText( a_string )

        self.append_msg( "set_text_ver_2 done" )



    #-------------------
    def delete_textxxxx(self, text_edit):
        """
        """
        self.append_function_msg( "delete_text" )

        text_edit.clear()

        self.append_msg( "delete_text done" )

    #--------
    def insert_textxxx( self, ):
        """
        insert text at the cursor position
        """
        self.append_function_msg( "insert_text" )

        a_string  = ( """>>---- so here is a bit
of text the we will
           ------------------> insert
at the cursor ----<<""")

        text_edit       = self.text_edit
        cursor          = text_edit.textCursor()
        cursor.insertText( a_string )
        self.append_msg( "insert_text done" )

    #----------------------------
    def copy_selected_text(self,  ):
        """
        """
        self.append_function_msg( "copy_selected_text" )

        text_edit       = self.text_edit
        selected_text   = text_edit.textCursor().selectedText()
        QApplication.clipboard().setText( selected_text )

        # to paste get the text with QApplication.clipboard().text()
        #clipboard = QApplication.clipboard()

        self.append_msg(  f"   -> {selected_text = } now in clipboard" )
        self.append_msg( "copy_selected_text done" )

    #----------------------
    def copy_n_lines_of_textxxxx(self, text_edit, num_lines ):
        """
        copy some number of lines of text to clipboard

        """
        self.append_function_msg( "copy_n_lines_of_text" )

        cursor = text_edit.textCursor()

        # Save the original cursor position
        original_position = cursor.position()

        # Move to the start of the current line
        cursor.movePosition(cursor.StartOfLine)

        # List to store the next lines
        lines = []

        # Collect the next `num_lines` lines
        for _ in range( num_lines ):
            # Select the line from the start to the end
            cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
            line_text = cursor.selectedText()

            # Add the selected line to the list
            lines.append(line_text)

            # Move to the start of the next line
            cursor.movePosition(cursor.Down)

        # Restore the original cursor position
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)

        # Print or return the list of lines
        self.append_msg( f"Next {num_lines} lines:", lines)
        self.append_msg( "copy_n_lines_of_text done" )
        return lines

    #----------------------
    def copy_line_of_textxxx(self, arg ):
        """
        chat:
        With a QTextWidge holding some text:
        from the cursor position copy the text from the
        beginning of the line to the end of the line.
        """
        self.append_function_msg( "copy_line_of_text" )

        text_edit           = self.text_edit
        cursor              = text_edit.textCursor()
        # Save the original cursor position
        original_position   = cursor.position()
        cursor.movePosition( cursor.StartOfLine )

        # Select the text from the beginning to the end of the line
        cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
        selected_text = cursor.selectedText()
        # print(f"Copied text: {selected_text = }")

        # Optionally, copy to the system clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

        # Restore the original cursor position
        cursor.setPosition(original_position)
        self.text_edit.setTextCursor(cursor)

        self.append_msg( f"Copied text: {selected_text = }")
        self.append_msg( "copy_line_of_text done" )

    # ---------------------
    def search_downxxx(self):
        """
        think i want no print for this
        search from current cursor down in text field
        """
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(self.last_position)
            found = self.text_edit.find(search_text)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if end is reached and no match
                self.last_position = 0


    # ---------------------
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
        self_plot_widget            = self.plot_widget

        wat_inspector.go(
             msg            = "inspect ",
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

