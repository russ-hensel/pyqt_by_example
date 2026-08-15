#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof
"""


KEY_WORDS:      table model for relational sql join crud update add insert zz cursor
CLASS_NAME:     QSqlRelationalTableModelTab_4
WIDGETS:         QSqlRelationalTableModel QTableView workin in dev
STATUS:         just working on it -- but it works, and needs work
TAB_TITLE:       QSqlRelationalTableModel / #4 in dev
DESCRIPTION:    A experiment  for the QSqlRelationalTableModel does update
HOW_COMPLETE:   0 #   ... retired in favor of QSqlRelationalTableModelUpdate



"""
WIKI_LINK      =  "https://github.com/russ-hensel/qt5_by_example/wiki/What-We-Know-About-QDateEdit"

"""


tab_q_sql_relational_model_2.QSqlRelationalTableModelTab_2()

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


# ---- imports


#from app_global import AppGlobal
from qtpy.QtCore import (Qt)

from qtpy.QtCore import Qt, QModelIndex



from qtpy.QtSql import (
                        QSqlRelation,
                         QSqlRelationalTableModel,
                         QSqlTableModel,
                         QSqlDatabase,

                         )



from qtpy.QtWidgets import (
                            QHBoxLayout,
                            QPushButton,
                            QAbstractItemView,
                            QTableView,
                            QVBoxLayout,
                             )


import utils_for_tabs as uft
import wat_inspector
import tab_base
import global_vars

INDENT        = uft.INDENT
BEGIN_MARK_1  = uft.BEGIN_MARK_2
BEGIN_MARK_2  = uft.BEGIN_MARK_2



# ------------------------------------------
class PersonsPhonesModel( QSqlRelationalTableModel ):
    """
    cursor says, russ edits
    Base table: persons_phones.
    Shows persons.name via relation on person_id.
    Editable: persons_phones columns only (not persons.name / person_id).
  """

    def __init__( self, parent=None, db=None ):
        super().__init__( parent, db )
        self._person_id = None

        # you apply changes explicitly in apply_update()
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit )

    # ------------------------------------------
    def setup_and_select( self, person_id ):
        """
        Load all phone rows for one person.

        person_id : bind value for persons.id / persons_phones.person_id
        """
        self.setup()

        ok = self.select_for_id( person_id )


        return ok

    # ------------------------------------------
    def select_for_id( self, person_id ):
        """
        Load all phone rows for one person.

        person_id : bind value for persons.id / persons_phones.person_id
        """
        self._person_id = int( person_id )

        # filter to this person only (SQLite: literal in filter string)
        self.setFilter( f"person_id = {self._person_id}" )

        ok = self.select()
        if not ok:
            raise RuntimeError(
                f"persons_phones select failed: {self.lastError().text()}"
            )

        return ok

    # ------------------------------------------
    def setup( self,   ):
        """
        Load all phone rows for one person.

        person_id : bind value for persons.id / persons_phones.person_id
        """
        self.setTable( "persons_phones" )

        # show persons.name instead of raw person_id in the grid
        person_id_col       = self.fieldIndex( "person_id" )
        self.person_id_col  = person_id_col
        self.setRelation(
            person_id_col,
            QSqlRelation( "persons", "id", "name" ),
        )



    # ------------------------------------------
    def flags( self, index ):
        """
        persons.name is shown through person_id relation -> keep read-only.
        persons_phones.id is usually read-only too.
        """
        f = super().flags( index )

        if not index.isValid():
            return f

        field = self.record().fieldName( index.column() )

        if field in ( "person_id", "id" ):
            f &= ~Qt.ItemFlag.ItemIsEditable

        return f

    # ------------------------------------------
    def apply_update( self ):
        """
        Write pending edits to persons_phones only.

        Returns True on success.
        """
        if not self.isDirty():
            return True

        ok = self.submitAll()
        if not ok:
            err = self.lastError().text()
            raise RuntimeError( f"persons_phones update failed: {err}" )

        return True

    # ------------------------------------------
    def revert_changes( self ):
        """
        Discard edits not yet submitted.
        """
        self.revertAll()





#-----------------------------------------------
class QSqlRelationalTableModelTab_4( tab_base.TabBase  ):
    """
    for widgets joining two tables
    """
    def __init__(self, ):
        """
        """
        super().__init__( )

        self.module_file       = __file__      # save for help file usage
        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self.relation      = ( "", "", "",  )
        self.relation      = ( "persons", "id", "name" )
        self.relation      = ( "persons", "id", "name, age" )
        self.relation      = ( "persons", "id", "name, age, id" ) # ng
               # try to add foreigh key now broken

        self.relation      = ( "persons", "id", "name, age, person_id" ) #
               # try to add foreigh key now broken

        print( f"Note option of {self.relation = }")
        self.help_file_name     =  "qsql_relational_table_model_tab_2.txt"
        self._build_model()
        self._build_gui()

        self.model.select()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )



        layout.addWidget( self.view   )


        layout.addLayout( button_layout )

        # # ---- PB select_for\n_all
        # widget            = QPushButton( "select_\n_all" )
        # connect_to        = self.select_all
        # widget.clicked.connect( connect_to )
        # button_layout.addWidget( widget )

        # ---- PB select\n_some
        widget            = QPushButton( "select\n_some" )
        connect_to        = self.select_some
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # # ---- PB select\n_some
        # widget            = QPushButton( "select\n_some" )
        # connect_to        = self.select_some
        # widget.clicked.connect( connect_to )
        # button_layout.addWidget( widget )

        # ---- PB set_heading_by_number
        widget            = QPushButton( "set_heading\n_by_number" )
        widget.clicked.connect( self.set_heading_by_number )
        button_layout.addWidget( widget )

        # # ---- PB sset_heading_by name
        # widget            = QPushButton( "set_heading\n_by_name" )
        # widget.clicked.connect( self.set_heading_by_name )
        # button_layout.addWidget( widget )

        # ---- PB "get_data\n_from_model"
        widget              = QPushButton( "get_data\n_from_model" )
        connect_to          = self.get_data_from_model
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB get_selected_rows
        widget            = QPushButton("get_selected\n_rows")
        widget.clicked.connect( self.get_selected_rows )
        button_layout.addWidget( widget )

        # # ---- PB delete_selected_row
        # widget            = QPushButton("delete_selected\n_row")
        # widget.clicked.connect( self.delete_selected_row )
        # button_layout.addWidget( widget )


        # # ---- PB i"insert\n_record"
        # widget            = QPushButton("add\n_record")
        # connect_to        = self.add_record
        # widget.clicked.connect( connect_to )
        # button_layout.addWidget( widget )

        # # ---- PB add_test_record
        # widget            = QPushButton("add_test\n_record")
        # widget.clicked.connect( self.add_test_record )
        # button_layout.addWidget( widget )

        # # ---- PB add_test_record
        # widget            = QPushButton("add_via\n_chat")
        # widget.clicked.connect( self.add_via_chat )
        # button_layout.addWidget( widget )


        # ---- PB i"insert\n_record"
        widget            = QPushButton("update_db\n")
        connect_to        = self.update_db
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB special inspect
        widget              = QPushButton("special\ninspect")
        # widget.clicked.connect(lambda: self.print_message(widget.text()))
        connect_to          = self.special_inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- last buttons in own layout
        button_layout    = QHBoxLayout()
        layout.addLayout( button_layout )

        # our ancestor finishes off the tab with some standard buttons
        self.build_gui_last_buttons( button_layout )

    # ------------------------------
    def _build_model( self,   ):
        """

        will need         self.model and view
        """
        db = QSqlDatabase.database()   # your existing connection

        model           = PersonsPhonesModel( self,  global_vars.EX_DB )
        self.model      = model
        model.setup_and_select( person_id = 1002 )

        view            = QTableView()
        self.view       = view
        view.setModel( model )
        view.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
        )

        # # user edits phone_number / zone in the grid ...

        # model.apply_update()    # UPDATE persons_phones ...
        # # or on error:
        # # model.revert_changes()

    # ------------------------
    def get_selected_rows_dupe_delete(self, index,   ):
        """ """
        self.append_function_msg( "get_selected_rows" )

        view            = self.view   # QTableView

        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()  # Get the selected rows

            for index in selected_indexes:
                row = index.row()
                print(f"Selected row: {row = }")

    # -----------------------
    def special_inspect(self):
        """
        what it says
        """
        self.append_function_msg( "special_inspect" )

        model           = self.model
        new_record      = model.record()
        c_names         = []
        for ix in range( 7 ):
            i_name     = new_record.fieldName( ix )
            c_names.append( i_name )
            print( f"{ix = }:   {new_record.fieldName( ix ) = } " )

        #c_names      = [ "name", "phone_number", "xxx"]
        for i_name in c_names:
            print( f"{i_name = }:   {new_record.indexOf( i_name ) = } " )

        print( "\n field index on record names ")
        for i_name in c_names:
            print( f"{i_name = }:   {model.fieldIndex( i_name ) = }" )

        print( "did this get left off ?" )
        msg      = ( f'{ model.fieldIndex( "person_id") = }' )
        self.append_msg( msg,   )

        for column in range(model.columnCount()):
            header   = model.headerData(column, Qt.Horizontal)
            msg      = (f"Column {column}: {header}")
            self.append_msg( msg,   )

    # -----------------------
    def add_via_chat( self ):
        """
        another way is just to insert with a sqlquery thing and \
        then reselect, not what i wanted to do but pagmatic
        do i reselect I do not see it

        """

        # if query.lastError().isValid():
        #     print(query.lastError().text())
        #     return

        # # Set up the model
        # model = QSqlRelationalTableModel()
        # model.setTable("persons_phones")
        # model.setRelation(model.fieldIndex("person_id"), QSqlRelation("persons", "id", "name"))
        # model.select()
        self.append_function_msg( "add_via_chat" )

                # Add a new row
        model       = self.model
        db          = model.database()
        if not db.transaction():
            msg     = ( f"Failed to start transaction: {db.lastError().text()}" )
            self.append_msg( msg,   )

        row         = model.rowCount()  # Index for the new row
        model.insertRow(row)

        # Set values for the new row  --- does auto gen work ok

        # which table are these in the primay table  -- think only person id which is really id
        model.setData(model.index( row, model.fieldIndex( "person_id")),     1001)   # 1001 = Alice ?
        model.setData(model.index( row, model.fieldIndex( "phone_number")), "123-456-7890")
        model.setData(model.index( row, model.fieldIndex( "zone")),          "Z")

        # Debugging: Check if the row was inserted
        msg      = ("New row data before submission:")
        self.append_msg( msg,   )
        for col in range(model.columnCount()):
            msg      = (f"{model.headerData(col, Qt.Horizontal)}: {model.data(model.index(row, col))}")
            self.append_msg( msg,   )
        # update and -- do not see select
        if not model.submitAll():
            msg      = ("add_via_chat Error saving data:", model.lastError().text())
            self.append_msg( msg,   )
        else:
            msg      = ("Data added successfully.")
            self.append_msg( msg,   )
        if not db.commit():
            msg      = ("Database commit failed:", db.lastError().text())
            self.append_msg( msg,   )
        # Set up a view to display the data  --- do we need this ?? try without
        # view = QTableView()
        self.view.setModel(model)

        self.view.show()

    # -----------------------
    def add_record(self):
        """
        what it says
            we need to add to primary table here: persons_phones

           SELECT
               persons.id,
               persons.name,
               persons.age,
               persons.family_relation,
               persons_phones.phone_number

           FROM persons_phones
           LEFT JOIN persons ON persons.id = persons_phones.person_id

        """
        1/0   # us add via chat
        self.append_function_msg( "add_record" )

        msg             = "data for id  123  name  John Doe"
        print( msg )

        model           = self.model
        new_record      = model.record()

        """
        CREATE TABLE persons_phones (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id       INTEGER,
                phone_number    TEXT,
                zone            TEXT,
                FOREIGN KEY(person_id) REFERENCES persons(id) ON DELETE CASCADE
            )
        """

        # --- set values
        new_record.setValue( "id", 123)                  # appeared
        new_record.setValue( "name", "John Doe")         # nothing visible
        new_record.setValue( "age", 30)                   # nothing visible
        new_record.setValue( "family_relation", "Brother")   # nothing visible
        new_record.setValue( "phone_number", "123 456 7890")   # appeared off by column
        new_record.setValue( "zone", "Z")   # appeared wrong place

        if model.insertRecord(-1, new_record):
            pass
            # if model.submitAll():
            #     print("Record inserted and changes committed to the database.")
            # else:
            #     print("Error committing changes:", model.lastError().text())
        else:
            msg      = ("Error inserting record:", model.lastError().text())
            self.append_msg( msg,   )
        msg      = ( "the database has not yet been updated -- "
                "you may want to update_db, select_all or get_data_from_model next ")
        self.append_msg( msg,   )

    # -----------------------
    def add_test_record(self):
        """
        what it says
            try to add to every column
            just test data so we can see where it goes

        some set data just disappears and mapping seems wrong
        """
        self.append_function_msg( "add_test_record" )

        msg             = "data is data_0 _1....."
        self.append_msg( msg,   )

        model           = self.model
        new_record      = model.record()

        # put in data
        c_names         = []
        for ix in range( 7 ):
            i_name     = new_record.fieldName( ix )
            c_names.append( i_name )
            msg      = ( f"{ix = }: {new_record.fieldName( ix ) = } " )
            if i_name:
                new_record.setValue( i_name, f"data_{ix}")

        if model.insertRecord(-1, new_record):
            pass

        else:
            msg      = ("Error inserting record:", model.lastError().text())
            self.append_msg( msg,   )

        msg      = ( "the database has not yet been updated -- you may want to update_db, select_all or get_data_from_model next ")
        self.append_msg( msg,   )

    # -----------------------
    def update_db( self ):
        """
        what it says
        """

        self.append_function_msg( "update_db" )

        model           = self.model

        model.apply_update()

        # if model.submitAll():
        #     msg      = ("Changes committed no error detected ")
        #     self.append_msg( msg,   )

        # else:
        #     msg      = ("Error committing changes:", model.lastError().text())
        #     self.append_msg( msg,   )

        msg      = ( "you may want to select_all or get_data_from_model next ")
        self.append_msg( msg,   )

    # ------------------------
    def set_heading_by_number( self ):
        """
        what it says
        """
        self.append_function_msg( "set_heading_by_number" )

        msg        = "The lables are in numeric order ."
        self.append_msg( msg,   )

        model      = self.model
        model.setHeaderData(0, Qt.Horizontal, "c0")
        model.setHeaderData(1, Qt.Horizontal, "c1")
        model.setHeaderData(2, Qt.Horizontal, "c2")
        model.setHeaderData(3, Qt.Horizontal, "c3")
        model.setHeaderData(4, Qt.Horizontal, "c4")
        model.setHeaderData(5, Qt.Horizontal, "c5")
        model.setHeaderData(6, Qt.Horizontal, "c6")

    # ------------------------
    def set_heading_by_name(self):
        """
        what it says
        """
        self.append_function_msg( "set_heading_by_name" )

        msg        = "I have tried to get the qualified database names in here."
        self.append_msg( msg,   )
        msg        = "Note that headers can span lines."
        self.append_msg( msg,   )
        model      = self.model
        model.setHeaderData(0, Qt.Horizontal, "persons_phone\n.id" )
        model.setHeaderData(1, Qt.Horizontal, "persons\n.name")
        model.setHeaderData(2, Qt.Horizontal, "persons\n.age")
        model.setHeaderData(3, Qt.Horizontal, "persons_phone\n.phone_number")
        model.setHeaderData(4, Qt.Horizontal, "persons_phone\n.zone")
        model.setHeaderData(5, Qt.Horizontal, "c5")
        model.setHeaderData(6, Qt.Horizontal, "c6")


    # ------------------------
    def select_all(self):
        """
        select with a sort
        """
        self.append_function_msg( "select_all" )

        self.append_function_msg( "set filter to '' and .select" )

        model        = self.model

        # this may cause problems elsewhere
        # column_index = model.fieldIndex( "age" )  # Get the column index for "name"
        # print( f"for sorting {column_index = }")
        # model.setSort( column_index , Qt.AscendingOrder)  # seems needs to be index no

        model.setFilter( "" )

        model.select()

        self.append_function_msg( "select_all done" )

    # ------------------------
    def select_some(self):
        """
        select base on some criteria, read the code for details
        """
        person_id = 1002
        self.append_function_msg( f"select_some { person_id = }" )

        self.model.select_for_id(  person_id = 1002 )
        #self.model.setFilter( 'age >  26'   )
        #self.model.select()

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
        self.append_function_msg( "get_data_from_model" )

        model           = self.model

        row_count       = model.rowCount()
        column_count    = model.columnCount()

        for ix_row in range( row_count ):
            for ix_col  in range( column_count ):   # should figure out a column count
                index     = model.index( ix_row,   ix_col   )
                data      = model.data( index )
                msg       = f"for {ix_row = } {ix_col = }  {data = }"
                self.append_msg( msg,   )

    # ------------------------
    def do_selections(self):
        """
        not sure ... is dead?
        """
        self.append_function_msg( "do_selections" )


    # ------------------------
    def get_selected_rows(self, index,   ):
        """ """
        self.append_function_msg( "get_selected_rows" )

        # from qtpy.QtWidgets import QTableView, QAbstractItemView
        # from qtpy.QtCore import Qt

        view            = self.view
        # Assuming `view` is your QTableView
        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()  # Get the selected rows

            # Iterate over the selected rows
            for index in selected_indexes:
                row = index.row()  # Get the row number
                msg      = ( f"Selected row: {row = }" )
                self.append_msg( msg,   )

    # ------------------------
    def delete_selected_row(self):
        """
        or even rows
        """
        self.append_function_msg( "delete_selected_row" )

        #from qtpy.QtSql import QSqlRelationalTableModel

        view            = self.view

        msg     = "for now just get first seleectd row if any "
        self.append_msg( msg,   )

        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()  # Get the selected rows

            # Iterate over the selected rows
            for index in selected_indexes:
                row = index.row()  # Get the row number
                msg      = ( f"Selected row: {row = }" )
                self.append_msg( msg,   )
                break

        if row >= 0:
            # Assuming you already have a configured QSqlRelationalTableModel
            model = self.model

            # Deleting a single row
            #row_to_delete = 2  # Replace with the row number you want to delete
            if model.removeRow( row ):
               msg      = (f"Row {row = } marked for deletion. But may still show in view")
               self.append_msg( msg,   )

            else:
               msg      = ( "Failed to mark row for deletion.")
               self.append_msg( msg,  )

            msg      =( "for things to continue to work you should probably update the db ")
            self.append_msg( msg,   )
        # # Committing the changes to the database
        # if model.submitAll():
        #     print("Changes committed to the database.")
        # else:
        #     print("Failed to commit changes to the database:", model.lastError().text())

        # # If you want to refresh the view after deletion
        # model.select()

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg,   )

        self.append_msg( "mutate_0 done" )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "so far not implemented "
        self.append_msg( msg,  )

        self.append_msg( "mutate_1 done" )


    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        # make some locals for inspection
        my_self                 = self
        parent_window           = self.parent( ).parent( ).parent().parent()
        a_db                    = parent_window.sample_db
        local_self_model        = self.model    # relational model
        local_self_view         = self.view     #  QTableView

        new_record              = self.model.record()  # just to see what we can see

        wat_inspector.go(
             msg            = "inspect for QSqlRelationalTableModel_2 new_record just for inspection ",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "inspect done" )


    # ------------------------
    def breakpoint(self):
        """
        the usual
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( "breakpoint done" )
# ---- eof
