#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
KEY_WORDS:      date edit time drop down
CLASS_NAME:     QDateEditTab
WIDGETS:        QDateEdit  CalendarPopup QDateTimeEdit
TAB_TITLE:      QDateEdit QDateTimeEdit / Reference
DESCRIPTION:    A reference for the QDateEdit and closely related widgets
HOW_COMPLETE:   20  #   ...
STATUS:         should not have a custom date edit, mutates should do more

What We Know About QDateEdit · russ-hensel/qt5_by_example Wiki
https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QDateEdit

"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QDateEdit"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #qt_fitz_book.main()
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

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

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


#wat_inspector    = wat.Wat( "joe")

# ---- end imports

INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.


# ----------------------------
class CustomDateEdit( QDateEdit ):
    """
    not used, might keep to show addition of a context meny
    but may want different name ....
    move a version to stuffdb
    custom_widget.pb   as CQDateEdit
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.help_file_name     =  "date_edit_widget_tab.txt"
        self.setCalendarPopup(True)

        self.setDate(QDate.currentDate())

    def contextMenuEvent(self, event):

        context_menu = QMenu(self)

        clear_action = QAction("Clear Date", self)
        today_action = QAction("Set to Today", self)

        clear_action.triggered.connect(self.clear_date)
        today_action.triggered.connect(self.set_to_today)

        context_menu.addAction(clear_action)
        context_menu.addAction(today_action)

        context_menu.exec_(event.globalPos())

    def clear_date(self):
        self.clear()

    def set_to_today(self):
        self.setDate(QDate.currentDate())

#  --------
class QDateEditTab( tab_base.TabBase  ):
    def __init__(self):
        """
        date_edit_tab.QDateEditTab
        """
        super().__init__()


        self.module_file       = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.date_format       = "dd/MM/yyyy"

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
        layout              = QGridLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )


        ix_row        = 0
        ix_col        = 0

        widget  = QLabel( "start_date_widget w/o popup" )
        layout.addWidget( widget, ix_row, ix_col )   # row column alignment

        ix_col                  += 1
        #widget                  = QDateEdit()
        #widget                  = CustomDateEdit()   # with context menu fro chat
        widget                  = QDateEdit()
        self.start_date_widget  = widget
        # widget.userDateChanged.connect( lambda: self.date_changed( ) )
        # widget.editingFinished.connect( lambda: self.date_changed( ) )
        #widget.setCalendarPopup( True )
        widget.setDate(QDate( 2022, 1, 1 ))
        layout.addWidget( widget, ix_row, ix_col )

        # ----
        ix_col    += 1
        widget  = QLabel( "end_date_widget -> (see _build_gui) ->" )
        layout.addWidget( widget, ix_row, ix_col )

        """
           dateEdit->setSpecialValueText( " " );
           dateEdit->setDate( QDate::fromString( "01/01/0001", "dd/MM/yyyy" ) );
        """
        ix_col                  += 1
        widget                  = QDateEdit()
        self.end_date_widget    = widget
        widget.setCalendarPopup( True )
        widget.setDate(QDate( 2025, 1, 1 ))
        widget.setMinimumDate(QDate(1900, 1, 1))
        widget.setMaximumDate(QDate(2100, 12, 31))
        widget.setDisplayFormat( self.date_format )   # = "dd/MM/yyyy"
        widget.setSpecialValueText( " " )    # this will then reepor minimun date
        invalid_date            = QDate().fromString( "01/01/0001", self.date_format )
        widget.setDate( invalid_date )
        #widget.setDate(QDate( None, None, None, )) not ok
        widget.editingFinished.connect( lambda: self.date_changed(   ) )
        #placer.place( a_widget )
        layout.addWidget( widget, ix_row, ix_col )

        # ----- QDateTimeEdit
        ix_row                  += 1
        ix_col                  = 0
        # Create a QDateTimeEdit widget
        widget            = QDateTimeEdit( )
        self.dateTimeEdit = widget

        # Set a default date/time
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        widget.setCalendarPopup(True)

        self.dateTimeEdit.setGeometry(50, 50, 200, 30)

        layout.addWidget( widget, ix_row, ix_col )

        # ---- QTimeEdit
        ix_row                  += 1
        ix_col                  =0
        # Create a QTimeEdit widget
        widget          = QTimeEdit( self )
        self.timeEdit   = widget


        # Set a default time -- some error here
        #self.timeEdit.setTime( QTime.currentTime() )

        # Set a custom display format
        self.timeEdit.setDisplayFormat("HH:mm:ss")

        # Set the widget geometry
        self.timeEdit.setGeometry(50, 50, 150, 30)

        widget.setDisplayFormat("HH:mm")

        # Show hours, minutes, and seconds (24-hour format)
        widget.setDisplayFormat("HH:mm:ss")
        widget.setDisplayFormat("hh:mm:ss AP")


        widget.setMinimumTime(QTime(8, 0, 0))
        widget.setMaximumTime(QTime(18, 0, 0))

        # Set the time step to 15 minutes
        #widget.setSingleStep( 15 )   # fails

        # Enable time wrapping
        widget.setWrapping( True )

        # Enable keyboard tracking to update immediately
        widget.setKeyboardTracking( True )

        # Clear the time edit field
        widget.clear()

        layout.addWidget( widget, ix_row, ix_col )

        # ---- buttons ---------------------------------
        ix_row    += 1
        ix_col    = 0
        layout.addLayout( button_layout, ix_row, ix_col )

        # # ---- Inspect
        # widget = QPushButton("inspect")
        # # widget.clicked.connect(lambda: self.print_message(widget.text()))
        # a_widget        = widget
        # widget.clicked.connect( lambda: self.inspect( ) )
        # button_layout.addWidget( widget )

        # # ----set_empty
        # widget = QPushButton("set_empty\n")
        # widget.clicked.connect(lambda: self.set_empty( ))
        # a_widget        = widget
        # button_layout.addWidget( widget )

        self.build_gui_last_buttons( button_layout )

    # ------------------------------------
    def set_empty( self ):
        """
        not currently called may be deleted as not useful or not
        what is says
        this is sort of a hack, remove for now
        """
        self.append_function_msg(  "set_empty" )

        invalid_date     = QDate().fromString( "01/01/0001", "dd/MM/yyyy" )
        self.end_date_widget.setDate( invalid_date )

    # ------------------------------------
    def to_unix( self, qdate, ): # date_format = None ):
        """
        read it
        need a begin of day and an end of day this is end i think
        from chat
        """
        """
        what is says
        """
        self.append_function_msg(  "to_unix" )

        # # Example QDate object
        # qdate = QDate(2024, 9, 16)

        # # Convert QDate to QDateTime (time will be set to 00:00:00 by default)
        qdatetime       = QDateTime( qdate )

        unix_timestamp  = qdatetime.toSecsSinceEpoch()

        print(f"QDate: {qdate}")
        print(f"Unix Timestamp: {unix_timestamp}")

        return unix_timestamp

    # ------------------------------------
    def mutate_extract( self ):
        """
        read it
        some conversions from chat

        I have a QDateEdit i get the qdate from it.
        I want to convert the qdate to a unit time, the last
        second of the date,

        and second I want to convert the date to
        the first second of the date,

        and finally i want to convert
        the date to the last second of the day before the date.

        Assume the date and times are GMT

        """
        self.append_function_msg(  "mutate" )

        qdatetime       = QDateTime.fromSecsSinceEpoch( int( time.time() ) )
        qdate           = qdatetime.date()

        self.start_date_widget.setDate( qdate  )

    # ------------------------------------
    def inspect_old( self ):
        """
        read it

        """
        print( "\n\n---------------------------------------")
        print( f"w/o popup  {self.start_date_widget.date() = }" )  # setText()   ??
        print( f"w   popup  {self.end_date_widget.date() = }" )  # setText()   ??
        a_date            = self.end_date_widget.date()

        unix_time_stamp   = self.to_unix( a_date,   )
        print( f"w   popup   self.end_date_widget.date() ={ unix_time_stamp }" )
        # from PyQt5.QtCore import QDateTime

        # # Example Unix timestamp (for September 16, 2024, 00:00:00)
        # unix_timestamp = 1726444800

        # Convert Unix timestamp to QDateTime
        qdatetime         = QDateTime.fromSecsSinceEpoch( unix_time_stamp )

        print(f"Unix Timestamp: {unix_time_stamp}")
        print(f"QDateTime: {qdatetime.toString('yyyy-MM-dd hh:mm:ss')}")

        print(f"QDateTime: {qdatetime.toString(Qt.ISODate)}")

        qdate = qdatetime.date()

        print(f"QDate: {qdate.toString(Qt.ISODate)}")


    def qdate_to_unix_last_second( self, qdate):
        """ Convert QDate to Unix timestamp for the last second of the day (23:59:59) """
        qdatetime = QDateTime(qdate, QDateTime().time().fromString("23:59:59", "hh:mm:ss"), Qt.UTC)
        unix_time = qdatetime.toSecsSinceEpoch()  # Get Unix timestamp in seconds
        return unix_time

    def qdate_to_unix_first_second(self, qdate):
        """ Convert QDate to Unix timestamp for the first second of the day (00:00:00) """
        qdatetime = QDateTime(qdate, QDateTime().time().fromString("00:00:00", "hh:mm:ss"), Qt.UTC)
        unix_time = qdatetime.toSecsSinceEpoch()  # Get Unix timestamp in seconds
        return unix_time

    def qdate_to_unix_last_second_previous_day(self, qdate):
        """ Convert QDate to Unix timestamp for the last second of the previous day (23:59:59) """
        qdate_previous = qdate.addDays(-1)  # Get the previous day
        qdatetime = QDateTime(qdate_previous, QDateTime().time().fromString("23:59:59", "hh:mm:ss"), Qt.UTC)
        unix_time = qdatetime.toSecsSinceEpoch()  # Get Unix timestamp in seconds
        return unix_time

    # --------
    def date_changed( self,   ):
        """
        what is says
        """
        self.append_function_msg(  "date_changed()" )

        #print( f"{arg = }")

        self.append_msg( tab_base.DONE_MSG )

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

        my_tab_widget               = self
        self_start_date_widget      = self.start_date_widget
        self_timeEdit               = self.timeEdit
        wat_inspector.go(
             msg            = "from inspect method !! needs more locals",
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
