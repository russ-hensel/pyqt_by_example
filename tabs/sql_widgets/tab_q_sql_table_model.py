#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ---- tof

KEY_WORDS:      sql query of a single table crud select insert update delete rh
CLASS_NAME:     QSqlTableModelTab
WIDGETS:        QSqlTableModel QTableView
STATUS:         runs_correctly_?_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      QSqlTableModel Reference
DESCRIPTION:    A reference for the QSqlTableModel and its View QTableView


"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# -------------------


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

from qtpy.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from qtpy.QtWidgets import (  QDialog, )
from qtpy.QtWidgets import (  QSpinBox, )
from qtpy.QtWidgets import ( QHBoxLayout, QFormLayout, )
from qtpy.QtWidgets import ( QSpinBox, QComboBox, QDialogButtonBox, QMessageBox, )
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
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
import info_about
import utils_for_tabs as uft
import wat_inspector
import global_vars
import tab_base
# ---- end imports


INDENT              = uft.INDENT
# print_func_header   =  uft.print_func_header

#-----------------------------------------------
class QSqlTableModelTab( tab_base.TabBase   ):
    """
    QSqlTableModel
        and  QTableView
    """
    def __init__(self, ):
        """
        """
        super().__init__( )
        self.module_file       = __file__      # save for help file usage
        self._build_model()
        self._build_gui()

        self.ix_id_list         = 0
        self.id_list            = [ 1000, 1001, 1002, 1003, 1004, 3 ]

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self.select_all()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        layout.addWidget( self.persons_view   )

        layout.addWidget( self.phone_view    )

        # --- buttons
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- PB select_all
        widget              = QPushButton("select_all\n")
        connect_to          = self.select_all
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        label       = "clear\n"
        widget      = QPushButton( label )

        widget.clicked.connect( self.clear )
        row_layout.addWidget( widget )

        label       = "<<prior\n"
        widget      = QPushButton( label )
        connect_to  = partial( self.prior_next, -1 )
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )


        label       = "next>>\n"
        widget      = QPushButton( label )
        connect_to  = partial( self.prior_next, 1 )
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- get_selected_rows
        widget              = QPushButton("get_selected_rows\n")
        widget.clicked.connect( self.get_selected_rows )
        row_layout.addWidget( widget )

        # ---- get_data_values
        widget              = QPushButton("get_data_values\n")
        widget.clicked.connect( self.get_data_values )
        row_layout.addWidget( widget )

        # ---- add_new_person
        widget              = QPushButton("add_new_person\n")
        widget.clicked.connect( self.add_new_person )
        row_layout.addWidget( widget )

        # ---- edit_selected_person
        widget              = QPushButton("edit_selected_person\n")
        widget.clicked.connect( self.edit_selected_person )
        row_layout.addWidget( widget )

        # ---- edit_selected_person
        widget              = QPushButton("delete_selected_person\n")
        widget.clicked.connect( self.delete_selected_person )
        row_layout.addWidget( widget )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )



        # # ---- mutate
        # widget = QPushButton("mutate\n")
        # self.button_ex_1         = widget
        # widget.clicked.connect( lambda: self.mutate( ) )
        # row_layout.addWidget( widget )

        # # ---- PB inspect
        # widget              = QPushButton("inspect\n")
        # connect_to          = self.inspect
        # widget.clicked.connect( connect_to )
        # row_layout.addWidget( widget )

        # # ---- PB breakpoint
        # widget              = QPushButton("breakpoint\n ")
        # connect_to          = self.breakpoint
        # widget.clicked.connect( connect_to )
        # row_layout.addWidget( widget )

    # ------------------------------
    def _build_model( self,   ):
        """
        build model and views if used here

        """
        # ---- persons
        model                  = QSqlTableModel( self, global_vars.EX_DB   )
        self.persons_model      = model
        model.setTable( 'persons' )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
            #  OnFieldChange , OnRowChange , and OnManualSubmit .
        # header title
        model.setHeaderData(2, Qt.Horizontal, "Age*" ) # QtHorizontal
        #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

        view                    = QTableView( )
        self.persons_view       = view
        view.setModel( model  )
        view.hideColumn( 0 )       # hide is hear but header on model
        view.setSelectionBehavior( QTableView.SelectRows )
        view.clicked.connect( self._persons_view_clicked  )
        view.setSortingEnabled( True )

        # ---- persons_phones
        model                  = QSqlTableModel( self, global_vars.EX_DB  )
        self.phone_model       = model
        model.setTable( 'persons_phones' )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
            #  OnFieldChange , OnRowChange , and OnManualSubmit .
        # model->select();
        #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

        view                    = QTableView( )
        self.phone_view         = view
        view.setModel( model  )
        view.hideColumn( 0 )       # hide is hear but header on model
        view.setSortingEnabled(True)
        #view.setSelectionBehavior( QTableView.SelectRows )
        #view.clicked.connect( self._view_clicked  )

            #  OnFieldChange , OnRowChange , and OnManualSubmit .
        # model->select();
       #  model.setHeaderData(2, Qt.Horizontal, "Age*" ) # QtHorizontal in c
        #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

    # ------------------------
    def get_selected_rows(self, index,   ):
        """ """
        self.append_function_msg( "get_selected_rows" )

        msg = ( "looking at the persons view ")
        self.append_msg( msg,)
        view            = self.persons_view
        # Assuming `view` is your QTableView
        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()  # Get the selected rows

            for index in selected_indexes:
                row     = index.row()  # Get the row number
                msg     = ( f"Selected row: {row = }" )
                self.append_msg( msg, )
    # ------------------------
    def get_data_values(self,    ):
        """ """
        self.append_function_msg( "get_data_values" )

        row             = 1
        column          = 1
        msg    = ( f"for now not selectd by by {row = } {column = }" )
        self.append_msg( msg, )

        model           = self.persons_model


        # Retrieve the QModelIndex for the specified cell
        index   = model.index(row, column)

        # Get the data from the model at the specified index
        value   = model.data(index)
        msg     =  ( f"Value at row {row },  {column = }: {value = }" )
        self.append_msg( msg, )
        # using column name
        column_name = "name"

        # Get the column index for the column name
        column = model.fieldIndex( column_name )

        if column == -1:
            msg = ( f"Column '{column_name}' not found in the model." )
            self.append_msg( msg, )
        else:
            # Retrieve the QModelIndex for the specified cell
            index = model.index(row, column)

            # Get the data from the model at the specified index
            value = model.data(index)
            msg     = ( f"Value at   {row = },   '{column_name =}': {value}" )
            self.append_msg( msg, )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def _persons_view_clicked(self, index,   ):
        """ """
        self.append_function_msg( "_persons_view_clicked" )

        view    = self.persons_view
        msg     = f"_view_clicked {index} "
        self.append_msg( msg, )
        msg     = f"{INDENT}{view = } there is much to explore here, row, column, values"
        self.append_msg( msg, )

        msg     = f"{INDENT}{index} {index.row() = } {index.column() = } "
        self.append_msg( msg, )

        model           = self.persons_model
        persons_model   = model
        no_rows         = model.rowCount()

        msg     = f"{INDENT}{model.rowCount() = }   "
        self.append_msg( msg, )

        # extract some data
        row_ix       = index.row()
        age_ix       = 2
        age          = model.data( model.index( row_ix, age_ix ) )

        msg     = f"{INDENT}extracted data {age = }   "
        self.append_msg( msg, )

        # extract some data
        row_ix       = index.row()
        key_ix       = 0 # column may have been hidden
        key          = model.data( model.index( row_ix, key_ix ) )

        msg     = f"{INDENT}extracted data {key = }   "
        self.append_msg( msg, )

        msg     = f"{INDENT}phones are now displayed for for the persons clicked on"
        self.append_msg( msg, )

        # ---- sync up second model with row clicked in first
        phone_model     = self.phone_model
        phone_model.setFilter( f"persons_id = {key}" )
        phone_model.select()
        self.append_msg( tab_base.DONE_MSG )

    # -----------------------
    def delete_selected_record(self):
        """
        !!What it says
        """
        self.append_function_msg( "delete_selected_record implemented?/" )
        self.append_msg( tab_base.DONE_MSG )
    # --------------------------
    def prior_next( self, delta  ):
        """
        What it says
        delta may be positive or negative
        """
        self.append_function_msg( f"prior_next {delta = }" )

        ix                     = self.ix_id_list
        our_list               = self.id_list
        max                    = len( our_list )

        new_ix                 = ix + delta

        if   new_ix < 0:
            msg     = ( "wrap to max ix")
            self.append_msg( msg, )
            new_ix  = max - 1

        elif new_ix >= max:
            msg     = ( "wrap to ix = 0")
            self.append_msg( msg, )
            new_ix  = 0

        self.ix_id_list   = new_ix
        #return new_ix

        self.select_by_id( our_list[ new_ix ]  )

        self.append_msg( tab_base.DONE_MSG )

    # --------------------------
    def select_by_id( self, a_id   ):
        """
        What it says
        taken from stuff and simplifed
        """
        self.append_function_msg( f"select_by_id for persons {a_id = }" )

        record   = None
        model    = self.persons_model

        #ia_qt.q_sql_query_model( model, "select_record 1" )
        model.setFilter( f"id = {a_id}" )
        model.select()
        #ia_qt.q_sql_query_model( model, "select_record 2" )

        msg     = ( f"{INDENT}select_by_id{model.rowCount() = }  ")
        self.append_msg( msg, )


        #print( info_about.get( model, msg = "select_by_id post filter and select " ) )
        msg     = (  info_about.INFO_ABOUT.find_info_for(  model,
                                msg = "select_by_id post filter and select " ) )
        self.append_msg( msg, )


        if model.rowCount() > 0:
            record                  = model.record(0)
            #self.id_field.setText( str(record.value("id")) )
            #self.record_to_field( record )
            #self.textField.setText(record.value("text_data"))
            #self.record_state       = RECORD_FETCHED
            self.current_id         = a_id
            msg     = ( f"persons id = {a_id}")
            self.append_msg( msg, )

        else:
            msg    = ( f"Record not found! {a_id = }" )
            self.append_msg( msg, )


    # -----------------------
    def clear(self):
        """
        !!What it says

        from ask a chat bot
        Temporary Clearing: If the goal is to temporarily hide or reset the displayed
        data without affecting the database, using setTable("") or setQuery(QSqlQuery()) is safer

        If you only want to clear the view or selected data without altering the model, you can clear the view component:

            view.clearSelection()  # Assuming `view` is your QTableView

        or bad selection


        """
        self.append_function_msg( "clear experimenting with methods persons_model" )
        # like this the best
        # try a know bad select
        model       = self.persons_model
        model.setFilter( f"id = -99" )
        model.select()


    # -----------------------
    def save(self):
        """
        !!What it says
        """
        self.append_function_msg( "save" )

    # # ------------------------
    # def print_data(self):
    #     """ """
    #     what    = "print_data"
    #     print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

    #     DB_OBJECT.query_data()

    # # ------------------------
    # def do_selections(self):
    #     """ """
    #     what    = "print_data"
    #     print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

    # ------------------------
    def select_all(self):
        """ """
        self.append_function_msg( "select_all" )

        self.persons_model.setFilter( "" )
        self.persons_model.select()  # Load the data into the model

        self.phone_model.setFilter( "" )
        self.phone_model.select()



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

        msg    = "so far nothing implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def add_with_dialogold( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "add_with_dialog texting " )

        msg    = "so far nothing implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    def add_with_dialog_for_stuff(self):
        """
        Open dialog to add a new event and insert it into the model.
        did with wrong sql
        """

        self.append_function_msg( "add_with_dialog texting " )
        dialog = StuffEventDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # Create a new record
            row = self.model.rowCount()
            self.model.insertRow(row)

            # Set data for each field
            self.model.setData(self.model.index(row, 0), form_data["id"])
            self.model.setData(self.model.index(row, 1), form_data["stuff_id"])
            self.model.setData(self.model.index(row, 2), form_data["event_dt"])
            self.model.setData(self.model.index(row, 3), form_data["dlr"])
            self.model.setData(self.model.index(row, 4), form_data["cmnt"])
            self.model.setData(self.model.index(row, 5), form_data["type"])

        self.append_msg( tab_base.DONE_MSG )


    def add_new_person(self):
        """Open dialog to add a new person and insert it into the model."""

        self.append_function_msg( "add_new_person" )
        dialog = PersonDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # Create a new record
            row = self.model.rowCount()
            self.model.insertRow(row)

            # Set data for each field (except ID which is auto-incremented)
            self.model.setData(self.model.index(row, 1), form_data["name"])
            self.model.setData(self.model.index(row, 2), form_data["age"])
            self.model.setData(self.model.index(row, 3), form_data["family_relation"])
            self.model.setData(self.model.index(row, 4), form_data["add_kw"])

            # Submit the new record immediately to get the ID
            if self.model.submitAll():
                QMessageBox.information(self, "Success", "New person added successfully.")
                self.model.select()  # Refresh to show the new ID
            else:
                QMessageBox.warning(self, "Error",
                                   f"Database error: {self.model.lastError().text()}")
    # ------------------------------
    def get_selected_row_data(self):
        """Get the data from the currently selected row."""


        self.append_function_msg( "xxx" )
        # Get the currently selected row
        model       = self.persons_model
        view        = self.persons_view

        indexes     = view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "Warning", "No record selected.")
            return None

        # Get the model row index
        model_row = indexes[0].row()

        # Extract data from the row
        data = {
            "id":      model.data( model.index(model_row, 0)),
            "name":    model.data( model.index(model_row, 1)),
            "age":     model.data( model.index(model_row, 2)),
            "family_relation":     model.data( model.index(model_row, 3)),
            "add_kw":  model.data( model.index(model_row, 4))
        }

        return (model_row, data)

    def edit_selected_person(self):
        """
        Open dialog to edit the currently selected person.
        """
        self.append_function_msg( "xxx" )
        model       = self.persons_model

        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # Open dialog with the current data
        dialog = PersonDialog(self, edit_data=data)
        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # Update the row with the new data
            model.setData( model.index(row, 1), form_data["name"])
            model.setData( model.index(row, 2), form_data["age"])
            model.setData( model.index(row, 3), form_data["family_relation"])
            model.setData( model.index(row, 4), form_data["add_kw"])

    def delete_selected_person(self):
        """Delete the currently selected person."""
        self.append_function_msg( "delete_selected_person" )
        model       = self.persons_model

        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # Confirm deletion with the user
        reply = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete the selected person (ID: {data['id']}, Name: {data['name']})?",
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove the row from the model
            model.removeRow(row)

            # Apply the deletion immediately
            if model.submitAll():
                QMessageBox.information(self, "Success", "Person deleted successfully.")
            else:
                QMessageBox.warning(self, "Error",
                                   f"Database error: {self.model.lastError().text()}")
                model.select()  # Refresh the view

    # ------------------------------
    def submit_changes(self):
        """Submit all changes to the database."""
        self.append_function_msg( "xxx" )
        model       = self.persons_model

        if model.submitAll():
            QMessageBox.information(self, "Success", "All changes saved to database successfully.")
        else:
            QMessageBox.warning(self, "Error",
                               f"Database error: {model.lastError().text()}")
    # ------------------------------
    def refresh_data(self):
        """Refresh the data from the database."""
        self.append_function_msg( "xxx" )
        model       = self.persons_model
        model.select()

    # ------------------------
    def inspect(self):
        """ """
        self.append_function_msg( "inspect" )

        # locals for inspection
        my_tab_widget       = self
        parent_window       = self.parent( ).parent( ).parent().parent()
        #a_db                = parent_window.sample_db
        persons_model        = self.persons_model
        persons_view         = self.persons_view
        wat_inspector.go(
             msg            = "inspect QSqlTableModelTab",
             # inspect_me     = self.persons_model,
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )
    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )


class PersonDialog(QDialog):
    """
    Dialog for adding or editing a person record.
    """

    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Person" if edit_data is None else "Edit Person")

        # Create form layout and fields
        form_layout = QFormLayout()

        # ID field (Only shown when editing)
        self.id_spinbox = QSpinBox()
        self.id_spinbox.setRange(1, 999999)
        if edit_data is not None:
            form_layout.addRow("ID:", self.id_spinbox)
            self.id_spinbox.setValue(edit_data["id"])
            self.id_spinbox.setReadOnly(True)  # ID shouldn't be changed

        # Name field
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(150)
        form_layout.addRow("Name:", self.name_edit)

        # Age field
        self.age_edit = QLineEdit()
        self.age_edit.setMaxLength(150)
        form_layout.addRow("Age:", self.age_edit)

        # Family relation field
        self.family_relation_edit = QTextEdit()
        self.family_relation_edit.setAcceptRichText(False)
        form_layout.addRow("Family Relation:", self.family_relation_edit)

        # Additional Keywords field
        self.add_kw_edit = QLineEdit()
        self.add_kw_edit.setMaxLength(150)
        form_layout.addRow("Additional Keywords:", self.add_kw_edit)

        # If we're editing, populate the fields with the existing data
        if edit_data is not None:
            self.name_edit.setText(edit_data["name"])
            self.age_edit.setText( str( edit_data["age"]) ) # tweak
            self.family_relation_edit.setPlainText(edit_data["family_relation"])
            self.add_kw_edit.setText(edit_data["add_kw"])

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setMinimumWidth(400)

    def get_form_data(self):
        """Get the data from the form fields as a dictionary."""
        data = {
            "name": self.name_edit.text(),
            "age": self.age_edit.text(),
            "family_relation": self.family_relation_edit.toPlainText(),
            "add_kw": self.add_kw_edit.text()
        }

        # Include ID if it exists (edit mode)
        if hasattr(self, 'id_spinbox') and self.id_spinbox.isVisible():
            data["id"] = self.id_spinbox.value()

        return data

class StuffEventDialogxxx( QDialog ):
    """Dialog for adding or editing a record in the stuff_event table."""

    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Event" if edit_data is None else "Edit Event")

        # Create form layout and fields
        form_layout = QFormLayout()

        # ID field
        self.id_edit = QLineEdit()
        self.id_edit.setMaxLength(15)
        form_layout.addRow("ID:", self.id_edit)

        # Stuff ID field
        self.stuff_id_edit = QLineEdit()
        self.stuff_id_edit.setMaxLength(15)
        form_layout.addRow("Stuff ID:", self.stuff_id_edit)

        # Event date/time field (stored as integer timestamp)
        self.event_date_edit = QDateTimeEdit(QDateTime.currentDateTime())
        form_layout.addRow("Event Date:", self.event_date_edit)

        # DLR field (integer)
        self.dlr_spinbox = QSpinBox()
        self.dlr_spinbox.setRange(0, 9999)
        form_layout.addRow("DLR:", self.dlr_spinbox)

        # Comment field
        self.comment_edit = QLineEdit()
        self.comment_edit.setMaxLength(150)
        form_layout.addRow("Comment:", self.comment_edit)

        # Type field
        self.type_combobox = QComboBox()
        # Add your event types here
        self.type_combobox.addItems(["Type1", "Type2", "Type3"])
        form_layout.addRow("Type:", self.type_combobox)

        # If we're editing, populate the fields with the existing data
        if edit_data is not None:
            self.id_edit.setText(edit_data["id"])
            self.stuff_id_edit.setText(edit_data["stuff_id"])

            # Convert timestamp to QDateTime
            dt = QDateTime()
            dt.setSecsSinceEpoch(edit_data["event_dt"])
            self.event_date_edit.setDateTime(dt)

            self.dlr_spinbox.setValue(edit_data["dlr"])
            self.comment_edit.setText(edit_data["cmnt"])

            # Find and set the index for the type
            index = self.type_combobox.findText(edit_data["type"])
            if index >= 0:
                self.type_combobox.setCurrentIndex(index)

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def get_form_data(self):
        """Get the data from the form fields as a dictionary."""
        data = {
            "id": self.id_edit.text(),
            "stuff_id": self.stuff_id_edit.text(),
            "event_dt": int(self.event_date_edit.dateTime().toSecsSinceEpoch()),
            "dlr": self.dlr_spinbox.value(),
            "cmnt": self.comment_edit.text(),
            "type": self.type_combobox.currentText()
        }
        return data
