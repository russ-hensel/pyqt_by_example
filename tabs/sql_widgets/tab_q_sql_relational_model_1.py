#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


tab_q_sql_relational_model_1.QSqlRelationalTableModelTab_1()



"""



# ---- imports


import inspect
import os
import subprocess
import sys
#	addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())
# import PyQt5.QtWidgets as qtw    #  qt widgets avoid so much import above
from functools import partial
from platform import python_version
from subprocess import PIPE, STDOUT, Popen, run

#from app_global import AppGlobal
from PyQt5 import QtGui
from PyQt5.QtCore import (QDate,
                          QModelIndex,
                          QSize,
                          QSortFilterProxyModel,
                          Qt,
                          QTimer)
# sql
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlField,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
from PyQt5.QtWidgets import (QAbstractItemView,
                             QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDataWidgetMapper,
                             QDateEdit,
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
                             QSpinBox,
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
import utils_for_tabs as uft
import wat_inspector

INDENT        = uft.INDENT
BEGIN_MARK_1  = uft.BEGIN_MARK_2
BEGIN_MARK_2  = uft.BEGIN_MARK_2

def print_func_header( what ):
        """
        what is says
        """
        #what    = "fix_me"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

#-----------------------------------------------
class QSqlRelationalTableModelTab_1( QWidget ):
    """
    for widgets joining two tables
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__( )

        self._build_model()
        self._build_gui()

        self.model.select()

    # ------------------------------
    def _build_gui( self,   ):
        """
        the usual
        """
        tab_page       = self

        layout        = QVBoxLayout( tab_page )
        self.layout   = layout

        layout.addWidget( self.view   )

        # --- buttons
        button_layout      = QHBoxLayout(   )
        layout.addLayout( button_layout )

        # ---- PB select_for\n_all
        widget            = QPushButton( "select_for\n_all" )
        connect_to        = self.select_all
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB select\n_some
        widget            = QPushButton( "select\n_some" )
        connect_to        = self.select_some
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB "get_data\n_from_model"
        widget              = QPushButton( "get_data\n_from_model" )
        connect_to          = self.get_data_from_model
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB i"insert\n_record"
        widget            = QPushButton("insert\n_record")
        connect_to        = self.add_record
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        # widget.clicked.connect(lambda: self.print_message(widget.text()))
        connect_to          = self.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget            = QPushButton("breakpoint\n")
        connect_to        = self.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

    # ------------------------------
    def _build_model( self,   ):
        """
        build model and views if used here

        sql behind this should be:
            SELECT
                people.id,
                people.name,
                people.age,
                people.family_relation,
                people_phones.phone_number
            FROM people
            LEFT JOIN people_phones ON people.id = people_phones.person_id

        """
        model           = QSqlRelationalTableModel(self)
        self.model      = model

        model.setTable( "people" )

        debug_var   = self.model.fieldIndex( "id" )   # field name to number

        model.setRelation(
            self.model.fieldIndex( "id" ),  # column name in first table, here people

            QSqlRelation("people_phones", "person_id", "phone_number")
            #             table to join to
            #                             column to join on
            #                                           # columns from people phones to fetch.and display display
            #QSqlRelation("people_phones", "person_id", "phone_number, zone")

        )

        column_index = model.fieldIndex( "age" )  # Get the column index for "name"
        print( f"{column_index = }")
        model.setSort( column_index , Qt.AscendingOrder)  # seems needs to be index no

        # Set headers -- need to match to model
        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "Name")
        model.setHeaderData(2, Qt.Horizontal, "Age")
        model.setHeaderData(3, Qt.Horizontal, "Family Relation")
        model.setHeaderData(4, Qt.Horizontal, "Phone Number")

        # self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        model.setEditStrategy( QSqlRelationalTableModel.OnManualSubmit )
        self.select_all()

        # ---- view
        view        = QTableView()
        self.view   = view
        view.setModel( model)

        # --- view options
        view.resizeColumnsToContents()
        view.setAlternatingRowColors(True)
        view.setSortingEnabled(True)    # is this click on header?

    # ------------------------
    def _people_view_clickedxxx(self, index,   ):
        """ """
        what    = "_people_view_clicked"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

        view    = self.people_view
        msg     = f"{INDENT}{view = } there is much to explore here, row, column, values"
        print( msg )

        msg     = f"{INDENT}{index} {index.row() = } {index.column() = } "
        print( msg )

        model      = self.people_model
        people_model = model
        no_rows    = model.rowCount()

        msg     = f"{INDENT}{model.rowCount() = }   "
        print( msg )

        # extract some data
        row_ix       = index.row()
        age_ix       = 2
        age          = model.data( model.index( row_ix, age_ix ) )

        msg     = f"{INDENT}extracted data {age = }   "
        print( msg )

        # extract some data
        row_ix       = index.row()
        key_ix       = 0 # may have been hidden
        key          = model.data( model.index( row_ix, key_ix ) )

        msg     = f"{INDENT}extracted data {key = }   "
        print( msg )

        # ---- sync up second model
        phone_model     = self.phone_model
        phone_model.setFilter( f"person_id = {key}" )
        phone_model.select()

    # -----------------------
    def add_record(self):
        """
        what it says
        """
        print_func_header( "add_record" )

        msg             = "data for id  123  name  John Doe"
        print( msg )

        model           = self.model

        new_record      = model.record()

        # --- set values
        new_record.setValue("id", 123)
        new_record.setValue("name", "John Doe")
        new_record.setValue("age", 30)
        new_record.setValue("family_relation", "Brother")

        if model.insertRecord(-1, new_record):
            if model.submitAll():
                print("Record inserted and changes committed to the database.")
            else:
                print("Error committing changes:", model.lastError().text())
        else:
            print("Error inserting record:", model.lastError().text())
        pass

    # ------------------------
    def xxxx(self):
        """ """
        print_func_header( "xxxx" )

        DB_OBJECT.query_data()

    # ------------------------
    def select_all(self):
        """
        select with a sort
        """
        print_func_header( "select_all" )

        model        = self.model
        column_index = model.fieldIndex( "age" )  # Get the column index for "name"
        print( f"for sorting {column_index = }")
        model.setSort( column_index , Qt.AscendingOrder)  # seems needs to be index no

        model.setFilter( "" )

        model.select()

    # ------------------------
    def select_some(self):
        """
        select base on some criteria, read the code for details
        """
        print_func_header( "select_some" )

        self.model.setFilter('age >  26 '   )
        self.model.select()

    # -----------------------
    def get_data_from_model(self):
        """
        What it says
            get data
            get rowcount
            can we get column count
            can we get column names
            note we also have a view
        """
        print_func_header( "select_some" )

        model           = self.model

        row_count       = model.rowCount()
        column_count    = model.columnCount()

        for ix_row in range( row_count ):
            for ix_col  in range( 3 ):   # should figure out a column count
                index     = model.index( ix_row,   ix_col   )
                data      = model.data( index )
                msg       = f"for {ix_row = } {ix_col = } {index = } {data = }"
                print( msg )

    # ------------------------
    def do_selections(self):
        """
        not sure ... is dead?
        """
        print_func_header( "do_selections" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        # make some locals for inspection
        my_self                = self
        parent_window           = self.parent( ).parent( ).parent().parent()
        a_db                    = parent_window.sample_db
        local_self_model        = self.model
        local_self_view         = self.view
        wat_inspector.go(
             msg            = "inspect for QSqlRelationalTableModelTab",
             #inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        the usual
        """
        print_func_header( "breakpoint" )

        breakpoint()


# ---- eof
