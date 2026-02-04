#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY_WORDS:      label widget experiments test ideas
CLASS_NAME:     QTExperimentsTab
WIDGETS:        QLabel
STATUS:         ??
TAB_TITLE:      XPeriments



TAB_HELPxx:       combo_box_widget_tab.txt


self.help_file_name     =  "combo_box_widget_tab.txt"
/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/docs/combo_box_widget_tab.txt
"""

"""
I would like you to use Python with QT5 to make a subclass of
the QTComboBox.  I want the box to accept user typed input.  The class
should have a method that adds the input to the list of items in the combo
box in oder that they are added up to a maximun of max_items and then
remove the oldest first.  Call this function any time the user
leaves the widget or hits enter in the widget


"""






# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------

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

import parameters
import utils_for_tabs as uft
import wat_inspector
import tab_base
import custom_widgets

# ---- end imports

# from PyQt5.QtWidgets import QComboBox, QApplication
# from PyQt5.QtCore import Qt

class LimitedHistoryComboBox(QComboBox):
    """
    chatgpt first effort
    works on first try
    """
    def __init__(self, max_items=5, parent=None):
        super().__init__(parent)
        self.setEditable(True)  # Allow user input
        self.max_items = max_items  # Set max item limit

        # Connect signals
        self.editTextChanged.connect(self.handle_edit_text)
        self.activated.connect(self.add_current_text)
        self.focusOutEvent = self.create_focus_out_event()

    def handle_edit_text(self, text):
        """Handles when user types into the box"""
        self.current_text = text

    def add_current_text(self):
        """Adds the current text to the list with max_items limit"""
        text = self.currentText().strip()
        if text and text not in [self.itemText(i) for i in range(self.count())]:  # Avoid duplicates
            self.addItem(text)

            # Keep only the last 'max_items' items
            if self.count() > self.max_items:
                self.removeItem(0)  # Remove the oldest entry

    def keyPressEvent(self, event):
        """Capture Enter key to add item"""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.add_current_text()
        super().keyPressEvent(event)

    def create_focus_out_event(self):
        """Handles when focus leaves the widget"""
        def focus_out_event(event):
            self.add_current_text()
            super(LimitedHistoryComboBox, self).focusOutEvent(event)
        return focus_out_event

# # Example usage
# if __name__ == "__main__":
#     app = QApplication([])

#     combo = LimitedHistoryComboBox(max_items=5)
#     combo.show()

#     app.exec_()






#  --------
class QTExperimentsTab( tab_base.TabBase  ) :
    def __init__(self):
        """
        """
        super().__init__()
        self.help_file_name     =  "lable_widget_tab.txt"

        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_gui()

    # ----------------------------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        # ----
        layout        = QVBoxLayout(   )
        main_layout.addLayout( layout )

        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ----- widget

        widget        = LimitedHistoryComboBox( max_items=5  )
        self.widget_1  = widget
        row_layout.addWidget( widget )

        widget        = custom_widgets.CQComboBoxEditCriteria2( )
        self.widget_2  = widget
        row_layout.addWidget( widget )


        # ---- label_1
        widget        = QLabel( "label_1 ")
        self.label_1  = widget

        # these work but in some case seem only to work with a lambda
        # widget.currentIndexChanged.connect( self.conbo_currentIndexChanged )
        # widget.currentTextChanged.connect(  self.combo_currentTextChanged  )

        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        row_layout.addWidget( widget )

        # ---- label_1
        widget        = QLabel( "label_2 ")
        self.label_2  = widget

        # these work but in some case seem only to work with a lambda
        # widget.currentIndexChanged.connect( self.conbo_currentIndexChanged )
        # widget.currentTextChanged.connect(  self.combo_currentTextChanged  )

        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        row_layout.addWidget( widget )


        # ---- buttons
        # button_layout = QHBoxLayout(   )
        # layout.addLayout ( button_layout )
        # # --- buttons
        # label       = "combo\n_reload"
        # widget = QPushButton( label )
        # widget.clicked.connect( self.combo_reload )

        # button_layout.addWidget( widget )

        row_layout    = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- PB mutate
        label       = "mutate\n"
        widget = QPushButton( label )
        widget.clicked.connect( self.mutate )

        row_layout.addWidget( widget )

        # ---- PB inspect
        widget = QPushButton( "inspect\n" )
        widget.clicked.connect( self.inspect    )
        clear_button = widget
        row_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton( "breakpoint\n" )
        widget.clicked.connect( self.breakpoint    )
        clear_button = widget
        row_layout.addWidget( widget,   )


    # -----------------------
    def conbo_return(self, arg ):
        """

        """
        self.append_function_msg( "conbo_signal" )

        #print( f"conbo_signal {arg}")

    # -----------------------
    def conbo_signal(self, arg ):
        """
                activated(int index)
        void 	currentIndexChanged(int index)
        void 	currentTextChanged(const QString &text)
        void 	editTextChanged(const QString &text)
        void 	highlighted(int index)
        void 	textActivated(const QString &text)
        void 	textHighlighted(const QString &text)
        """
        self.append_function_msg( "conbo_signal" )

        print( f"conbo_signal {arg}")

    # -----------------------
    def conbo_currentIndexChanged(self, arg ):
        """
        what it says
        """
        self.append_function_msg( "conbo_currentIndexChanged" )

        self.append_function_msg( "conbo_currentIndexChanged -- and get text" )

        self.append_msg( f"{self.combo_1.currentText( ) = }" )

        self.append_msg( tab_base.DONE_MSG )



    # --------------------------
    def combo_reload(self,   ):
        """
        notice order of events
        """
        self.append_function_msg( "combo_reload" )

        self.append_msg( f"combo_reload { '' }clear next --------", flush = True )
        values         =  [ "1_reload", "2", "3", "4", ]
            # what do i get I get a dict of lists, I need all the keys
        widget         = self.combo_1
        widget.clear()       # delete all items from Combobox
        self.append_msg( f"combo_reload end clear / next addItems", flush = True )
        widget.addItems( values )


        self.append_msg( tab_base.DONE_MSG )
    # --------------------------
    def inspect_old( self, arg  ):
        """
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        self.append_function_msg( "inspect_old" )
        self.append_msg( f"combo_info { '' }  --------", flush = True )

        widget         = self.combo_1

        info           = widget.count()
        msg            = f"widget.count() {info}"
        self.append_msg( msg )

        info           = widget.currentData()    # seem to always get None
        msg            = f"widget.currentData() {info}"
        self.append_msg( msg )

        # qt5 not working for me
        # info           = widget.editable
        # msg            = f".editable {info}"
        # print( msg )

        info           = widget.currentText()  # is good
        msg            = f".currentText() {info}"
        self.append_msg( msg )

        info           = widget.currentIndex()
        msg            = f".currentIndex() {info}"
        self.append_msg( msg )

        info           = widget.placeholderText()
        msg            = f".placeholderText() {info}"
        self.append_msg( msg )

        self.show_combo_values()   # move this code here

        self.append_msg( f"combo_info end { '' } --------", flush = True )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )
        # print( f"{self.little_widget_qlabel_1.text() = }" )  # setText() ??
        self.append_msg( f"{self.label_2.text() = }" )


        msg      = "set text for lable_1"
        self.append_msg( msg )
        self.label_1.setText( "mutate_0 self.label_1.setText" )


        # msg    = 'combo_2.lineEdit().setText( "mutate_0" )  '
        # self.append_msg( msg, clear = False )
        # self.combo_2.lineEdit().setText( "mutate_0" )  # for line edit

        # msg     = f"{self.combo_1.currentText =}"
        # self.append_msg( msg  )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        self.append_msg( f"{self.label_2.text() = }" )


        msg      = "set text for lable_1"
        self.append_msg( msg )
        self.label_1.setText( "mutate_1 self.label_1.setText" )



        # msg    = 'combo_2.setCurrentText( "2" )'
        # self.append_msg( msg, clear = False )
        # self.combo_2.setCurrentText( "2" )

        # msg    = 'combo_1.setCurrentIndex( 2 )'
        # self.append_msg( msg, clear = False )
        # self.combo_1.setCurrentIndex( 2 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_2" )

        # msg    = 'combo_2.setCurrentText( "2" )'
        # self.append_msg( msg, clear = False )
        # self.combo_2.setCurrentText( "2" )

        # msg    = 'combo_1.setCurrentIndex( 2 )'
        # self.append_msg( msg, clear = False )
        # self.combo_1.setCurrentIndex( 2 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        # make some locals for inspection
        my_tab_widget   = self
        # self_qlabel_1   = self.label_1
        # self_qlabel_2   = self.label_2
        self_widget_1   = self.widget_1
        self_widget_2   = self.widget_2

        wat_inspector.go(
             msg            = "self.text_edit from inspect method",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

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