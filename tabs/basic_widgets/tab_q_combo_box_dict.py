#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY_WORDS:      combo box model dict dictionary key value set reset ddl
CLASS_NAME:     QComboBoxDictTab
WIDGETS:        QComboBox, QAbstractListModel
STATUS:         works
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
TAB_TITLE:      QComboBox / with Dict Model
DESCRIPTION:    Two QComboBoxes share one dict backed model, the dict is set and reset by methods

This is a variation on tab_q_combo_box_model_2.py.  There the model
data lives in a list of ( key, value ) tuples built in __init__.
Here the data is a plain python dict, and the whole dict can be
swapped by DictListModel.set_dict() or put back by
DictListModel.reset_dict().

The interesting part is what a model reset does to a QComboBox:
the combo loses its current selection ( it goes to row 0 ), so if
you want to keep the user's choice you save the key first and set
the row for that key afterwards.  The mutations below show both.
"""
WIKI_LINK = "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QComboBox-with-Model"

# ---- tof
if __name__ == "__main__":
    # ----- run the full app
    pass
# --------------------

from qtpy.QtCore import QAbstractListModel, QModelIndex, Qt
from qtpy.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

import tab_base
import wat_inspector


# ---- the dicts we play with

NUMBER_DICT     = {
                    1   : "one",
                    2   : "two",
                    3   : "three",
                    4   : "four",
                    5   : "five",
                  }

COLOR_DICT      = {
                    1   : "red",
                    2   : "green",
                    3   : "blue",
                  }

BIG_DICT        = {
                    1   : "uno",
                    2   : "dos",
                    3   : "tres",
                    4   : "cuatro",
                    5   : "cinco",
                    6   : "seis",
                    7   : "siete",
                    8   : "ocho",
                  }


# --------------------------------------------------
class DictListModel( QAbstractListModel ):
    """
    this stores the data, but does not keep current
    selection info

    the data is a dict:  key -> value
        the key   is shown as user data ( KEY_ROLE )
        the value is what the combo box displays

    row order is dict insertion order, python 3.7+ guarantees it
    self._keys is just a row -> key lookup so we do not rebuild
    a key list on every call to data()
    """
    # -----------------------
    def __init__( self, a_dict = None, parent = None ):
        super().__init__( parent )

        self.KEY_ROLE       = Qt.UserRole
        self.VALUE_ROLE     = Qt.UserRole + 1

        if a_dict is None:
            a_dict          = NUMBER_DICT

        self._original_dict = dict( a_dict )   # for reset_dict()
        self._dict          = dict( a_dict )
        self._keys          = list( self._dict.keys() )

    # -----------------------
    def rowCount( self, parent = QModelIndex() ):
        if parent.isValid():
            return 0
        return len( self._keys )

    # -----------------------
    def columnCount( self, parent = QModelIndex() ):
        if parent.isValid():
            return 0
        return 2

    # -----------------------
    def data( self, index, role = Qt.DisplayRole ):
        if not index.isValid():
            return None

        row     = index.row()
        col     = index.column()
        if row < 0 or row >= len( self._keys ):
            return None

        key     = self._keys[ row ]
        value   = self._dict[ key ]

        # For combo rendering, always provide the string value.
        if role in ( Qt.DisplayRole, Qt.EditRole ):
            return value

        # Always provide the key as user data.
        if role == self.KEY_ROLE:
            return key

        if role == self.VALUE_ROLE:
            return value

        if role == Qt.ToolTipRole:
            if col == 0:
                return f"key={key}"
            if col == 1:
                return f"value={value}"

        return None

    # -----------------------
    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "key"
            if section == 1:
                return "value"
        return None

    # ---- set and reset the whole dict

    # -----------------------
    def set_dict( self, a_dict ):
        """
        replace all the data with a new dict

        this is a model reset, every view attached to the model
        throws away what it knew, including a QComboBox current
        index.  save/restore the key yourself if you care.
        """
        self.beginResetModel()
        self._dict      = dict( a_dict )
        self._keys      = list( self._dict.keys() )
        self.endResetModel()

    # -----------------------
    def reset_dict( self ):
        """
        put back the dict the model was built with
        """
        self.set_dict( self._original_dict )

    # -----------------------
    def get_dict( self ):
        """
        a copy, so a caller cannot edit around our back
        """
        return dict( self._dict )

    # ---- smaller changes, no full reset

    # -----------------------
    def set_item( self, key, value ):
        """
        add a key at the end, or change the value of a key
        we already have -- like dict[ key ] = value
        """
        if key in self._dict:
            self._dict[ key ]   = value
            row                 = self.row_for_key( key )
            index               = self.index( row, 0 )
            self.dataChanged.emit( index, index )
            return

        insert_row  = len( self._keys )
        self.beginInsertRows( QModelIndex(), insert_row, insert_row )
        self._dict[ key ]   = value
        self._keys.append( key )
        self.endInsertRows()

    # -----------------------
    def remove_key( self, key ):
        """
        drop one key, returns True if there was one to drop
        """
        row     = self.row_for_key( key )
        if row < 0:
            return False

        self.beginRemoveRows( QModelIndex(), row, row )
        del self._dict[ key ]
        del self._keys[ row ]
        self.endRemoveRows()
        return True

    # ---- lookups

    # -----------------------
    def row_for_key( self, target_key ):
        """
        -1 when we do not have the key, which is also what
        QComboBox.setCurrentIndex() wants for "nothing selected"
        """
        for ix, i_key in enumerate( self._keys ):
            if i_key == target_key:
                return ix
        return -1

    # -----------------------
    def key_for_row( self, row ):
        if row < 0 or row >= len( self._keys ):
            return None
        return self._keys[ row ]


# ------------------------
class QComboBoxDictTab( tab_base.TabBase ):
    def __init__( self ):
        super().__init__()

        self.module_file    = __file__
        self.wiki_link      = WIKI_LINK

        self.mutate_dict[0] = self.mutate_0
        self.mutate_dict[1] = self.mutate_1
        self.mutate_dict[2] = self.mutate_2
        self.mutate_dict[3] = self.mutate_3
        self.mutate_dict[4] = self.mutate_4
        self._build_gui()

    # ----------------------------------------------
    def _build_gui_widgets( self, main_layout ):
        layout      = QVBoxLayout()
        main_layout.addLayout( layout )

        # ---- combo with dict model
        sub_layout  = QHBoxLayout()
        layout.addLayout( sub_layout )

        label       = QLabel( "combo_box ->" )
        sub_layout.addWidget( label )

        self.combo_box      = QComboBox()
        self.dict_model     = DictListModel( NUMBER_DICT, self )
        self.combo_box.setModel( self.dict_model )
        # With QAbstractListModel descendants, use column 0 for combo stability.
        self.combo_box.setModelColumn( 0 )
        self.combo_box.setSizeAdjustPolicy( QComboBox.AdjustToContents )
        self.combo_box.setMaxVisibleItems( 10 )
        self.combo_box.currentIndexChanged.connect( self.combo_changed )
        self.combo_box.setCurrentIndex( 0 )
        self.combo_box.setMinimumWidth( 320 )
        self.combo_box.setMinimumHeight( 32 )
        self.combo_box.view().setMinimumWidth( 320 )
        self.combo_box.view().setMinimumHeight( 120 )
        sub_layout.addWidget( self.combo_box )

        # ---- second combo: same model, independent current index
        sub_layout_2    = QHBoxLayout()
        layout.addLayout( sub_layout_2 )

        label_2         = QLabel( "combo_box_2 ->" )
        sub_layout_2.addWidget( label_2 )

        self.combo_box_2    = QComboBox()
        self.combo_box_2.setModel( self.dict_model )
        self.combo_box_2.setModelColumn( 0 )
        self.combo_box_2.setSizeAdjustPolicy( QComboBox.AdjustToContents )
        self.combo_box_2.setMaxVisibleItems( 10 )
        self.combo_box_2.currentIndexChanged.connect( self.combo_changed )
        row_five        = self.dict_model.row_for_key( 5 )
        self.combo_box_2.setCurrentIndex( row_five )
        self.combo_box_2.setMinimumWidth( 320 )
        self.combo_box_2.setMinimumHeight( 32 )
        self.combo_box_2.view().setMinimumWidth( 320 )
        self.combo_box_2.view().setMinimumHeight( 120 )
        sub_layout_2.addWidget( self.combo_box_2 )

        # ---- button
        button_layout   = QHBoxLayout()
        layout.addLayout( button_layout )

        widget          = QPushButton( "show\nselection" )
        widget.clicked.connect( self.show_selection )
        button_layout.addWidget( widget )

        widget          = QPushButton( "show\ndict" )
        widget.clicked.connect( self.show_dict )
        button_layout.addWidget( widget )

        self.build_gui_last_buttons( button_layout )

    # -----------------------
    def combo_changed( self, _arg ):
        """
        linked to both combo boxes, set so can not
        write to non-created msg_widget
        """
        if self.msg_widget is None:
            pass
        else:
            self.show_selection()

    # -----------------------
    def show_selection( self ):
        """
        what both combo boxes think is selected right now
        """
        key     = self.combo_box.currentData( self.dict_model.KEY_ROLE )
        text    = self.combo_box.currentText()
        self.append_msg(
            f"show_selection()  combo_box:   currentText={text!r} currentData(KEY_ROLE)={key!r}"
        )

        key_2   = self.combo_box_2.currentData( self.dict_model.KEY_ROLE )
        text_2  = self.combo_box_2.currentText()
        self.append_msg(
            f"show_selection()  combo_box_2: currentText={text_2!r} currentData(KEY_ROLE)={key_2!r}"
        )

    # -----------------------
    def show_dict( self ):
        """
        the dict currently inside the model
        """
        a_dict  = self.dict_model.get_dict()
        msg     = ( f"show_dict()  rowCount={self.dict_model.rowCount()}  {a_dict = }" )
        self.append_msg( msg )

    # -----------------------
    def save_keys( self ):
        """
        the selected key of each combo, so we can put the
        selection back after a model reset
        """
        key     = self.combo_box.currentData(   self.dict_model.KEY_ROLE )
        key_2   = self.combo_box_2.currentData( self.dict_model.KEY_ROLE )
        return ( key, key_2 )

    # -----------------------
    def restore_keys( self, keys ):
        """
        set each combo to the row holding its old key
        a key that is gone gives row -1 -> nothing selected
        """
        key, key_2  = keys

        self.combo_box.setCurrentIndex(   self.dict_model.row_for_key( key   ) )
        self.combo_box_2.setCurrentIndex( self.dict_model.row_for_key( key_2 ) )

    # ------------------------------------
    def mutate_0( self ):
        """
        a mutation... read

        back to where we started, this is also run once
        as the tab is built
        """
        self.append_function_msg( "mutate_0()" )

        msg    = ( "reset_dict() then box 1 -> key 1, box 2 -> key 5\n" )
        self.append_msg( msg )

        self.dict_model.reset_dict()

        self.combo_box.setCurrentIndex(   self.dict_model.row_for_key( 1 ) )
        self.combo_box_2.setCurrentIndex( self.dict_model.row_for_key( 5 ) )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        a mutation... read

        change one value in place, no model reset, so both
        combos keep their selection
        """
        self.append_function_msg( "mutate_1()" )

        msg    = ( "set_item( 3, 'THREE changed' ) -- key already in dict\n"
                   "this is a dataChanged, not a reset, selections survive\n" )
        self.append_msg( msg )

        self.dict_model.set_item( 3, "THREE changed" )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        a mutation... read

        a new dict, selections NOT saved, watch them go
        """
        self.append_function_msg( "mutate_2()" )

        msg    = ( "set_dict( COLOR_DICT ) with no save of the keys\n"
                   "a model reset, both combos drop back to row 0\n" )
        self.append_msg( msg )

        self.dict_model.set_dict( COLOR_DICT )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        a mutation... read

        a new dict, this time keep the selection by key
        """
        self.append_function_msg( "mutate_3()" )

        msg    = ( "set_dict( BIG_DICT ) with save/restore of the keys\n"
                   "same keys, new values, so the selected key survives\n" )
        self.append_msg( msg )

        # mutate_2 left both combos on row 0, spread them out again
        # so the restore below is worth looking at
        self.combo_box.setCurrentIndex(   self.dict_model.row_for_key( 2 ) )
        self.combo_box_2.setCurrentIndex( self.dict_model.row_for_key( 3 ) )

        keys    = self.save_keys()
        self.dict_model.set_dict( BIG_DICT )
        self.restore_keys( keys )

        self.append_msg( f"saved keys were {keys}" )
        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        a mutation... read

        the empty dict, an edge case worth seeing once
        """
        self.append_function_msg( "mutate_4()" )

        msg    = ( "set_dict( {} ) -- an empty model\n"
                   "currentText is '' and currentData is None\n"
                   "mutate again to get back to mutate_0\n" )
        self.append_msg( msg )

        self.dict_model.set_dict( {} )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect( self ):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them

        self_dict_model     = self.dict_model
        self_combo_box      = self.combo_box
        self_combo_box_2    = self.combo_box_2

        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint( self ):
        """
        each tab gets its own function so we break in that
        tab's code

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )


# ---- eof
