#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_q_table_widget.py
self.help_file_name     =  "q_table_widget_tab.txt"

KEY_WORDS:      table widget tabular data display click select headers pp tablewidget qtable
CLASS_NAME:     QTableWidgetTab
WIDGETS:        QTableWidget
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      QTableWidget

"""

# --------------------
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
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAbstractItemView,
                             QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDataWidgetMapper,
                             QDateEdit,
                             QDateTimeEdit,
                             QDialog,
                             QDoubleSpinBox,
                             QFormLayout,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QHeaderView,
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
                             QSpinBox,
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)


import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports


INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.




#-----------------------------------------------
class QTableWidgetTab( tab_base.TabBase  ):
    """
    here build a tab in its own class to hide its variables
    """
    def __init__(self, ):
        """
        """
        super().__init__( )

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        self.mutate_dict[4]     = self.mutate_4

        self.help_file_name     =  "q_table_widget_tab.txt"
        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        table_widget        = QTableWidget(4, 5)  # row, column ??third arg parent
        self.table_widget   = table_widget
        layout.addWidget( table_widget )

        # ---- insert data --- now a mess, parameterize this
        print( "this adds cell 'upside down' and cell cords are ng ")
        for i in range( 4, 0,   -1 ):  # better match table
            for j in range( 5,  0, -1 ):  # col
                # these items arguments must be strings
                item     = QTableWidgetItem( "Cell ({}, {})".format( i, j) )
                table_widget.setItem(i, j, item)

        ix_col   = 1
        table_widget.setColumnWidth( ix_col, 22 )
        # Set selection behavior and mode

        print( "how select_row works may depend on these ")
        table_widget.setSelectionBehavior( QAbstractItemView.SelectRows )  # Can be SelectRows, SelectColumns, or SelectItems
        # table_widget.setSelectionMode(QAbstractItemView.MultiSelection)  # Can be SingleSelection or MultiSelection

        # set row count works but messes up model
        # row_count   = 2
        # a_widget.setRowCount( row_count )  # increase or decrease rows

        print( "also setColumnCount()  ")

        #self.table.setHorizontalHeaderLabels(employees[0].keys())

        labels  = [ "label0" ]   #ok
        labels  = [ "label0", "label1",
                    "label2", "label3", "label4" ] # too many also ok

        table_widget.setHorizontalHeaderLabels( labels  )
        table_widget.setSortingEnabled( True )

        table_widget.cellClicked.connect( self.on_cell_clicked )

        # getting an error !!
        print( f"{table_widget.currentRow()}")
            # method returns the currently selected row. It returns -1 i

        # ---- buttons
        button_layout = QHBoxLayout()
        layout.addLayout( button_layout )

        # --- begin a_widget method
        a_widget           = QPushButton("add_row\n_at_end")
        a_widget.clicked.connect(self.add_row_at_end)
        button_layout.addWidget(a_widget)

        # select a row
        a_widget           = QPushButton("select_\nrow_3 ( 0 based )")
        a_widget.clicked.connect(self.select_row_3)
        button_layout.addWidget(a_widget)

        # delete or remove a row
        a_widget           = QPushButton("remove_row\n_current")
        a_widget.clicked.connect(self.remove_row_currrent)
        button_layout.addWidget(a_widget)

        # delete or remove a row
        a_widget           = QPushButton("set_size\n")
        a_widget.clicked.connect(self.set_size)
        button_layout.addWidget(a_widget)

        #
        a_widget           = QPushButton("sort\n")
        a_widget.clicked.connect(self.sort)
        button_layout.addWidget(a_widget)

        # # ---- search
        # a_widget           = QPushButton( "search\n" )
        # a_widget.clicked.connect( self.search )
        # button_layout.addWidget(a_widget)

        # ---- mutate
        widget = QPushButton("mutate\n")
        self.button_ex_1         = widget
        widget.clicked.connect( lambda: self.mutate( ) )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to          = self.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = self.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

    # -------------------------------------
    def populate_table(self):
        """
        Populate the table with some sample data
        """
        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(f"Item {row + 1}, {col + 1}")
                self.table_widget.setItem(row, col, item)

    # -------------------------------------
    def select_row_3(self,  ):
        """
        what it says
        """
        self.append_function_msg( "select_row_3" )

        self.select_row( 3 )

    # -------------------------------------
    def select_row(self, row_index):
        """
        Select a specific row.
        may depend on selection mode
        """
        self.append_function_msg( "select_row" )

        print( f"select_row {row_index = }")
        self.table_widget.selectRow( row_index )
        self.table_widget.show()

    # -------------------------------------
    def select_column(self, col_index):
        """
        Select a specific column.
        """
        self.append_function_msg( "select_column" )

        self.table_widget.selectColumn(col_index)

    # ------------------------------
    def on_cell_clicked( self, row, col  ):
        """
        read it

        """
        self.append_function_msg( "on_cell_clicked" )

        table      = self.table_widget

        item       = table.item( row, col )
        if item:
            print(f"Cell clicked: Row {row}, Column {col}, Data: {item.text()}")
        else:
            print(f"Cell clicked: Row {row}, Column {col}, Data: None")

        print( "enable some select if you wish ")
        self.select_row( row )

    # some of next may be mixed up with tableModel, beware
    # -------------------------------------
    def add_row_at_end(self):
        """ """
        self.append_function_msg( "add_row_at_end" )

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow( row_position )

    # -------------------------------------
    def remove_row_currrent(self):
        """
        what it says
        """
        self.append_function_msg( "remove_row_current" )

        row_position = self.table_widget.currentRow()
        self.table_widget.removeRow( row_position )

    # -------------------------------------
    def remove_row_currrent_what(self):
        """
        what it says
        """
        self.append_function_msg( "remove_row_current" )
        # ---- insert data --- now a mess, parameterize this
        msg     = ( "this adds cell 'upside down' and cell cords are ng ")
        self.append_msg( msg,  )
        table_widget   = self.table_widget
        for i in range( 4, 0,   -1 ):  # better match table
            for j in range( 5,  0, -1 ):  # col
                # these items arguments must be strings
                item     = QTableWidgetItem( "Cell ({}, {})".format( i, j) )
                table_widget.setItem(i, j, item)

    # -------------------------------------
    def select_column(self, col_index):
        """Select a specific column."""
        self.table_widget.selectColumn(col_index)


    # ------------------------------
    def set_size(self):
        """
        read it
        """
        self.append_function_msg( "set_size")



        table   = self.table_widget
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.append_msg( "set_size done" )

    # ------------------------------
    def sort(self):
        """
        read it
        """
        self.append_function_msg( "sort")

        # !! more research on args
        self.table_widget.sortItems ( 1, Qt.AscendingOrder  )

        self.append_msg( "sort done" )

    # ------------------------------
    def search(self, search_for   = "1," ):
        """
        read it
        passing of argument unclear ????
        """
        self.append_function_msg( "search")

        search_for   = "1,"
        msg          = f"search {search_for = }"
        self.append_msg( msg,  )
        a_widget    =    self.table_widget
        # Clear current selection.
        a_widget.setCurrentItem( None )

        if not search_for:
            msg      =  "Empty string, don't search."
            self.append_msg( msg,  )
            return

        matching_items = a_widget.findItems(search_for,  Qt.MatchContains )
        if matching_items:
            # We have found something.
            item       = matching_items[0]  # Take the first.
            msg        = f"found {item = }"
            self.append_msg( msg,  )
            a_widget.setCurrentItem(item)
        else:
            msg        = f"nothing found {search_for = }"
            self.append_msg( msg,  )


    # ------------------------------------
    def mutate_x( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg,  )

        self.append_msg( "mutate_0 done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "hide some stuff"
        self.append_msg( msg, clear = False )

        table   = self.table_widget
        table.hideRow( 1 )
        table.hideColumn( 1 )

        self.append_msg( "mutate_0 done" )



    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "show some stuff"
        self.append_msg( msg, )
        table   = self.table_widget
        table.showRow( 1 )
        table.showColumn( 1 )

        self.append_msg( "mutate_1 done" )



    #----------------------------
    def mutate_2( self  ):
        """
        read it
        """
        self.append_function_msg( "mutate_2" )
        self.append_msg( "was copy of mutat_1 now nothing " )

        self.append_msg( "mutate_2 done" )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets



        def horizontalHeader(…) # horizontalHeader(self) -> Optional[QHeaderView]
        def horizontalHeaderItem(…) # horizontalHeaderItem(self, column: int) -> Optional[QTableWidgetItem]
        def setHorizontalHeader(…) # setHorizontalHeader(self, header: Optional[QHeaderView])
        def setHorizontalHeaderItem(…) # setHorizontalHeaderItem(self, column: int, item: Optional[QTableWidgetItem])

        def setHorizontalHeaderLabels(…) # setHorizontalHeaderLabels(self, labels: Iterable[Optional[str]])


        def setVerticalHeader(…) # setVerticalHeader(self, header: Optional[QHeaderView])
        def setVerticalHeaderItem(…) # setVerticalHeaderItem(self, row: int, item: Optional[QTableWidgetItem])
        def setVerticalHeaderLabels(…) # setVerticalHeaderLabels(self, labels: Iterable[Optional[str]])
        def takeHorizontalHeaderItem(…) # takeHorizontalHeaderItem(self, column: int) -> Optional[QTableWidgetItem]
        def takeVerticalHeaderItem(…) # takeVerticalHeaderItem(self, row: int) -> Optional[QTableWidgetItem]
        def verticalHeader(…) # verticalHeader(self) -> Optional[QHeaderView]
        def verticalHeaderItem(…) # verticalHeaderItem(self, row: int) -> Optional[QTableWidgetItem]


        """
        self.append_function_msg( "mutate_3" )

        msg    = "mess with column headers and col width "
        self.append_msg( msg, clear = False )

        table       = self.table_widget

        # Set horizontal headers --- all at once
        headers = ["Name", "Age", "City"]
        table.setHorizontalHeaderLabels( headers )

        table.setColumnWidth(2, 100)  # Set specific width for a column


        self.append_msg( "mutate_3 done" )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_4" )


        #self.append_msg( msg,  )



        msg    = ( "mutate_4 -- change headers one at a time a bit of a mess " )
        self.append_msg( msg,  )

        table            = self.table_widget

        for ix_col, i_header_text in enumerate(  [ "XXX", "AAA", ] ):
            table.setHorizontalHeaderItem( ix_col, QTableWidgetItem( i_header_text )  )
          #  table.setHorizontalHeaderItem( ix_col, QTableWidgetItem( i_column.col_head_text )  )

    #from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView

        table.setColumnWidth(2, 10)  # Set specific width for a column

        # # Set horizontal headers --- all at once
        # headers = ["Name", "Age", "City"]
        # table.setHorizontalHeaderLabels( headers )

            # # Set vertical headers
            # vertical_headers = ["1", "2", "3"]
            # table_widget.setVerticalHeaderLabels(vertical_headers)

        # Customize header parameters
        header = table.horizontalHeader()
        print( header )

        # Set column widths
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # First column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Auto-size based on content
        header.setSectionResizeMode(2, QHeaderView.Interactive)  # Manually resizable


        # table_widget.setColumnWidth(2, 100)  # Set specific width for a column

        # Customize alignment of header text
        header_item = table.horizontalHeaderItem( 0 )  # Access a header item
        if header_item:
            header_item.setTextAlignment( Qt.AlignLeft )

    # Header Alignment:

    #     Use QTableWidgetItem.setTextAlignment(Qt.AlignmentFlag) for alignment.

    # Row Height:

    #     Customize row height similarly with setRowHeight.

    # Header Styling:

    #     Header items can be styled using QTableWidgetItem (e.g., font, color).

    # Interactive Resizing:

    #     Users can resize columns manually with Interactive.


    # # Customize vertical header (optional)
    # vertical_header = table_widget.verticalHeader()
    # vertical_header.setSectionResizeMode(QHeaderView.Stretch)  # Stretch rows

        self.append_msg( "mutate_4 done" )


    #----------------------------
    def find_row_with_text_in_column(self, ):
        """
        !! revisit  -- seems not to be connected
        might be faster
        might be wrong depending on how matching works
        from chat
        may be ok not yet tested
        """
        self.append_function_msg( "find_row_with_text_in_column broken comment out fix me " )


        return

        table               = self.table_widget

        ix_col_searched     = 2
        ix_found            = None
        target_text         = "xyz"

        matching_items      = table.findItems(target_text, QtCore.Qt.MatchExactly )
        for item in matching_items:
            if item.column() == column:
                ix_found            =  item.row()

        print( f"find_row_with_text {ix_found = }")

        return ix_found



    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection
        self_table_widget   = self.table_widget

        wat_inspector.go(
             msg            = "inspect...",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "inspect done" )

    # ------------------------
    def breakpoint(self):
        """
        the usual
        """
        self.append_function_msg( "breakpoint" )


        # #__file__

        # print( f"{__file__ = }" )

        # clipboard = QApplication.clipboard()

        # clipboard.setText( str( __file__ ) )

        # print("Text added to clipboard:", clipboard.text())

        breakpoint()

        self.append_msg( "breakpoint done" )

# ---- eof