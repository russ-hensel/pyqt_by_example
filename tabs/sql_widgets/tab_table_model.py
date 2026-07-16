#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
tab_table_model.py


KEY_WORDS:      programatically populated tabe for data add remove select QTableModel
CLASS_NAME:     TableModelTab
WIDGETS:        QAbstractTableModel QTableView QSortFilterProxyModel
STATUS:         more or less a mess, think never finished
TAB_TITLE:      QAbstractTableModel / with Proxy
DESCRIPTION:    A reference for the QAbstractTableModel widget
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QPushButtons"
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------

from functools import partial

from qtpy.QtCore import ( QAbstractTableModel,
                          QModelIndex,
                          QSortFilterProxyModel,
                          Qt,
                          )

from qtpy.QtWidgets import ( QHBoxLayout,
                             QHeaderView,
                             QPushButton,
                             QTableView,
                             QVBoxLayout
                             )


import utils_for_tabs as uft
import wat_inspector
import tab_base


print_func_header =  uft.print_func_header

# ---- end imports

# ------------------------
class ATableModel( QAbstractTableModel ):
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

    # ------------------------
    def rowCount(self, index=None):
        """
        what it says read
        why index = None, drop it
        """
        return len( self._data )

    # ------------------------
    def columnCount(self, index=None ):
        return len(self._headers)

    # ------------------------
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    # ------------------------
    def set_data(self, data ):
        self._data      = data

    # ------------------------
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

    # ------------------------
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)

    # ------------------------
    def addRow(self, row_data):
        """
        read
        row_data   a list of the data types ??
        remember to invalidate index if any --- may build in or not
        """
        self.beginInsertRows(self.index(len(self._data), 0), len(self._data), len(self._data))
        self._data.append(row_data)
        self.endInsertRows()

    # ------------------------
    def removeRow(self, row_index):
        """
        what it says, read
        !! emits seem to be messed up fixed ?
        """
        # self.beginRemoveRows(self.index(row_index, 0), row_index, row_index)
        self.beginRemoveRows(self.createIndex(row_index, 0).parent(), row_index, row_index)
        self._data.pop( row_index )
        self.endRemoveRows()
        self.layoutChanged.emit()
        self.dataChanged.emit()
        #return True

    # ---------------------------
    def clear_data(self):
        """
        what it says, read
        """
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

#-----------------------------------------------
class TableModelTab( tab_base.TabBase  ):
    """
        see ez_qt table_widget and table_model table_widget
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__()

        self.help_file_name     =  "table_model_tab.txt"
        self.sort_ix            = 0 # modify sort each time

        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]     = self.mutate_2
        # self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4
        self.table_model_is_hidden = False   # !! really needs a rework
        self.build_model()
        self._build_gui()

    #--------------------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        this is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        # ---- new row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        table_view    = self.table_view
        row_layout.addWidget( table_view )

        button_layout = QHBoxLayout(   )

        # ---- QPushButtons
        layout.addLayout( button_layout )

        # ---- QPushButtons
        layout.addLayout( button_layout )
        # widget        = QLabel( 'table_model\n TableModel()/QTableView()' )
        # button_layout.addWidget( widget )

        #-------------
        widget          = QPushButton( "table_model_\ntab_populate" )
        widget.clicked.connect( lambda: self.table_model_tab_populate() )
        button_layout.addWidget( widget )

        #-------------
        widget = QPushButton("table_model_\ntab_get_data")
        widget.clicked.connect(lambda: self.table_model_tab_get_data( ) )
        #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        button_layout.addWidget( widget )

        # ---- PB get_selected_rows
        widget              = QPushButton("get_selected_rows\n")
        widget.clicked.connect( self.get_selected_rows )
        button_layout.addWidget( widget )

        # ---- PB select_column
        widget              = QPushButton("select_column\n")
        widget.clicked.connect( self.select_column )
        button_layout.addWidget( widget )

        # #-------------!! revisit
        # widget = QPushButton("hide/\nunhide")
        # widget.clicked.connect(lambda: self.table_model_hide_unhide( ) )
        # a_widget        = widget
        # #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        # button_layout.addWidget( widget )

        #-------------
        widget = QPushButton("hide\n_unhide column")
        widget.clicked.connect(lambda: self.table_model_toggle_hide_column( ) )
        #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        button_layout.addWidget( widget )

        # --- select a row
        a_widget           = QPushButton("select_\nrow_2 ( 0 based )")
        connect_to         = partial( self.select_row, 2 )
        a_widget.clicked.connect( connect_to )
        button_layout.addWidget(a_widget)

        #-------------
        widget = QPushButton("remove_row_\nselected")
        widget.clicked.connect( self.remove_row_selected )
        #widget.clicked.connect( lambda: self.widget_clicked( a_widget ) )
        button_layout.addWidget( widget )

        widget        = QPushButton('clear_\nall_rows')
        widget.clicked.connect(self.clear_all_rows )
        button_layout.addWidget( widget )

        widget        = QPushButton('sort\n')
        widget.clicked.connect(self.sort )
        button_layout.addWidget( widget )

        widget        = QPushButton('table_model\n_inspect')
        widget.clicked.connect(self.table_model_inspect )
        button_layout.addWidget( widget )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # -------------------------------------
    def build_model(self,   ):
        """
        what it says
        and view..... self.table_view
        """
        headers = ["Name", "Age", "Occupation" ]
        #self.view           = QTableView()
        self.table_model   =  ATableModel( headers )  # QAbstractTableModel
        #self.model.set_data( data )

        # Proxy model for sorting
        proxy_model         = QSortFilterProxyModel()
        proxy_model.setSourceModel( self.table_model )
        self.proxy_model    = proxy_model

        table_view                  = QTableView()
        self.table_model_table_view = table_view
        self.table_view             = table_view
        # Connect the clicked signal to a slot
        table_view.doubleClicked.connect( self.double_clicked )
        table_view.doubleClicked.connect( self.clicked )

        # really shhould have just one of below
        #table_view.setModel( self.table_model )  # table_model for no sorting
        table_view.setModel( proxy_model )  # table_model for no sorting

        # next not crrently working may be in conflict with other code
        table_view.setSortingEnabled( True )
            # Enables sorting by clicking column headers may need QSort....

        print( "some selection options" )
        table_view.setSelectionBehavior( QTableView.SelectRows )       # For row selection
        # table_view.setSelectionBehavior( QTableView.SelectColumns )  # For column selection
        # table_view.setSelectionBehavior(QTableView.SelectItems)      # For item selection

    # -------------------------------------
    def table_model_tab_populate(self,   ):
        """
        what it says
            seems ok
        populates a row at a time
        """
        self.append_msg( "table_model_tab_populate -- add rows" )

        model      = self.table_model

        for ix in range( 3 ):
            # self.view_all_subjects.setModel(  self.model_all_subjects )
            # model        = self.model_display
            row_data     = [ f"a{ix}", f"b{ix}",   f"c{ix}", f"d{ix}" ]
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
        self.append_msg(  "table_model_hide_unhide !! fix me " )

        # if self.table_model_filter:
        #     self.table_model_filter   = FilterProxyModelHideRows( )

    #-----------------------------------------------
    def double_clicked( self, index: QModelIndex):
        """
        what it says,
        index comes from table view
        """
        self.append_msg( "double_clicked" )

        model    = self.table_model
        row      = index.row()
        self.append_msg(  f"on_row_other_clicked {row = }")
        #self.add_ix_other( row )

    #-----------------------------------------------
    def clicked( self, index: QModelIndex):
        """
        what it says,
        index comes from table view
        """
        self.append_msg( "clicked" )

        model    = self.table_model
        row      = index.row()
        self.append_msg(  f"on_row_other_clicked {row = }" )

        self.select_row( row )

    #-----------------------------------------------
    def select_column(self, ):
        """
        Select a specific column.
        may want to test and hook up
        """
        self.append_msg( "select_column" )

        col_index       = 1

        selection_model = self.table_view.selectionModel()

        model           = self.table_model

        col_start       = model.index(0, col_index)
        col_end         = model.index( model.rowCount() - 1, col_index)

        selection_model.select(col_start, selection_model.Select | selection_model.Columns)

    # ------------------------
    def get_selected_rows(self, index,   ):
        """ """
        self.append_msg( "get_selected_rows" )

        view            = self.table_view

        self.append_msg( "the selected rows follow.... " )

        selection_model = view.selectionModel()

        if selection_model:
            selected_indexes = selection_model.selectedRows()

            for index in selected_indexes:
                row = index.row()
                self.append_msg( f"Selected row: {row = }" )

    #-----------------------------------------------
    def table_model_toggle_hide_column(self,   ):
        """
        we actually use the view
        """
        self.append_msg( "table_model_toggle_hide_column" )

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
        self.append_msg( "table_model_tab_get_data" )

        model           = self.table_model

        data_list       = [  ]
        ix_row          = 0

        for ix_col in range( 3 ):
            index     = model.index( ix_row, ix_col )
            data      = model.data( index, ) #role=Qt.DisplayRole)
            data_list.append( data )

        self.append_msg( f"table_model_tab_get_data {data_list = }" )

    # ------------------------------------------
    def table_model_inspect(self):
        """
        what it says, read
        """
        self.append_msg( "table_model_inspect" )

        view     = self.table_model_table_view
        # def get_selected_row_and_column():
        selected_indexes = view.selectionModel().selectedIndexes()

        if selected_indexes:

            for index in selected_indexes:
                row     = index.row()
                column  = index.column()
                self.append_msg( f"Selected Cell - Row: {row}, Column: {column}")

        else:
            self.append_msg( "No selection" )

    #-----------------------------------------------
    def select_row(self, row_index ):
          """
          Select a specific row.
          """
          self.append_msg( "\nselect_row" )
          model           = self.table_model
          view            = self.table_view
          # Get the selection model from the view
          selection_model = view.selectionModel()

          row_start       = model.index( row_index, 0 )
          row_end         = model.index( row_index, model.columnCount() - 1 )

          selection_model.select( row_start, selection_model.Select | selection_model.Rows )

    # ------------------------------------------
    def add_row_at_end( self ):
        """
        may work needs to be hooked up
        """
        self.append_msg( "\nadd_row_at_end" )

        row_position = self.table_model.rowCount()
        self.table_model.insertRow( row_position )

    # ------------------------------------------
    def clear_all_rows(self):
        """
        what it says

        """
        self.append_msg( "\nclear_all_rows" )
        model           = self.table_model
        model.clear_data()

    # ------------------------------------------
    def remove_row_selected(self):
        """
        what it says
        see also selection in get_selected_rows
        """
        self.append_msg( "\nget_selected_rows" )

        model           = self.table_model
        view            = self.table_view

        row             = -1
        # Assuming `view` is your QTableView
        selection_model = view.selectionModel()

        if selection_model:
            selected_indexes = selection_model.selectedRows()

            # will get the first selected
            for index in selected_indexes:
                row = index.row()
                self.append_msg(f"Selected row: {row = }")
                break   # only get one

        if row == -1:
            self.append_msg( "no selected row")
            return

        model.removeRow( row )

    # ------------------------------
    def set_size(self):
        """
        read it
        may work needs to be hooked up
        """
        self.append_msg( "\nset_size" )

        self.table_model.horizontalHeader().setStretchLastSection( True )
        self.table_model.horizontalHeader().setSectionResizeMode(
                                               QHeaderView.Stretch )

    # ------------------------------
    def sort(self):
        """
        read it

        """
        self.append_msg( "\nsort" )

        # !! more research on args
        self.sort_ix  += 1
        if self.sort_ix > 1:
            self.sort_ix = 0

        if self.sort_ix == 0:
            sort_order  = Qt.AscendingOrder

        else:
            sort_order  = Qt.DescendingOrder   # Qt.AscendingOrder

        self.append_msg( f"sort on column 1 {sort_order = }" )
        self.proxy_model.sort(  1, sort_order  )

    #----------------------------
    def mutate_0( self  ):
        """
        read it

        """
        self.append_function_msg( "mutate_0()" )
        table   = self.table_model
        view    = self.table_view

        msg     = "hide row and column 1"
        self.append_msg( msg )

        view.hideRow( 1 )
        view.hideColumn( 1 )

        self.append_msg( tab_base.DONE_MSG )

    #----------------------------
    def mutate_1( self  ):
        """
        read it

        """
        self.append_function_msg( "mutate_1()" )
        table   = self.table_model
        view    = self.table_view

        msg     = "show row and column 1"
        self.append_msg( msg )

        view.showRow( 1 )
        view.showColumn( 1 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------
    def on_cell_clicked( self, row, col  ):
        """
        read it

        may work needs to be hooked up
        """
        self.append_msg( "\non_cell_clicked" )

    # ------------------------------
    def search(self, search_for   = "1," ):
        """
        read it
        passing of argument unclear ????

        may work needs to be hooked up
        """
        self.append_msg( "\nsearch" )

        search_for   = "1,"

        msg          = f"search {search_for = }"
        self.append_msg( msg )

        a_widget    =    self.table_model

        # Clear current selection first ??
        a_widget.setCurrentItem( None )

        if not search_for:
            msg      =  "Empty string, don't search."
            self.append_msg( msg )
            return

        matching_items = a_widget.findItems( search_for, Qt.MatchContains )

        if matching_items:
            # We have found something.
            item       = matching_items[0]  # Take the first.
            msg        = f"found {item = }"
            self.append_msg( msg )
            a_widget.setCurrentItem(item)

        else:
            msg        = f"nothing found {search_for = }"
            self.append_msg( msg )

    # ------------------------
    def find_row_with_text( self  ):
        """
        read it

        """
        print_func_header( "find_row_with_text" )

        table               = self.table_model
        ix_col_searched     = 2
        ix_found            = None
        target_text   = "Cell (2, 2)"
        for row in range( table.rowCount() ):
            item = table.item( row, ix_col_searched )
            if item and item.text() == target_text:
                ix_found = row

        msg    = ( f"find_row_with_text {ix_found = }")
        self.append_msg( msg )

        return ix_found

    # ------------------------
    def find_row_with_text_in_column(self, ):
        """
        not used? in error
        might be faster
        might be wrong depending on how matching works
        from chat
        may be ok not yet tested
        """
        msg         = ( "find_row_with_text_in_column !! fix me " )
        self.append_msg( msg )

        table       = self.table_model

        # ix_col_searched     = 2
        # ix_found            = None
        # target_text     = "xyz"

        # matching_items = table.findItems( target_text, QtCore.Qt.MatchExactly)
        # for item in matching_items:
        #     if item.column() == column:
        #         ix_found            =  item.row()

        # print( f"find_row_with_text {ix_found = }")

        # return ix_found

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        self_table_model    = self.table_model
        self_table_view     = self.table_view

        wat_inspector.go(
             msg            = "tbd add more locals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof



