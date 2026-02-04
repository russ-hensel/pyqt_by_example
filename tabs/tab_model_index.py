#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof

"""
self.help_file_name     =  "table_model_tab.txt"

KEY_WORDS:      model table with an index rsh custom maybe with headers select rows columns
CLASS_NAME:     Model_Index_Tab
WIDGETS:        QAbstractTableModel QTableView.
STATUS:         works
TAB_TITLE:      Model/ModelIndex

"""


"""
from:
/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/widgets_list.py
  widgets_list.py
"""

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

import table_model
import wat
from PyQt5 import QtGui
from PyQt5.QtCore import (QAbstractTableModel,
                          QDate,
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

import utils_for_tabs as uft
import wat_inspector
import global_vars

# ---- imports neq qt


# ---- end imports

print_func_header   = uft.print_func_header


# ------------------------
class ATableModelxxx( QAbstractTableModel ):
    """
    use a a list of file names from browse
    may be more generally useful
    code derived from chat
    was in
    import qt_table_model
    """
    def __init__(self,  headers):
        super().__init__()
        self._data      = []
        self._headers   = headers
        self.indexer    = None
        """
        model.indexer.index_tuple = ( 0, 1 )
        """
    #-------
    def add_indexer (self, index_tuple ):
        """
        what it says read
        index tuple for now pair of column numbers to use as an index to model

        """
        self.indexer    = table_model.ModelIndexer( self, index_tuple  )

    #-------
    def rowCount(self, index=None):
        """
        what it says read
        why index = None, drop it
        """
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def set_data(self, data ):
        self._data      = data

    # def add_data(self, data ):
    #     pass


    def set_data_at_index(self, index, value, role=Qt.EditRole):
        """
        index might be index = model.index(ix_row,  ix_col )  # Row 1, Column 1

        Args:
            index (TYPE): DESCRIPTION.
            value (TYPE): DESCRIPTION.
            role (TYPE, optional): DESCRIPTION. Defaults to Qt.EditRole.

        Returns:
            bool: DESCRIPTION.

        """
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value  # Update the data
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
                # Emit dataChanged signal for this index
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)

    # Method to add a row
    def addRow(self, row_data):
        """
        read
        row_data   a list of the data types ??
        remember to invalidate index if any --- may build in or not
        """
        self.beginInsertRows(self.index(len(self._data), 0), len(self._data), len(self._data))
        self._data.append(row_data)
        self.endInsertRows()

    # Optional method to remove a row
    def removeRow(self, row_index):
        """
        what it says, read
        """
        self.beginRemoveRows(self.index(row_index, 0), row_index, row_index)
        self._data.pop(row_index)
        self.endRemoveRows()

    # ---------------------------
    def clear_data(self):
        """
        what it says, read
        """
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

#-----------------------------------------------
class Model_Index_Tab( QWidget ):
    """
    and table view
    from  QAbstractTableModel
    see ez_qt table_widget and table_model table_widget
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__( )
        self.help_file_name     =  "table_model_tab.txt"
        self.build_model()
        self.build_tab()

    #-----------------------------------------------
    def build_tab( self, ):
        """
        the usual
        """
        self.table_model_is_hidden  = False

        tab_page      = self
        layout        = QVBoxLayout( tab_page )

        button_layout = QHBoxLayout(   )

        headers = ["Name", "Age", "Occupation" ]
        #self.view           = QTableView()
        self.table_model            = table_model.TableModel( headers )  # QAbstractTableModel
        #self.model.set_data( data )

        table_view                  = QTableView()
        self.table_model_table_view = table_view
        self.table_view             = table_view
        # Connect the clicked signal to a slot
        #table_view.doubleClicked.connect( self.double_clicked )
        #table_view.doubleClicked.connect( self.clicked )
        table_view.clicked.connect( self.table_clicked  )
        table_view.setModel( self.table_model )

        print( "some selection options" )
        table_view.setSelectionBehavior( QTableView.SelectRows )       # For row selection
        # table_view.setSelectionBehavior( QTableView.SelectColumns )  # For column selection
        # table_view.setSelectionBehavior(QTableView.SelectItems)      # For item selection

        layout.addWidget( table_view )

        layout.addWidget( self.persons_view   )

        #layout.addWidget( self.phone_view    )

        # ---- QPushButtons
        layout.addLayout( button_layout )
        # widget        = QLabel( 'table_model\n TableModel()/QTableView()' )
        # button_layout.addWidget( widget )

        # widget          = QPushButton("QPushButton")
        # # widget.clicked.connect(lambda: self.print_message(widget.text()))
        # a_widget        = widget
        # #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        # button_layout.addWidget( widget )

        #button_layout.addWidget( widget )

        widget        = QPushButton('persons_\nselect_all')
        widget.clicked.connect(self.persons_select_all )
        button_layout.addWidget( widget )

        #-------------
        widget          = QPushButton( "table_model_\ntab_populate" )
        widget.clicked.connect( lambda: self.table_model_tab_populate() )
        button_layout.addWidget( widget )

        #-------------
        widget = QPushButton("table_model_\ntab_get_data")
        widget.clicked.connect(lambda: self.table_model_tab_get_data( ) )
        #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        button_layout.addWidget( widget )

        # #-------------!! revisit
        # widget = QPushButton("hide/\nunhide")
        # widget.clicked.connect(lambda: self.table_model_hide_unhide( ) )
        # a_widget        = widget
        # #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        # button_layout.addWidget( widget )

        #-------------
        widget = QPushButton("hide/\nunhide column")
        widget.clicked.connect(lambda: self.table_model_toggle_hide_column( ) )
        #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        button_layout.addWidget( widget )

        layout.addLayout( button_layout )

        # widget        = QPushButton('add_\nindexers')
        # widget.clicked.connect(self.add_indexers )
        # button_layout.addWidget( widget )

        widget        = QPushButton('table_model\n_inspect')
        widget.clicked.connect(self.table_model_inspect )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget = QPushButton("inspect\n")
        widget.clicked.connect( self.inspect    )
        button_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton("breakpoint\n")
        widget.clicked.connect( self.breakpoint    )
        button_layout.addWidget( widget,   )

        self.add_indexers()

    # ------------------------------
    def build_model( self,   ):
        """
        build model and views if used here

        """
        #print_func_header( "_build_model" )
        # ---- persons
        model                  = QSqlTableModel( self, global_vars.EX_DB )
        self.persons_model      = model
        model.setTable('persons')

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
            #  OnFieldChange , OnRowChange , and OnManualSubmit .

        model.setHeaderData(2, Qt.Horizontal, "Age*" ) # QtHorizontal in c
        #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

        view                    = QTableView( )
        self.persons_view        = view
        view.setModel( model  )
        view.hideColumn( 0 )       # hide is hear but header on model
        view.setSelectionBehavior( QTableView.SelectRows )
        #view.clicked.connect( self._persons_view_clicked  )
        view.clicked.connect( self.persons_view_clicked  )

    # -------------------------------------
    def table_model_tab_populate(self,   ):
        """
        what it says
            seems ok
        populates a row at a time
        """
        print_func_header( "table_model_tab_populate" )

        model      = self.table_model
        #print( f" add_to_model_all_subjects {photo_id = } , {table = }, {table_id = },  {info =} "  )
        #key           = ( table, table_id )
        #key_row       = model_display.indexer.find( key )
        # set_row_of_data
        for ix in range( 3 ):
            # self.view_all_subjects.setModel(  self.model_all_subjects )
            # model        = self.model_display
            row_data     = [  f"a{ix}", f"b{ix}",   f"c{ix}", f"d{ix}"   ]
            #rint( f"{row_data = }")
            model.addRow( row_data)
            #model_display.indexer.set_is_valid( False )
        # set value at index
        an_index       = model.index( 2,2 )
        value          = 9999
        model.set_data_at_index(  an_index, value,  )

    #---------------------------------------
    def table_model_hide_unhide( self ):
        """
        once filter applied not sure how to remove
        this is messed up might want to start over with chat
        !! revisit
        """
        print_func_header( "table_model_hide_unhide !! fix me " )

        if self.table_model_filter:
            self.table_model_filter   = FilterProxyModelHideRows( )

    # ------------------------
    def persons_select_all(self):
        """ """
        print_func_header( "select_all" )

        self.persons_model.select()  # Load the data into the model

        # self.phone_model.setFilter( "" )
        # self.phone_model.select()


    #-----------------------------------------------
    def double_clicked( self, index: QModelIndex):
        """
        what it says,
        index comes from table view
        """
        print_func_header( "double_clicked" )

        model    = self.table_model
        row      = index.row()
        print( f"on_row_other_clicked {row = }")
        #self.add_ix_other( row )

    #-----------------------------------------------
    def persons_view_clicked( self, index: QModelIndex):
        """
        what it says,
        index comes from table view
        """
        print_func_header( "persons_view_clicked" )

        model       = self.persons_model
        row_ix      = index.row()
        print( f"persons_view_clicked {row_ix = }")

        model          = self.persons_model
        # row_start      = model.index(row_index, 0)
        # row_end        = model.index(row_index, model.columnCount() - 1)

        # Select the row
        # selection_model.select( row_start, selection_model.Select | selection_model.Rows )

        key      = []

        index   = model.index( row_ix, 0 )
        data    = model.data( index )
        key.append( data )

        index   = model.index( row_ix, 1 )
        data    = model.data( index )
        key.append( data )

        # but the key needs to be a tuple
        key     = tuple( key )
        print( f"key for clicked row { row_ix = }  is {key = } ")

        # now try to find
        indexer       =  self.persons_indexer
        indexer.refresh_index()
        found_ix      = indexer.find( key )

        print( f"key found at {found_ix = } ")


    #-----------------------------------------------
    def table_clicked( self, index: QModelIndex):
        """
        what it says,
        index comes from table view
        """
        print_func_header( "table_clicked" )

        model    = self.table_model
        row      = index.row()
        print( f"table_clicked {row = }")

        self.select_row( row )

    #-----------------------------------------------
    def select_row(self, row_index ):
        """Select a specific row."""

        print_func_header( "select_row" )

        # Get the selection model from the view
        selection_model = self.table_view.selectionModel()

        # Create an index for the row
        model          = self.table_model
        row_start      = model.index(row_index, 0)
        row_end        = model.index(row_index, model.columnCount() - 1)

        # Select the row
        selection_model.select( row_start, selection_model.Select | selection_model.Rows )

        key      = []

        index   = model.index( row_index, 0 )
        data    = model.data( index )
        key.append( data )

        index   = model.index( row_index, 1 )
        data    = model.data( index )
        key.append( data )

        # but the key needs to be a tuple
        key     = tuple( key )
        print( f"key for first selected row { row_index = }  is {key = } ")

        # now try to find

        indexer       =  self.table_model.indexer
        indexer.refresh_index()
        found_ix      = indexer.find( key )

        print( f"key found at {found_ix = } ")

    # ----------------------------
    def select_column(self, col_index):
        """
        Select a specific column.
        may want to test and hook up
        """
        print_func_header( "select_column" )

        # Get the selection model from the view
        selection_model = self.table_view.selectionModel()

        # Create an index for the column
        col_start       = self.model.index(0, col_index)
        col_end         = self.model.index(self.model.rowCount() - 1, col_index)

        # Select the column
        selection_model.select(col_start, selection_model.Select | selection_model.Columns)

    #-----------------------------------------------
    def table_model_toggle_hide_column(self,   ):
        """
        we actually use the view
        """
        print_func_header( "table_model_toggle_hide_column" )

        self.table_model_is_hidden  = not self.table_model_is_hidden
        if self.table_model_is_hidden:
            self.table_model_table_view.hideColumn( 1 )
        else:
            self.table_model_table_view.showColumn( 1 )

        self.table_model_table_view.show()

    #-----------------------------------------------
    def table_model_tab_get_data(self,   ):
        """
        what it says
        seem ok
        """
        print_func_header( "table_model_tab_get_data" )

        model           = self.table_model

        # !!table_model.model_dump( model )

        data_list       = [  ]
        ix_row          = 0
        for ix_col in range( 3 ):
            index     = model.index( ix_row, ix_col )
            data      = model.data( index, ) #role=Qt.DisplayRole)
            data_list.append( data )
        print( f"table_model_tab_get_data   {data_list = }" )

    # ------------------------------------------
    def table_model_inspect(self):
        """
        what it says, read
        """
        # ia_qt.ia_obj( self.table_model,             msg = "table_model_inspect" )
        # ia_qt.ia_obj( self.table_model_table_view,  msg = "table_view_inspect" )
        # ia_qt.q_abstract_table_model( self.table_model,   msg = "table_model_inspect" )
        print_func_header( "table_model_inspect" )

        view     = self.table_model_table_view
        # def get_selected_row_and_column():
        selected_indexes = view.selectionModel().selectedIndexes()
        if selected_indexes:
            for index in selected_indexes:
                row     = index.row()
                column  = index.column()
                print(f"Selected Cell - Row: {row}, Column: {column}")
        else:
            print("No selection")

    # ------------------------------------------
    def add_row_at_end(self):
        """
        may work needs to be hooked up
        """
        print_func_header( "add_row_at_end" )

        row_position = self.table_widget_1.rowCount()
        self.table_widget_1.insertRow( row_position )

    # ------------------------------------------
    def remove_row_currrent(self):
        """
        may work needs to be hooked up
        """
        print_func_header( "remove_row_currrent" )

        row_position = self.table_widget_1.currentRow()
        self.table_widget_1.removeRow(row_position)

    # ------------------------------
    def set_size(self):
        """
        read it
        may work needs to be hooked up
        """
        print_func_header( "set_size" )

        self.table_widget_1.horizontalHeader().setStretchLastSection(True)
        self.table_widget_1.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

    # ------------------------------
    def sort(self):
        """
        read it
        """
        """
        may work needs to be hooked up
        """
        print_func_header( "sort" )

        # !! more research on args
        self.table_widget_1.sortItems (  1 , Qt.AscendingOrder  )

    # ------------------------------
    # def on_list_clicked( self  index: QModelIndex ): ) :
    #     """
    #     read it
    #     """
    #     msg   = "click headers to sort   "
    #     print( msg )
    # ------------------------------
    def on_cell_clicked( self, row, col  ):
        """
        read it

        may work needs to be hooked up
        """
        print_func_header( "on_cell_clicked" )

        table      = self.table_widget_1

        item       = table.item( row, col )
        if item:
            print(f"Cell clicked: Row {row}, Column {col}, Data: {item.text()}")
        else:
            print(f"Cell clicked: Row {row}, Column {col}, Data: None")

    # ------------------------------
    def add_indexers(self,   ):
        """

        """
        print_func_header( "add_indexer" )

        index_tuple    = ( 0, 1 ) # columns in index
        self.indexer   = self.table_model.add_indexer( index_tuple )

        index_tuple             = ( 0, 1 ) # columns in index
        self.persons_indexer     =  table_model.ModelIndexer( self.persons_model, index_tuple )
        self.persons_indexer.refresh_index()

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        self_table_model    = self.table_model
        #self_table_view     = self.table_view
        table_indexer       = self.table_model.indexer
        self_persons_indexer = self.persons_indexer
        wat_inspector.go(
             msg            = "tbd add more locals",
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        print_func_header( "breakpoint" )

        breakpoint()

# ---- eof
