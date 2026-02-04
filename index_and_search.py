#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build the database to search for tabs
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    # import qt_search
    # qt_search.main()
# --------------------

import logging
import inspect
import os
import sqlite3 as lite
import subprocess
import sys
from functools import partial
from pathlib import Path
from platform import python_version
from subprocess import PIPE, STDOUT, Popen, run

import key_word_indexer
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

import global_vars
import parameters
import utils_for_tabs as uft
import wat_inspector

# ---- ---- local imports

print_func_header  = uft.print_func_header

# -----------------------------
def delete_db_file( file_name ):
    """
    will delete any file, but intended for db file
    """
    exists    = str( os.path.isfile( file_name ) )
    msg       =  f"{file_name} exists {exists}"
    logging.error( msg )

    if exists:
        try:
            os.remove( file_name )   # error if file not found
            msg    = ( f"delete_db_file removed {file_name} "  )
            logging.debug( msg )

        except OSError as error:
            msg    = f"{error = }"
            logging.debug( msg )

            msg        = ( f"delete_db_file os.remove threw error on file {file_name}")
            logging.debug( msg )

    else:
        msg         = ( f"delete_db_file file already gone  {file_name}   ")
        logging.debug( msg )

# -------------------------------------
class TabDBBuilder():
    """
    this will create
    """
    #-------------------
    def __init__( self ):
        """
        The usual
        global_vars.set_tab_db_builder( self  )
        global_vars.TAB_DB_BUILDER.widget_list

        """
        self.db    = None
        self.reset()

        global_vars.set_tab_db( self.db  )
        global_vars.set_tab_db_builder( self  )

    #------------
    def reset( self, ):
        """
        Reset and rebuild the db
        """
        self.widget_set   = set( )
        self.create_connection()
        self.create_populate_tables()
        self.widget_set = self.widget_set - { "" }

        widget_list   = list( self.widget_set )
        widget_list.sort()
        self.widget_list   = widget_list   # intervace
        #rint( f"reset {widget_list = }")

    #------------
    def create_connection( self, ):
        """
        Create a SQLite database connection.
        """
        if self.db is not None:
            self.db.close()
            self.db    = None  # or delete?

        db_file_name             = parameters.PARAMETERS.tab_db_file_name

        if db_file_name !=  ':memory:':  # delete for a fresh start
            delete_db_file( db_file_name )

        db              = QSqlDatabase.addDatabase( parameters.PARAMETERS.tab_db_type, "tab_db" )
        db.setDatabaseName( db_file_name )
        self.db         = QSqlDatabase.database( "tab_db" )  # may need to do neare to use lets see

        if not db.open():
            msg       = ("IndexDB Error: Unable to establish a database connection.")
            logging.error( msg )
            return False

        return True

    # ---------------------------
    def create_populate_tables( self, ):
        """
        Create  tables.and populate with a bit of data
        """
        self.create_tab_table()
        self.create_tab_key_word_table()

        file_list     = self.find_doc_files()
        self.add_docs_to_db( file_list  )

        self.populate_key_word_table()

        self.query_print_tab()

    # ---------------------------
    def create_tab_table( self, ):
        """
        Create table
        ."""
        query   = QSqlQuery( self.db )

        sql     = """
            CREATE TABLE tabs (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_file_name   TEXT,
                name            TEXT,
                tab_title       TEXT,
                module          TEXT,
                class           TEXT,
                widgets         TEXT,
                key_words       TEXT,
                description     TEXT,
                web_link        TEXT
            )
        """

        if not query.exec_(sql):
            msg      = ("Error executing query: {query.lastError().text() }" )
            logging.error( msg )
        else:
            pass
            #rint("Query executed successfully.")

    # ---------------------------
    def create_tab_key_word_table( self, ):
        """
        Create table
        ."""
        query   = QSqlQuery( self.db )

        sql     = """
            CREATE TABLE tabs_key_word (
                id              INTEGER,
                key_word        TEXT
            )
        """

        if not query.exec_(sql):

            msg     = ("create_tab_key_words_table Error executing query: {query.lastError().text()}" )
            logging.error( msg )
        else:
            pass
            #rint("create_tab_key_words_table Query executed successfully.")

    #------------
    def find_doc_files( self, ):
        """
        find the object files and make a list
           may later need to use .name or .stem
        """
        directory_list      = parameters.PARAMETERS.dir_for_tabs
        directory_list      = list( set( directory_list ))  #de dup
        file_list           = []
        #i_directory    = Path( "./" )
        for i_directory in directory_list:
            i_directory     = Path( i_directory )
            i_file_list     = [file  for file in i_directory.glob('tab*.py')  ]
                    # not .stem or .name whic may be needed later
            file_list       = file_list + i_file_list

        msg         = "index_and_search.py find_doc_files this is the file list"
        logging.debug( msg )
        for ix, i_file in enumerate( file_list ):
            msg    = f" {ix }ix, {i_file} "
            logging.debug( msg )

        return file_list

    #------------
    def add_docs_to_db( self, doc_file_list  ):
        """
        add data from all the docs in doc_file_list to
        the database
        """
        for ix, i_doc in enumerate( doc_file_list ):
            doc_data  = self.get_doc_data( i_doc )
            # if str( i_doc ) == "tab_box_layout.py":

            module              = doc_data[ "module" ].strip()  # !! redundatan hack fix
            how_complete        = doc_data[ "how_complete" ].strip()
            how_complete        = how_complete.replace( "#", " ")

            print( f"add_docs_to_db tab file: {how_complete = }" )
            # if how_complete != "":
            #     breakpoint()

            if how_complete    == "":
                how_complete   = "1 #default "
            splits             = how_complete.split( " " )
            how_complete       = int( splits[0] )

            if how_complete < parameters.PARAMETERS.min_complete:
                msg    = ( f"TabDBBuilder dropping {module = } because of "
                        "-- not complete enough {how_complete = }  )" )
                logging.debug( msg )
                continue

            module       = doc_data[ "module" ].strip()
            class_name   = doc_data[ "class_name" ].strip()
            if not bool( class_name ) or not bool( module ):
                msg    = ( f"TabDBBuilder dropping {module = } because of "
                            "-- not bool( {class_name = } ) or not bool( module )" )
                logging.debug( msg )
                continue

            self.doc_data_to_db( doc_data )

    #------------
    def doc_data_to_db( self, doc_data ):
        """
        add a doc data to the db
        and our set ... read it
        """
        widget_list     = doc_data[ "widgets"].split( " " )

        self.widget_set = self.widget_set | set( widget_list )
        #rint( f"{self.widget_set = }")

        query           = QSqlQuery( self.db )

        # think we can just unpack the dict, did a chatbot tell me to do this
        table_data = [
            ( str( doc_data[ "doc_file_name"] ),
              "name??",
              doc_data[ "tab_title"],
              doc_data[ "module"],
              doc_data[ "class_name"],
              doc_data[ "widgets"],
              doc_data[ "key_words"],
              doc_data[ "description"],
              doc_data[ "web_link"],
            ),
        ]

        for doc_file_name, name,  tab_title, module, class_name, widgets, key_words, description, web_link  in table_data:
            # this only one way to bind
            sql     = """INSERT INTO tabs (
                doc_file_name,
                name,
                tab_title,
                module ,
                class,
                widgets,
                key_words,
                description,
                web_link
                )
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )
            """
            query.prepare( sql )
            query.addBindValue( doc_file_name )
            query.addBindValue( name )
            query.addBindValue( tab_title )
            query.addBindValue( module )
            query.addBindValue( class_name )
            query.addBindValue( widgets )
            query.addBindValue( key_words )
            query.addBindValue( description )
            query.addBindValue( web_link )

            result   = query.exec_()
            if not result:
                msg      = ( f"doc_data_to_db Error executing query: "
                              f" {query.lastError().text()} " )
                logging.error( msg )
                1/0
            else:
                pass
                #rint("doc_data_to_db Query executed successfully.")

    #------------
    def get_doc_data( self, file_name ):
        """
        beware file_name really file_name_path
        read the doc data into a dict strings?
        file_name think string or path
        change to with

        !! better code would probably be a generator -- chat to fix??
        !! do the stip here
        """
        #rint( f"get_doc_data {file_name = }")
        #rint( "could make a loop to do this maybe a comp !!")

        doc_data_items       = [ "doc_file_name",
                                  "class_name",
                                  "tab_title",
                                  "key_words",
                                  "widgets",
                                  "description",
                                  "how_complete",
                                  "web_link"] # omit doc_file_name -- for sure

        doc_data    = {}
        doc_data[ "module"  ]    = str( file_name )[ :-3 ]
        for i_doc_item in doc_data_items:
            doc_data[ i_doc_item ] = ""

        doc_data[ "doc_file_name" ] = file_name
        doc_data[ "description" ]   = "Description comming soon"
        doc_data[ "web_link" ]      = "https://github.com/russ-hensel/qt5_by_example/wiki"

        a_file  = open( file_name, 'r', encoding = "utf8", errors = 'ignore' )

        for ix, i_line in enumerate( a_file ):

            # looks like a loop woruld do all this
            i_line    = i_line.rstrip('\n')   # this i think is the best way --- think is arg to have python strip
            i_line    = i_line.strip()
            #rint( f"reading line no {ix} =  {i_line }")


            if i_line.startswith( "KEY_WORDS:"):
                i_line    = i_line[ 10: ].strip()
                doc_data[ "key_words" ] = doc_data[ "key_words" ] + " " + i_line

            # if i_line.startswith( "MODULE:"):
            #         i_line    = i_line[ len("MODULE:" ): ].strip()
            #         doc_data[ "module" ] = doc_data[ "module" ] + " " + i_line

            key         = "class_name"
            if i_line.startswith(  f"{key.upper()}:"):
                    i_line    = i_line[ len(key) + 1 : ].strip()
                    doc_data[ key ] = doc_data[ key ] + " " + i_line

            key         = "widgets"
            if i_line.startswith(  f"{key.upper()}:"):
                    i_line    = i_line[ len(key) + 1 : ].strip()
                    doc_data[ key ] = doc_data[ key ] + " " + i_line

            key         = "tab_title"
            if i_line.startswith(  f"{key.upper()}:"):
                    i_line    = i_line[ len(key) + 1 : ].strip()
                    doc_data[ key ] = doc_data[ key ] + " " + i_line

            key         = "description"
            if i_line.startswith(  f"{key.upper()}:"):
                    i_line    = i_line[ len(key) + 1 : ].strip()
                    #doc_data[ key ] = doc_data[ key ] + " " + i_line
                    doc_data[ key ] = i_line  # needs to be on one line

            key         = "how_complete"
            if i_line.startswith(  f"{key.upper()}:"):
                    i_line    = i_line[ len(key) + 1 : ].strip()
                    #doc_data[ key ] = doc_data[ key ] + " " + i_line
                    doc_data[ key ] = i_line  # needs to be on one line

            key         = "wiki_link"
            if i_line.startswith(  f"{key.upper()}:"):
                    i_line    = i_line[ len(key) + 1 : ].strip()
                    #doc_data[ key ] = doc_data[ key ] + " " + i_line
                    doc_data[ key ] = i_line  # needs to be on one line

            if ix > 35:   # line limit
                #rint( "break on ix .....")
                break

        a_file.close()

        #rint( f"{doc_data = }")

        return doc_data

    #------------
    def populate_key_word_table ( self, ):
        """
        Populate
        """
        print_func_header( "populate_key_word_table" )

        a_kwi     = key_word_indexer.KeyWordIndexer( db             = self.db,
                                                    table_name      = "tabs",
                                                    kw_table_name   = "tabs_key_word"   )
        a_kwi.loop_thru()

    #------------
    def query_print_tab( self, ):
        """
        Print out the table
        """
        print_func_header( "query_print_tab" )

        query           = QSqlQuery( self.db )

        #rint("tab table")

        sql   = "SELECT id, module, class, widgets, key_words FROM tabs"

        if not query.exec_( sql ):  # Check if execution failed
            msg        = ("query_print_tab Error executing query:  {query.lastError().text()}" )
            logging.error( msg )

        while query.next():
            a_id                = query.value(0)
            module              = query.value(1)
            a_class             = query.value(2)
            #rint(f"ID: {a_id},  {module = },   {a_class = }")

# ---- useless object but requred delete it later
class IndexSearch(   ):
    def __init__(self):
        """
        obj.index_db.

        """
        pass
        self.build_stuff()

    def build_stuff( self ):
        self.index_db     = TabDBBuilder( )
        return self.index_db.db


# ---- eof