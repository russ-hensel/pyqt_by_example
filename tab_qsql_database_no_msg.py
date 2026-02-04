#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

tab_qsql_database.

self.help_file_name     =  "qsql_database_tab.txt"

KEY_WORDS:      sql database insert define schema query create db select cursor bind error last join table zzz
CLASS_NAME:     QSqlDatabaseTab
WIDGETS:        QSqlDatabase QSqlQuery
STATUS:         works
TAB_TITLE:      QSqlDatabase QSqlQuery


"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main

# --------------------


import inspect
import os
import sqlite3 as lite
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
from PyQt5.QtGui import QColor, QIcon, QPalette, QTextCursor, QTextDocument
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
                             QSplitter,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextBrowser,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
import qt_table_model
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import global_vars
# ---- imports neq qt

# ---- end imports



INDENT          = uft.INDENT
BEGIN_MARK_1    = uft.BEGIN_MARK_1
BEGIN_MARK_2    = uft.BEGIN_MARK_2


print_func_header =  uft.print_func_header


# -----------------------------
def delete_db_file( file_name ):
    """
    will delete any file, but intended for db file
    """
    exists    = str( os.path.isfile( file_name ) )
    print( f"{file_name} exists {exists}" )

    if exists:
        try:
            os.remove( file_name )   # error if file not found
            print(f"removed {file_name} "  )

        except OSError as error:
            print( error )
            print( f"os.remove threw error on file {file_name}")

    else:
        print( f"file already gone  {file_name}                ")


# -------------------------------------
class SampleDB():
    """
    this will create an instance of SampleDB and set up two module Globals
    """
    #-------------------
    def __init__( self ):
        """
        The usual
        """
        self.db             = None
        # self.sample_db      = None  # same as above
        self.reset()
        #global_vars.SAMPLE_DB_OBJ  = self
        global_vars.set_sample_db_obj( self )

    #------------
    def reset( self, ):
        """
        Reset and rebuild the db
        """
        self.create_connection()
        self.create_populate_tables()

    #------------
    def create_connection( self, ):
        """
        Create a SQLite database connection.
        """
        if self.db is not None:
            self.db.close()
            self.db    = None  # or delete?

        db_file_name    = parameters.PARAMETERS.db_file_name
        if    db_file_name !=  ':memory:':
            # delete for a fresh start
            delete_db_file( db_file_name )

        # !! may need parameters particurlarry for the db type
        db              = QSqlDatabase.addDatabase( parameters.PARAMETERS.db_type, db_file_name )
        db.setDatabaseName( db_file_name )   # is this really the file name

        # next kills it ?  --- now seems ok may still be issues
        #self.db         = QSqlDatabase.database( "qt_example_db" )
        self.db         = db
        print( "!! globalize in some way ")
        #self.db         = db

        global_vars.set_ex_db( db )

        if not db.open():
            print("SampleDB Error: Unable to establish a database connection.")
            return False
        return True

    # ---------------------------
    def create_populate_tables( self, ):
        """
        Create  tables.and populate with a bit of data
        """
        print_func_header( "create_populate_tables" )

        self.create_persons_table()
        self.populate_persons_table()

        self.create_persons_key_words_table()

        self.create_persons_phones_table()
        self.populate_persons_phones_table()

        self.create_book_club_table()
        self.populate_book_club_table()

        self.create_employee_table()
        self.populate_employee_table()

    # ---------------------------
    def create_persons_table( self, ):
        """
        Create people and people_phones tables
        ."""
        print_func_header( "create_persons_table" )

        query   = QSqlQuery( self.db )

        sql     = """
            CREATE TABLE persons (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT,
                age             INTEGER,
                family_relation TEXT,
                add_kw          TEXT
            )
        """

        if not query.exec_(sql):  # Check if execution failed
            print("Error executing query:", query.lastError().text())
        else:
            pass
            #rint("Query executed successfully.")

    # ---------------------------
    def create_persons_key_words_table( self, ):
        """
        query.prepare( f"INSERT INTO {self.table_name}"
                        "  (id, key_word ) VALUES ( :id, :key_word )")
        ."""
        print_func_header( "create_persons_key_words_table" )

        query   = QSqlQuery( self.db )

        sql     = """
            CREATE TABLE persons_key_words (
                id              INTEGER,
                key_word        TEXT
            )
        """
        self.query_exec_error_check( query, sql )


        # if not query.exec_(sql):  # Check if execution failed
        #     print("Error executing query:", query.lastError().text())
        # else:
        #     pass
        #     #rint("Query executed successfully.")



    #------------
    def populate_persons_table( self, ):
        """
        Populate the people table with sample data.
        """
        print_func_header( "populate_persons_table" )

        if False:
            # a bit of straight sql lite -- this does not work for in memory?
            sql_con    = lite.connect( parameters.PARAMETERS.db_file_name )
            #conn       = sqlite3.connect("example.db")
            cursor     = sql_con.cursor()
            # Insert a row with a specific starting ID
            cursor.execute("INSERT INTO persons (id, name) VALUES (?, ?)", (1000, "Initial Entry"))
            # cursor.commit()
            sql_con.commit()

            #rint( "persons table initialized to starting id of 1000")

        if True:

            query       = QSqlQuery( self.db )
            sql  =   """INSERT INTO persons (
                    id,
                    name,
                    age,
                    family_relation )
                VALUES ( 1000, "initial", 0, 0 )
            """
            query.prepare( sql )
            # query.exec_()

            self.query_exec_error_check( query )

        query       = QSqlQuery( self.db )

        # you can comment out some data if you wish
        table_data = [
            ("Alice",   25,   "Aunt"      ),
            ("Bob",     30,   "Father"    ),
            ("Charlie", 35,   "Daughter"  ),
            ("David",   40,   "Daughter2" ),
            ("James",   28,   "Aunt"      ),
            ("Jim",     28,   "Son"       ),
            # ("Judy",    28,   "Sun"       ),
            # ("Jo",      29,   "God"       ),
        ]

        sql  =   """INSERT INTO persons (
                name,
                age,
                family_relation )
            VALUES ( ?,?, ? )
        """

        for name, age, family_relation in table_data:
            # this only one way to bind
            query.prepare( sql )
            query.addBindValue(name)
            query.addBindValue(age)
            query.addBindValue(family_relation)
            query.exec_()

    # ---------------------------
    def create_employee_table( self, ):
        """
        Create  table.
        """
        query       = QSqlQuery( self.db )
        # Create a sample table and insert data

        sql   = """
            CREATE TABLE employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                dob TEXT,
                occupation TEXT
            );
        """

        query.exec_( sql )

    #------------
    def populate_employee_table( self, ):
        """
        Populate the table.
        """
        query       = QSqlQuery( self.db )

        sql    = ("""
            INSERT INTO employee (name, dob, occupation) VALUES
            ('Alice', '1990-04-20', 'Engineer'),
            ('Bob', '1985-11-30', 'Designer'),
            ('Charlie', '1992-06-15', 'Developer');
        """)

        query.exec_( sql )

    # ---------------------------
    def create_persons_phones_table( self, ):
        """
        Create persons_phones table.
        """
        print_func_header( "create_persons_phones_table" )

        query = QSqlQuery( self.db )

        sql   = """
            CREATE TABLE persons_phones (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id       INTEGER,
                phone_number    TEXT,
                zone            TEXT,
                FOREIGN KEY(person_id) REFERENCES persons(id) ON DELETE CASCADE
            )
        """
        query.exec( sql )

    #------------
    def populate_persons_phones_table( self, ):
        """
        Populate the persons_phones table.
        """
        print_func_header( "populate_persons_phones_table" )

        query = QSqlQuery( self.db )

        table_data = [
            (1001, "555-1234", "A"), (1001, "555-5678", "B"), (1001, "555-8765", "C"),
            (1002, "555-4321", "A"), (1002, "555-8765", "B"), (1002, "555-3456", "C"),
            # (1003, "555-9876", "A"), (1003, "555-1111", "B"), (1003, "555-2222", "C"),
            # (1004, "555-3333", "A"), (1004, "555-4444", "B"), (1004, "555-5555", "C"),
            # (1005, "555-6666", "A"), (1005, "555-7777", "B"), (1005, "555-8888", "C"),
            # (1005, "555-9999", "A"), (1005, "555-0000", "B"), (1005, "555-1235", "C"),
            # (2, "555-2345", "A"),    (1, "555-3456", "B"),
        ]

        sql   = """INSERT INTO persons_phones (
                      person_id,
                      phone_number,
                      zone )
                     VALUES ( ?, ?, ? )
        """

        # this  is the positional style with bind values
        for person_id, phone_number, zone in table_data:
            query.prepare( sql )
            # bind value for each ?
            query.addBindValue( person_id )
            query.addBindValue( phone_number)
            query.addBindValue( zone )
            query.exec_()

    #------------
    def create_book_club_table( self, ):
        """
        Book Clubs that persons can belong to
        a many to many relationship based on persons and book_club
        """
        what    = "create_book_club_table"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

        query   = QSqlQuery( self.db )

        sql     = """
            CREATE TABLE book_club (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                frequency       TEXT
            ) """

        query.exec_( sql )

    #------------
    def populate_book_club_table( self, ):
        """
        Populate the book_club table
        """
        what    = "populate_book_club_table"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

        query = QSqlQuery( self.db )

        table_data = [
            ("ScinectFiction",      "weekly"    ),
            ("Romance",             "weekly"    ),
            ("Westerns",            "monthly"   ),
            ("Biography",           "daily"     ),
        ]

        for name, frequency in table_data:
            # this only one way to bind
            sql     = """INSERT INTO book_club (
                name,
                frequency  )
                VALUES (?, ? )
            """

            query.prepare( sql )
            query.addBindValue( name )
            query.addBindValue( frequency )

            query.exec_()

    #------------
    def create_persons_book_club_table( self, ):
        """
        Create  table -- what it says
        """
        print_func_header( "create_persons_book_club_table" )

        query = QSqlQuery( self.db )

        sql    = """
            CREATE TABLE persons_book_club (        print_func_header( "query_print_people" )
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                people_id       INTEGER,
                book_club_id    INTEGER
              ) """

        query.exec_( sql )

    #------------
    def populate_persons_book_club_data( self, ):
        """
        what it says
        """
        query = QSqlQuery( self.db )

        table_data = [
            ("Alice",   25,   "Aunt"      ),
            ("Bob",     30,   "Father"    ),
            ("Charlie", 35,   "Daughter"  ),
            ("David",   40,   "Daughter2" ),
            ("James",   28,   "Aunt"      ),
            ("Jim",     28,   "Son"       ),
            ("Judy",    28,   "Sun"       ),
            ("Jo",      29,   "God"       ),
        ]

        sql     = """INSERT INTO persons (
                  name, age, family_relation) VALUES (?,?, ? )
        """

        for name, age, family_relation in table_data:
            # this only one way to bind
            query.prepare()
            query.addBindValue(name)
            query.addBindValue(age)
            query.addBindValue(family_relation)
            query.exec_()

    #------------
    def query_print_persons( self, ):
        """
        Print out the table
        """
        print_func_header( "query_print_persons" )

        query           = QSqlQuery( self.db )

        print("People:")

        # Execute the query
        if not query.exec_("SELECT id, name, age, family_relation FROM persons"):  # Check if execution failed
            print("Error executing query:", query.lastError().text())
        else:
            pass
            #rint("Query executed successfully.")

        while query.next():
            person_id           = query.value(0)
            name                = query.value(1)
            age                 = query.value(2)
            family_relation     = query.value(3)
            print(f"ID: {person_id}, Name: {name}, Age: {age} {family_relation = }")

    #------------
    def query_persons_key_words( self, ):
        """
        Print out the table
        """
        print_func_header( "query_persons_key_words" )

        sql     = """
            SELECT
                id,
                key_word

                FROM persons_key_words
            """

        query           = QSqlQuery( self.db )

        print("persons_key_words table:")

        self.query_exec_error_check( query, sql )

        while query.next():
            a_id        = query.value(0)
            name        = query.value(1)
            print(f"ID: {a_id = }  { name = } ")

    #------------
    def query_book_club( self, ):
        """
        Print out the table
        """
        print_func_header( "query_book_club" )

        sql     = """
            SELECT
                id,
                name,
                frequency
                FROM book_club
            """

        query           = QSqlQuery( self.db )

        print("book_club table:")

        query.exec_( sql )


        while query.next():
            a_id        = query.value(0)
            name        = query.value(1)
            frequency   = query.value(2)

            print(f"ID: {a_id = }  { name = }  {frequency = }  ")

    #------------
    def query_print_phone( self, ):
        """
        Print out the table
        """
        what    = "query_print_phone"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

        query           = QSqlQuery( self.db )

        print("persons_phones_data table:")
        sql  = ("SELECT id, person_id, phone_number, zone FROM persons_phones")

        self.query_exec_error_check( query, sql )


        while query.next():
            a_id             = query.value(0)
            person_id        = query.value(1)
            phone_number     = query.value(2)
            zone             = query.value(3)
            print(f"ID: {a_id = }  { person_id = }  {phone_number = }  {zone = }")

    #------------
    def query_print_person_phone( self, ):
        """
        Print a join of people and people_phones
        """
        what    = "query_print_people_phone"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

        query           = QSqlQuery( self.db )

        print("\nPeople and their phone numbers: join of people and people_phones")

        sql = ("""
            SELECT persons.name, persons_phones.phone_number
            FROM persons
            JOIN persons_phones ON persons.id = persons_phones.person_id
            ORDER BY persons.name ASC
        """)

        self.query_exec_error_check( query, sql )

        while query.next():
            name            = query.value(0)
            phone_number    = query.value(1)
            print(f"Name: {name}, Phone: {phone_number}")

    def query_exec_error_check( self, a_query, sql = None ):
        """
        !! think about outher args
        make this the standard error checking
        or send result an query as arguments
        """
        if sql is None:
            result  = a_query.exec_( )
        else:
            result  = a_query.exec_( sql )

        if not result:
            print( "query_exec_error_check Error:", a_query.lastError().text())
            print( f"{sql = } ", )
        else:
            pass
            #rint("Query executed successfully.")

# -------------------------------------
class KeyGen():
    """
    This is a key generator, may use in future or not
    it is quite stupid but good enough for here
    """
    #-------------------
    def __init__( self ):
        """
        what it says
        """
        self.keys     = list( range( 2000, 5000 ))
        self.ix_keys  = -1

    #-------------------
    def get_next_key( self, ):
        """
        what it says
        """
        self.ix_keys  += 1

        return self.keys[ self.ix_keys ]

#-----------------------------------------------
class QSqlDatabaseTab( QWidget ):
    """
    for the basic database object
    SampleDB()     QSqlDatabase    query
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__( )
        self.help_file_name     =  "qsql_database_tab.txt"
        self.sample_db   = SampleDB()
        self.build_tab()


    #-----------------------------------------------
    def build_tab( self, ):
        """
        what it says
        """
        tab_page      = self
        layout        = QVBoxLayout( tab_page )

        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout )

        # ---- PB rebuild_db
        widget              = QPushButton( "rebuild_db\n ")
        self.button_ex_1    = widget
        widget.clicked.connect( self.rebuild_db )

        button_layout.addWidget( widget )

        # ---- PB print_db
        widget              = QPushButton("print_db\n ")
        connect_to          = self.print_db
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB "insert_more_\ndata"
        widget              = QPushButton("insert_more_\ndata")
        connect_to          = self.insert_more_data
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB "delete_\ndata"
        widget              = QPushButton("delete_\ndata")
        connect_to          = self.delete_data
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB "update_\ndata"
        widget              = QPushButton("update_\ndata")
        widget.clicked.connect( self.update_data )
        button_layout.addWidget( widget )

        # ---- PB "query_book_\nclub "
        widget              = QPushButton("query_book_\nclub ")
        connect_to          = self.sample_db.query_book_club # see SampleDB
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to        = self.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = self.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

    # ------------------------
    def print_db(self):
        """ """
        print_func_header( "print_db" )

        self.sample_db.query_print_persons()
        self.sample_db.query_persons_key_words()
        self.sample_db.query_print_phone()

        self.sample_db.query_book_club()
        self.sample_db.query_print_person_phone()

    # ------------------------
    def rebuild_db(self):
        """ """
        print_func_header( "rebuild_db" )

        self.sample_db.reset()

    #-----------------------------------------------
    def insert_more_data( self ):
        """
        what it says, data with stars
        """
        print_func_header( "insert_more_data" )

        db      = self.sample_db.db

        query   = QSqlQuery( db )  # beware using this with no arg default

        table_data = [
            ("**History",      "weekly"    ),
            ("**Adventure",    "weekly"    ),
            ("**Easterns",      "monthly"  ),
            ("**Physics",      "daily"     ),
        ]

        for name, frequency in table_data:
            # this only one way to bind
            print( f"insert {name} {frequency}")

            sql     = """INSERT INTO book_club (
                name,
                frequency  )
                VALUES (?, ? )
            """

            query.prepare( sql )

            if not query.prepare(sql):
                print(f"Prepare failed: {query.lastError().text()}")
                continue

            query.addBindValue( name )
            query.addBindValue( frequency )

            if not query.exec_():
                print(f"Execution failed: {query.lastError().text()}")
            else:
                pass
                #print("Insert successful.")

    #-----------------------------------------------
    def delete_data( self ):
        """
        I have a table:
            CREATE TABLE book_club (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                frequency       TEXT

         could you give me the sql to delete all records where name begins with "*"
         give the code for running with QSqlQuery using a bind variable for the where clause
        """
        print_func_header( "delete_data" )

        db      = self.sample_db.db

        query   = QSqlQuery(db)

        # SQL statement with a bind variable
        sql     = "DELETE FROM book_club WHERE name LIKE ?"

        if not query.prepare(sql):
            print(f"Prepare failed: {query.lastError().text()}")

        else:
            query.addBindValue("*%")

            if not query.exec_():
                print(f"Execution failed: {query.lastError().text()}")
            else:
                print("Records deleted successfully.")

    #-----------------------------------------------
    def update_data( self ):
        """
        what it says
        """
        print_func_header( "update_data" )

        db      = self.sample_db.db


        print( "QSqlQuery can be used without specifying the db then it uses a default use with care " )
        query   = QSqlQuery( db )

        sql      = """
            UPDATE book_club
            SET name = :new_name
            WHERE name LIKE :pattern;
            """
        if not query.prepare(sql):
            print(f"Prepare failed: {query.lastError().text()}")

        else:
            query.bindValue(":new_name", "stars")
            query.bindValue(":pattern", "*%")

            if not query.exec_():
                print(f"Execution failed: {query.lastError().text()}")

            else:
                rows_affected = query.numRowsAffected()
                print( f"Records udated successfully. {rows_affected = } ")

    # ------------------------
    def inspect(self):
        """ """
        print_func_header( "inspect" )
        # make some locals for inspection
        the_example_db_obj    = self.sample_db
        # parent_window = self.parent( ).parent( ).parent().parent()
        # a_db          = parent_window.sample_db
        # model         = self.people_model
        # view          = self.people_view
        wat_inspector.go(
             msg            = "see the_global_db",
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """ """
        print_func_header( "breakpoint" )

        breakpoint()

# ---- eof
