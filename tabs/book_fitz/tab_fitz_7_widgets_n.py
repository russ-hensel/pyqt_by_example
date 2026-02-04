#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
based lousely on

Chapter 7
Listing 14. basic/widgets_1.py
Listing 15. basic/widgets_2.py
Listing 16. basic/widgets_3.py
Listing 17. basic/widgets_4.py
Listing 18. basic/widgets_5.py


... /book_pyqt5_src/basic/widgets_2c.py


KEY_WORDS:      fitzz chapter book lables with images   7   rsh
CLASS_NAME:     Fitz_2_Tab
WIDGETS:        QCheckBox QPixmap QLabel QComboBox
STATUS:         ** runs   !! runs_correctly      demo_complete_0_10
TAB_TITLE:      Fitz Chapt  7 / Widgets N
HOW_COMPLETE:   15  #  AND A COMMENT
DESCRIPTION:    Various widgets from the second half of the chapter

"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/Fitz-7-Widgets-N"

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------

import inspect
import os
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
from PyQt5.QtGui import QColor, QPalette, QPixmap, QTextCursor, QTextDocument
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
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
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
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports

#  --------
class Fitz_2_Tab(  tab_base.TabBase ) :
    def __init__(self):
        """
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

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

        # ---- fitz code here
        basedir = os.path.dirname(__file__)

        # ---- QLabel
        widget = QLabel("Hello")
        self.q_label_text  = widget
        layout.addWidget( widget )

        # ---- QLabel
        widget = QLabel( "a_jpg" )
        self.q_label_jpg  = widget

        # # # tag::scaledContents[]
        # widget.setPixmap( QPixmap( "a_cat.jpg" ) )
        # widget.setPixmap( QPixmap( "bird_house.jpg" ))

        # for some photos you may loose control of size this whould fix
        widget.setMinimumSize( 100, 75)  # Minimum width: 100px, Minimum height: 75px
        widget.setMaximumSize( 400, 300)  # Maximum width: 400px, Maximum height: 300px

        chat_says = """
        Summary of Methods:

            setFixedSize(width, height): Sets a fixed size.
            setMinimumSize(width, height): Sets a minimum size.
            setMaximumSize(width, height): Sets a maximum size.
            setSizePolicy(policy_horizontal, policy_vertical): Sets resizing behavior.
            resize(width, height): Sets the initial size of the QLabel.

        """
        widget.setPixmap( QPixmap( "./tabs/book_fitz/a_cat.jpg" ) )
        #widget.setPixmap( QPixmap(os.path.join( basedir, "a_cat.jpg")) )
        widget.setScaledContents(True)
        # widget.setGeometry( 50, 50, 50, 50 ) #
        layout.addWidget( widget )

        # ---- QCheckBox
        widget          = QCheckBox( "This is a checkbox" )
        self.widget_q_check_box   = widget
        widget.setCheckState( Qt.Checked )
        # For tristate: widget.setCheckState(Qt.PartiallyChecked)
        # Or: widget.setTriState(True)
        #widget.stateChanged.connect(self.show_state)

        layout.addWidget( widget )

        # ----
        widget = QComboBox()
        self.q_combo_box_widget   = widget
        widget.addItems(["One", "Two", "Three"])
        widget.currentIndexChanged.connect(self.index_changed)

        layout.addWidget( widget )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    def index_changed(self, i):
        print(i)# i is an int

    def text_changed(self, s):
        print(s)# s is a

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

        #self_widgets_list   = self.widgets_list
        wat_inspector.go(
             msg            = "see self_widgets_list",
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
