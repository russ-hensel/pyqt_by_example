#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_q_tree_view_widget.py
self.help_file_name     =  "q_tree_view_widget_tab.txt"

KEY_WORDS:      tree view hierarchy model QStandardItemModel expand collapse levels nodes children treeview qtree
CLASS_NAME:     QTreeViewTab
WIDGETS:        QTreeView QStandardItemModel QStandardItem
STATUS:         new   !! review_key_words   !! review_help_0_10
TAB_TITLE:      QTreeView / A Tree
DESCRIPTION:    QTreeView Reference
HOW_COMPLETE:   30  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/QTreeView Reference"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


from qtpy.QtCore import (Qt)
from qtpy.QtGui import (
                         QStandardItem,
                         QStandardItemModel,
                         )
from qtpy.QtWidgets import (
                             QAbstractItemView,
                             QHBoxLayout,
                             QHeaderView,
                             QPushButton,
                             QTreeView,
                             QVBoxLayout
                             )


import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports


INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2


# ---- tree data
# four levels:  region -> country -> city -> site
# each leaf is ( name, info )
TREE_DATA   = {
    "Europe": {
        "France":   {
            "Paris":     [ ( "Louvre",            "museum"   ),
                           ( "Eiffel Tower",      "landmark" ),
                           ( "Notre-Dame",        "church"   ), ],
            "Lyon":      [ ( "Vieux Lyon",        "district" ),
                           ( "Fourviere",         "church"   ), ],
        },
        "Italy":    {
            "Rome":      [ ( "Colosseum",         "landmark" ),
                           ( "Pantheon",          "temple"   ), ],
            "Florence":  [ ( "Uffizi",            "museum"   ),
                           ( "Duomo",             "church"   ), ],
        },
    },
    "North America": {
        "USA":      {
            "Boston":    [ ( "Fenway Park",       "stadium"  ),
                           ( "Freedom Trail",     "walk"     ),
                           ( "MIT Museum",        "museum"   ), ],
            "Chicago":   [ ( "Art Institute",     "museum"   ),
                           ( "Millennium Park",   "park"     ), ],
        },
        "Canada":   {
            "Toronto":   [ ( "CN Tower",          "landmark" ),
                           ( "Royal Ontario Museum", "museum" ), ],
            "Montreal":  [ ( "Old Port",          "district" ),
                           ( "Mount Royal",       "park"     ), ],
        },
    },
    "Asia": {
        "Japan":    {
            "Tokyo":     [ ( "Senso-ji",          "temple"   ),
                           ( "Tokyo Tower",       "landmark" ), ],
            "Kyoto":     [ ( "Kinkaku-ji",        "temple"   ),
                           ( "Fushimi Inari",     "shrine"   ), ],
        },
    },
}

LEVEL_NAMES     = [ "region", "country", "city", "site" ]


#-----------------------------------------------
class QTreeViewTab( tab_base.TabBase  ):
    """
    here build a tab in its own class to hide its variables
    """
    def __init__(self, ):
        """
        """
        super().__init__( )

        self.module_file        = __file__      # save for help file usage

        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        self.mutate_dict[4]     = self.mutate_4

        self.add_count          = 0

        self.help_file_name     =  "q_tree_view_widget_tab.txt"
        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )

        # ---- model
        model               = QStandardItemModel( )
        self.model          = model
        model.setHorizontalHeaderLabels( [ "Name", "Level", "Info" ] )
        self.populate_model()

        # ---- view
        tree_view           = QTreeView( )
        self.tree_view      = tree_view
        tree_view.setModel( model )
        layout.addWidget( tree_view )

        tree_view.setSelectionBehavior( QAbstractItemView.SelectRows )
        tree_view.setSelectionMode( QAbstractItemView.SingleSelection )
        tree_view.setAlternatingRowColors( True )
        tree_view.setSortingEnabled( True )
        tree_view.sortByColumn( 0, Qt.AscendingOrder )  # else sort on open is odd
        tree_view.setColumnWidth( 0, 250 )

        tree_view.clicked.connect(  self.on_clicked  )
        tree_view.expanded.connect( self.on_expanded )

        tree_view.expandToDepth( 0 )   # 0 based, show countries

        # ---- buttons
        button_layout = QHBoxLayout()
        layout.addLayout( button_layout )

        a_widget           = QPushButton( "expand\n_all" )
        a_widget.clicked.connect( self.expand_all )
        button_layout.addWidget( a_widget )

        a_widget           = QPushButton( "collapse\n_all" )
        a_widget.clicked.connect( self.collapse_all )
        button_layout.addWidget( a_widget )

        a_widget           = QPushButton( "expand_to\n_depth_1" )
        a_widget.clicked.connect( self.expand_to_depth_1 )
        button_layout.addWidget( a_widget )

        a_widget           = QPushButton( "add_child\n_to_current" )
        a_widget.clicked.connect( self.add_child_to_current )
        button_layout.addWidget( a_widget )

        a_widget           = QPushButton( "remove\n_current" )
        a_widget.clicked.connect( self.remove_current )
        button_layout.addWidget( a_widget )

        a_widget           = QPushButton( "count\n_rows" )
        a_widget.clicked.connect( self.count_rows )
        button_layout.addWidget( a_widget )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # -------------------------------------
    def make_row( self, name, level, info = "" ):
        """
        a row in a tree is a list of items, one per column
        the children hang off the first item
        """
        name_item       = QStandardItem( name )
        level_item      = QStandardItem( LEVEL_NAMES[ level ] )
        info_item       = QStandardItem( info )

        # keep the level as data, not just text
        name_item.setData( level, Qt.UserRole )

        # level and info are not editable, name is
        level_item.setEditable( False )
        info_item.setEditable( False )

        return [ name_item, level_item, info_item ]

    # -------------------------------------
    def populate_model( self ):
        """
        Populate the model from TREE_DATA, four levels deep
        """
        model           = self.model
        root            = model.invisibleRootItem()

        for i_region, countries in TREE_DATA.items():
            region_row      = self.make_row( i_region, 0, f"{len( countries )} countries" )
            root.appendRow( region_row )

            for i_country, cities in countries.items():
                country_row     = self.make_row( i_country, 1, f"{len( cities )} cities" )
                region_row[0].appendRow( country_row )

                for i_city, sites in cities.items():
                    city_row        = self.make_row( i_city, 2, f"{len( sites )} sites" )
                    country_row[0].appendRow( city_row )

                    for i_site, i_info in sites:
                        site_row        = self.make_row( i_site, 3, i_info )
                        city_row[0].appendRow( site_row )

    # -------------------------------------
    def count_items( self, parent_item ):
        """
        recursive count of all items ( rows ) below parent_item
        """
        count   = 0
        for ix_row in range( parent_item.rowCount() ):
            child   = parent_item.child( ix_row, 0 )
            count  += 1 + self.count_items( child )

        return count

    # -------------------------------------
    def item_path( self, index ):
        """
        walk up the parents to make a path string like
        Europe / France / Paris / Louvre
        """
        names   = []
        while index.isValid():
            names.append( index.siblingAtColumn( 0 ).data() )
            index   = index.parent()

        return " / ".join( reversed( names ) )

    # ------------------------------
    def on_clicked( self, index ):
        """
        index is a QModelIndex, may be any column
        """
        self.append_function_msg( "on_clicked" )

        name_index  = index.siblingAtColumn( 0 )
        level       = name_index.data( Qt.UserRole )

        msg     = ( f"row {index.row()} col {index.column()} data: {index.data()}" )
        self.append_msg( msg )

        msg     = ( f"level {level} ( {LEVEL_NAMES[ level ]} )  "
                    f"has children {self.model.hasChildren( name_index )}" )
        self.append_msg( msg )

        msg     = ( f"path: {self.item_path( index )}" )
        self.append_msg( msg )

    # ------------------------------
    def on_expanded( self, index ):
        """
        signal fires for each node expanded
        """
        print( f"on_expanded {self.item_path( index )}" )

    # ------------------------------
    def expand_all( self ):
        """
        what it says
        """
        self.append_function_msg( "expand_all" )

        self.tree_view.expandAll()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------
    def collapse_all( self ):
        """
        what it says
        """
        self.append_function_msg( "collapse_all" )

        self.tree_view.collapseAll()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------
    def expand_to_depth_1( self ):
        """
        depth is 0 based, so 1 shows cities
        """
        self.append_function_msg( "expand_to_depth_1" )

        tree_view   = self.tree_view
        tree_view.collapseAll()
        tree_view.expandToDepth( 1 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------
    def add_child_to_current( self ):
        """
        add a child row under the current item, one level down
        sites are the bottom level, so add a sibling there
        """
        self.append_function_msg( "add_child_to_current" )

        tree_view   = self.tree_view
        model       = self.model
        index       = tree_view.currentIndex()

        if not index.isValid():
            self.append_msg( "nothing current, click a row first" )
            return

        name_index  = index.siblingAtColumn( 0 )
        parent_item = model.itemFromIndex( name_index )
        level       = name_index.data( Qt.UserRole )

        if level >= len( LEVEL_NAMES ) - 1:
            self.append_msg( "already at bottom level, adding a sibling" )
            parent_item = parent_item.parent()
            level       = level - 1

        self.add_count += 1
        new_row         = self.make_row( f"new {LEVEL_NAMES[ level + 1 ]} {self.add_count}",
                                         level + 1,
                                         "added" )
        parent_item.appendRow( new_row )

        new_index       = new_row[0].index()
        tree_view.expand( new_index.parent() )
        tree_view.setCurrentIndex( new_index )
        tree_view.scrollTo( new_index )

        msg     = ( f"added: {self.item_path( new_index )}" )
        self.append_msg( msg )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------
    def remove_current( self ):
        """
        removes the row and all of its children
        """
        self.append_function_msg( "remove_current" )

        index       = self.tree_view.currentIndex()

        if not index.isValid():
            self.append_msg( "nothing current, click a row first" )
            return

        msg     = ( f"removing: {self.item_path( index )}" )
        self.append_msg( msg )

        self.model.removeRow( index.row(), index.parent() )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------
    def count_rows( self ):
        """
        rowCount() only counts direct children, so recurse
        """
        self.append_function_msg( "count_rows" )

        model       = self.model
        root        = model.invisibleRootItem()

        msg     = ( f"top level rows {model.rowCount()}" )
        self.append_msg( msg )

        msg     = ( f"all rows {self.count_items( root )}" )
        self.append_msg( msg )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg     = "expand all, select a site deep in the tree"
        self.append_msg( msg, )

        tree_view   = self.tree_view
        model       = self.model
        tree_view.expandAll()

        matches     = model.findItems( "Colosseum", Qt.MatchExactly | Qt.MatchRecursive, 0 )
        if matches:
            index       = matches[0].index()
            tree_view.setCurrentIndex( index )
            tree_view.scrollTo( index )
            msg         = ( f"found: {self.item_path( index )}" )
            self.append_msg( msg )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg     = "hide the Level column, sort descending, hide one row"
        self.append_msg( msg, )

        tree_view   = self.tree_view
        tree_view.hideColumn( 1 )
        tree_view.sortByColumn( 0, Qt.DescendingOrder )

        # hide a row: row number and its parent index
        tree_view.setRowHidden( 0, self.model.index( 0, 0 ), True )

        self.append_msg( tab_base.DONE_MSG )

    #----------------------------
    def mutate_2( self  ):
        """
        read it -- undo mutate_1
        """
        self.append_function_msg( "mutate_2" )

        msg     = "show the Level column, sort ascending, show all rows"
        self.append_msg( msg, )

        tree_view   = self.tree_view
        model       = self.model
        tree_view.showColumn( 1 )
        tree_view.sortByColumn( 0, Qt.AscendingOrder )

        for ix_row in range( model.rowCount() ):
            parent_index    = model.index( ix_row, 0 )
            for ix_child in range( model.rowCount( parent_index ) ):
                tree_view.setRowHidden( ix_child, parent_index, False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- header and look
        """
        self.append_function_msg( "mutate_3" )

        msg     = "header resize modes, indentation, no root decoration"
        self.append_msg( msg, )

        tree_view   = self.tree_view
        header      = tree_view.header()
        header.setSectionResizeMode( 0, QHeaderView.ResizeToContents )
        header.setSectionResizeMode( 1, QHeaderView.Interactive )
        header.setStretchLastSection( True )

        tree_view.setIndentation( 40 )
        tree_view.setRootIsDecorated( False )
        tree_view.setAnimated( True )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- undo mutate_3, and rebuild the model
        """
        self.append_function_msg( "mutate_4" )

        msg     = "restore look, clear and repopulate the model"
        self.append_msg( msg, )

        tree_view   = self.tree_view
        model       = self.model
        header      = tree_view.header()
        header.setSectionResizeMode( 0, QHeaderView.Interactive )
        tree_view.setColumnWidth( 0, 250 )
        tree_view.setIndentation( 20 )
        tree_view.setRootIsDecorated( True )

        # clear() also drops the header labels
        model.clear()
        model.setHorizontalHeaderLabels( [ "Name", "Level", "Info" ] )
        self.populate_model()
        tree_view.expandToDepth( 0 )

        msg     = ( f"all rows {self.count_items( model.invisibleRootItem() )}" )
        self.append_msg( msg )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection
        self_tree_view      = self.tree_view
        self_model          = self.model

        wat_inspector.go(
             msg            = "inspect...",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg(  tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        the usual
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg(  tab_base.DONE_MSG )

# ---- eof
