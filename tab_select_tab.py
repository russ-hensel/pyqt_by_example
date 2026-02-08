#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
select tab to open by running key word search
"""
# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #qt_search.main()
# --------------------


import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import key_words
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

#import app_services
import global_vars
#import parameters
#import qt_search
import qt_sql_query
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import parameters

# ---- imports neq qt

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class Search_Tab( QWidget ) :
    def __init__(self):
        """
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()

        self._build_gui()
        self.mutate_ix   = 0

    # -------------------------------
    def _build_gui(self,   ):
        """
        layouts
            a vbox for main layout
            h_box for or each row of buttons
        """
        tab_page        = self
        layout          = QVBoxLayout( tab_page )

        widget          = QLabel("Enter key words to search for a widget or use  "
                        "-- Box works, list works...  "
                        "-- Capitilization... is ignored  "
                        "-- Click on widget list to add widget to select  ")

        layout.addWidget( widget  )

        # ---- QListWidget
        widget              = QListWidget(    )
        self.widget_list    = widget
        widget.setMaximumHeight( 100 )
        layout.addWidget( widget )

        widget.itemClicked.connect( self.widget_list_clicked )

        #values    =  [ "one", "two"]
        values    = global_vars.TAB_DB_BUILDER.widget_list
        for value in values:
            item = QListWidgetItem( value )
            widget.addItem( item )

        # ---- a row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget          = QLabel("Key Words-> ")
        row_layout.addWidget( widget )

        widget               = QLineEdit()
        self.key_word_widget = widget
        #widget.setText( "")
            #\n does not give second line
        # widget.setDisabled( True )
        # widget.setDisabled( False )
        widget.setPlaceholderText( "Enter your key words here" )  # clear to see
        widget.setText( parameters.PARAMETERS.default_search )
        # widget.textChanged.connect( self.on_text_changed ) # user or pro grammatically
        # widget.textEdited.connect(self.on_text_edited)  # user only
        widget.returnPressed.connect( self.criteria_select )
        # widget.editingFinished.connect(self.on_editing_finished) # done leaves control
        # widget.setReadOnly(True)
        # widget.setReadOnly(False)
        row_layout.addWidget( widget )

        # ---- clear
        widget = QPushButton("Clear")
        widget.clicked.connect( self.clear_select )
        row_layout.addWidget( widget,   )

        # ---- "Select"
        widget = QPushButton("Select")
        widget.clicked.connect( self.criteria_select )
        row_layout.addWidget( widget,   )

        # ---- a row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout, ) # stretch = 6  )


        # ---- model and view
        db                  = global_vars.TAB_DB
        model               = QSqlTableModel( self, db )
        self.list_model     = model


        model.setTable( "tabs" )
        model.setFilter( "id = -99" )  # afte set table to be effiective

        model.setEditStrategy( QSqlTableModel.EditStrategy.OnManualSubmit ) # = never QSqlTableModel.EditStrategy.OnManualSubmit

        # COMMENT  out to default  Set column headers	model.setHorizontalHeaderLabels([...])

        view                 = QTableView()
        self.list_view       = view
        view.setSelectionBehavior( QTableView.SelectRows )
        view.setModel( model )
        view.setSortingEnabled( True )
        row_layout.addWidget( view )

        view.clicked.connect( self.open_tab_select )

        # ---- headings
        """
        i have a QTableView how do i control the titles of the columns and their width ?
        """
        model.setHeaderData( 0, Qt.Horizontal, "Seq.")
        view.setColumnWidth( 0,  50   )

        ix   = 1
        model.setHeaderData( ix, Qt.Horizontal, "Tab Name"  )
        view.setColumnWidth( ix, 300  )

        ix   += 1
        model.setHeaderData( ix, Qt.Horizontal, "Widgets")
        view.setColumnWidth( ix, 500  )

        ix   += 1
        model.setHeaderData( ix, Qt.Horizontal, "Description")
        view.setColumnWidth( ix, 700  )

        ix   += 1
        model.setHeaderData( ix, Qt.Horizontal, "Module")
        view.setColumnWidth( ix, 300 )

        ix   += 1
        model.setHeaderData( ix, Qt.Horizontal, "Class")
        view.setColumnWidth( ix, 150  )

        # # suppress excess columns
        # ix   += 1
        # view.setColumnHidden( ix, True)

        # ix   += 1
        # view.setColumnHidden( ix, True)

        # ix   += 1
        # view.setColumnHidden( ix, True)
        #view.setModel( model )

        #model.setTable( "tabs" )  # suppresse above

        # Set specific column widths	table_view.setColumnWidth(column, width)
        # Auto-size columns	table_view.horizontalHeader().setSectionResizeMode()
        # Stretch columns to fit	QHeaderView.Stretch

    # ------------------------
    def widget_list_clicked( self, item ):
        """
        what it says
            item comes from the list
        """
        widget    = self.key_word_widget
        #text      = item.text()
        text      =  widget.text() + " " + item.text()
        widget.setText( text )

    # ------------------------
    def clear_select(self):
        """
        what it says
        """
        widget = self.key_word_widget
        widget.clear()

    # -------------
    def criteria_select( self,     ):
        """
        do the select
        comment out to remove errors
        """
        model                           = self.list_model

        query                           = QSqlQuery( QSqlDatabase.database( "tab_db" ) )
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "tabs_key_word"

        column_list                     = [ "id", "tab_title", "widgets",
                                           "description", "module", "class", "web_link"  ]

        a_key_word_processor            = key_words.KeyWords( kw_table_name, global_vars.TAB_DB )
        query_builder.table_name        = "tabs"
        query_builder.column_list       = column_list

        # ---- key words
        criteria_key_words              = self.key_word_widget.text()

        # criteria_key_words              = criteria_dict[ "key_words" ]
        criteria_key_words              = a_key_word_processor.string_to_key_words( criteria_key_words, caps_split = False )
        key_word_count                  = len(  criteria_key_words )

        criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
        criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

        if key_word_count > 0:
            query_builder.group_by_c_list   = column_list
            query_builder.sql_inner_join    = " tabs_key_word  ON tabs.id = tabs_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        query_builder.add_to_order_by( "tab_title", "ASC"   )

        query_builder.prepare_and_bind()

        # msg      = f"{query_builder = }"
        # print( msg )
        model.setFilter( "" )
        self.query_exec_model( query,
                               model,
                               msg = "tab criteria_select" )

        msg      = (  query.executedQuery() )
        #rint( f"{msg  = }" )

    # -------------------------------------------
    def query_exec_model(self, query, model,  msg = None ):
        """
        exec queries with some error checking
        return ok   = True if now error

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = None )
        """

        # wat_inspector.go(
        #      msg            = "query_exec_model",
        #      a_locals       = locals(),
        #      a_globals      = globals(), )


        # msg      = f"Executing SQL query:  {query.executedQuery() = }"
        # print( msg )

        if query.exec():
            model.setQuery( query )
            if model.lastError().isValid():
                msg     = f"Query Error: {model.lastError().text() = }"
                print( msg )
                return False

        else:
            print( "Query Execution Error:", query.lastError().text())
            print( msg )
            print( query.executedQuery()   )
            return False

        return True

    # ------------------------
    def open_tab_select(self, index ):
        """
        opens a tab that is clicked on
        goes to controller.open_tab_select


       sql for ref
           look in index_and_search.py ?
           """

        row         = index.row()
        model       = self.list_model
        column      = model.fieldIndex( "tab_title" )
        model_index = model.index( row, column)
        tab_title   = model.data( model_index ).strip()  # do strip before add to db

        column      = model.fieldIndex( "module" )     # file name less .py

        model_index = model.index( row, column)
        module      = model.data( model_index ).strip()
        splits      = module.rsplit( "/", maxsplit = 1 )
        if len( splits )  == 2:
            module  = splits[1]
        else:
            module  = splits[0]

        column      = model.fieldIndex( "class" )
        model_index = model.index( row, column)
        a_class     = model.data( model_index ).strip()

        column      = model.fieldIndex( "widgets" )
        model_index = model.index( row, column)
        widgets     = model.data( model_index ).strip()
        #rint( f"open_tab_select: {widgets} ====================================================")

        column      = model.fieldIndex( "web_link" )
        model_index = model.index( row, column)
        web_link     = model.data( model_index ).strip()

        ix          = global_vars.CONTROLLER.switch_to_tab_by_class_name( a_class )
        if ix >= 0:
            return

        #rint( f"open_tab_select: {row = },  {tab_title = }    {module = }   {a_class = }   ")

        global_vars.CONTROLLER.open_tab_select( module, a_class , tab_title, web_link, widgets = widgets  )


# ---- eof