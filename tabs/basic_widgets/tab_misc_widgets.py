#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof



"""

tab_groupbox.py

self.help_file_name     =  "misc_widget_tab.txt"

KEY_WORDS:      lots multiple misc widgets many return pressed push button
CLASS_NAME:     MiscWidgetTab
WIDGETS:        QHBoxLayout QVBoxLayout QLabel QPushButton QCheckBox QLineEdit QLineEdit QRadioButton
STATUS:         works
TAB_TITLE:      Misc / Widgets
DESCRIPTION:    Various Misc Widgets
HOW_COMPLETE:   20  #  AND A COMMENT

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Documentation-Not-Written"

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
class MiscWidgetTab(  tab_base.TabBase  ):
    def __init__(self):
        """
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()

        self.module_file        = __file__      # save for help file usage
        self.help_file_name     =  "misc_widget_tab.txt"

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]    = self.mutate_0
        # self.mutate_dict[1]    = self.mutate_1
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

        # ---- New row colored_filler
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel( "colored_filler -> " )
        self.qlabel_1   = widget
        row_layout.addWidget( widget )

        widget          =  uft.ColoredFiller('red')
        self.qwidget_1  = widget
        row_layout.addWidget( widget )

        # ---- New Row button_1 and _2
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel( "q_pbutton_1 -> " )
        self.qlabel_1   = widget
        row_layout.addWidget( widget )

        widget              = QPushButton( "q_pbutton_1" )
        self.q_pbutton_1    = widget
        connect_to          = self.pb_1_clicked
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        widget              = QLabel("q_pbutton_2 -> ")
        row_layout.addWidget( widget )

        widget              = QPushButton( "q_pbutton_2" )
        self.q_pbutton_2    = widget
        connect_to          = self.pb_2_clicked
        widget.clicked.connect( connect_to    )
        row_layout.addWidget( widget,  )

        # ---- qlabel_1 an _2
        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel("qlabel_1 -> ")
        row_layout.addWidget( widget )

        widget          = QLabel("qlabel_1")
        self.qlabel_1   = widget
        #widget.setLayoutDirection( Qt.RightToLeft )
        #widget.setLayoutDirection( Qt.LeftToRight )
        row_layout.addWidget( widget )

        # ---- qlabel_2
        widget          = QLabel("qlabel_2 -> ")
        row_layout.addWidget( widget )

        widget          = QLabel("qlabel_2 text")
        self.qlabel_2   = widget
        row_layout.addWidget( widget )
        #widget.setLayoutDirection( Qt.RightToLeft )
        #widget.setText( "change original text ..........." )
        #widget.setLayoutDirection( Qt.LeftToRight )
        #layout.addWidget( widget )
        #row_layout.addWidget( widget, Qt.AlignmentFlag.AlignRight )

        # ---- QCheckBoxs
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel("cbox_1 - 3-> ")
        row_layout.addWidget( widget )

        widget          = QCheckBox( "cbox_1 label"  )
        self.cbox_1     = widget
        widget.setChecked(True)
        widget.toggled.connect( self.cbox_clicked )
        row_layout.addWidget( widget, stretch = 0 )

        widget          = QCheckBox( "cbox_2 label"  )
        self.cbox_2     = widget
        widget.setChecked(True)
        widget.toggled.connect( self.cbox_clicked )
        row_layout.addWidget( widget, stretch = 0 )

        widget          = QCheckBox( "cbox_3 label"  )
        self.cbox_3     = widget
        widget.setChecked(True)
        widget.toggled.connect( self.cbox_clicked )
        row_layout.addWidget( widget, stretch = 0 )

        # ---- QLineEdit 1
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel("line_edit_1 -> ")
        row_layout.addWidget( widget )

        widget            = QLineEdit()
        self.line_edit_1  = widget
        widget.setText( "QLineEdit use setText to set value disabled? on second line?")
            #\n does not give second line
        widget.setDisabled( True )
        widget.setDisabled( False )
        widget.setPlaceholderText( "Enter your text here" )  # clear to see
        widget.textChanged.connect( self.on_text_changed ) # user or pro grammatically
        widget.textEdited.connect(self.on_text_edited)  # user only
        widget.editingFinished.connect(self.on_editing_finished) # done leaves control
        widget.returnPressed.connect( self.return_pressed )

        widget.setReadOnly(True)
        widget.setReadOnly(False)
        row_layout.addWidget( widget )

        # ---- QLineEdit 2
        widget              = QLabel("line_edit_2 -> ")
        row_layout.addWidget( widget )

        widget              = QLineEdit()
        self.line_edit_2    = widget
        widget.setText( "line_edit_2")
        widget.textChanged.connect(      lambda: self.signal_sent(  "textChanged"   ) )
        widget.editingFinished.connect(  lambda: self.signal_sent( "editingFinished"  ) )
            #\n does not give second line
        #widget.setDisabled( True )
        # no errors from these but do not seem effective
        widget.setLayoutDirection( Qt.RightToLeft )
        widget.setLayoutDirection( Qt.LeftToRight )
        row_layout.addWidget( widget )

        # ---- new row QRadioButtons
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel("radio_buttons 1-3 -> ")
        row_layout.addWidget( widget )

        widget        = QRadioButton("rb_1")
        self.rb_1     = widget
        row_layout.addWidget( widget )

        widget        = QRadioButton("rb_2")
        self.rb_2     = widget
        row_layout.addWidget( widget )

        widget        = QRadioButton("rb_3")
        self.rb_3    = widget
        row_layout.addWidget( widget )

        # widget        = QRadioButton("rb_1")
        # self.rb_1     = widget
        # #radiobutton   = QRadioButton("AUSTRALIA")
        # widget = QRadioButton('Left-Text Radio Button')
        # widget.setChecked(True)  # Set as default selected
        # widget.setLayoutDirection( Qt.RightToLeft )  # Set text layout direction to right-to-left textOnLeft
        # widget.setLayoutDirection( Qt.LeftToRight )
        # row_layout.addWidget( widget )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        self.button_ex_1         = widget

        widget = QPushButton("show_\nvalues")
        self.button_ex_1         = widget
        widget.clicked.connect(  self.show_values )
        button_layout.addWidget( widget )

        widget = QPushButton("clear_\nvalues")
        a_widget        = widget
        widget.clicked.connect(  self.clear_values  )
        button_layout.addWidget( widget )

        widget = QPushButton("set_values\n")
        widget.clicked.connect( lambda: self.set_values( ) )
        button_layout.addWidget( widget )

        widget = QPushButton("clip\n")
        widget.clicked.connect( lambda: self.clip( ) )
        button_layout.addWidget( widget )

        self.build_gui_last_buttons( button_layout )



        # # ---- PB inspect
        # widget = QPushButton("inspect\n")
        # widget.clicked.connect( self.inspect    )
        # button_layout.addWidget( widget,   )

        # # ---- PB breakpoint
        # widget = QPushButton("breakpoint\n")
        # widget.clicked.connect( self.breakpoint    )
        # button_layout.addWidget( widget,   )

    def get_button_style_sheet( self ):
        """
        what it says
        """
        return ("""
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
        """)


    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find
        """
        self.append_function_msg( "signal_sent" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg(  f"signal_sent {msg}" )

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
        self.append_function_msg( "pb_1_clicked" )
        self.append_msg( tab_base.DONE_MSG )
    # ------------------------------------
    def pb_2_clicked( self ):
        """
        What it says
        """
        self.append_function_msg( "pb_2_clicked" )

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )
        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( "<<-- done" )

    # --------
    def clip( self ):
        """
        """
        self.append_function_msg( "clip" )

        a_string    = self.line_edit_1.text()
        self.put_in_clipboard( a_string )

        self.append_msg( "<<-- done" )

    # --------
    def cbox_clicked( self ):
        """
        """
        self.append_function_msg( "cbox_clicked" )

        cbox = self.sender()   # look into self.sender() looks like it might be standard !!

        self.append_msg(  f"check box text() = { cbox.text()} ")

        self.append_msg( "<<-- done" )

    # ---- signals sent -----------------------
    # --------------------------
    def on_editing_finished(self):
        """
        what is says
        """
        self.append_function_msg( "on_editing_finished" )

        self.append_msg( "<<-- done" )

    # --------------------------
    def return_pressed( self ):
        """
        what is says
        """
        self.append_function_msg( "return_pressed" )

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def on_text_changed( self, new_text):
        """
        what is says
        """
        self.append_function_msg( "on_text_changed" )

        self.append_msg( f"Text changed: {new_text}")

        self.append_msg( "<<-- done" )

    # ------------------------------------
    def on_text_edited(self, new_text):
        """
        what is says
        """
        self.append_function_msg( "on_text_edited" )

        self.append_msg( f"User edited text: {new_text}")

        self.append_msg( "<<-- done" )

    # ------------------------
    def show_values(self):
        """
        the usual sort of thing, just read it
        """
        self.append_function_msg( "inspect" )

        self.append_msg( f"{self.qwidget_1 = }")
        #print( f"{self.qwidget_1 = }")

        self.append_msg( f"{self.line_edit_1.text() = }" )  # setText()   ??
        self.append_msg( f"{self.line_edit_1.isEnabled() = }" )  # setEnabled() no focus
        self.append_msg( f"{self.line_edit_1.isReadOnly() = }" )

        self.append_msg( f"{self.qlabel_1.text() = }" )  # setText() ??
        self.append_msg( f"{self.qlabel_2.text() = }" )

        self.append_msg( f"{str(self.cbox_1.isChecked()) = }" )

        self.append_msg( "<<-- done" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        self_q_pbutton_1    = self.q_pbutton_1
        self_q_pbutton_2    = self.q_pbutton_2

        self_qlabel_1       = self.qlabel_1
        self_qlabel_2       = self.qlabel_2

        self_line_edit_1    = self.line_edit_1
        self_line_edit_2    = self.line_edit_2

        self_qwidget_1      = self.qwidget_1

        #my_tab_widget = self
        #parent_window = self.parent( ).parent( ).parent().parent()

        wat_inspector.go(
             msg            = "tbd add more locals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "<<-- done" )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
