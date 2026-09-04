#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY_WORDS:      combo box model dict dictionary display keys subclass custom widget
CLASS_NAME:     CQComboBoxDictTab
WIDGETS:        QComboBox, QAbstractListModel, CQComboBoxDict
STATUS:         works
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
TAB_TITLE:      CQComboBoxDict / dict model in the widget
DESCRIPTION:    A QComboBox subclass that owns its dict model and can display keys or values

This follows on from tab_q_combo_box_dict.py.  Two changes:

1.  the model can show the KEY in the drop down instead of the
    value.  set_display_keys( True/False ) flips it, the selection
    is not lost because it is a dataChanged not a model reset.

2.  the model lives inside a QComboBox subclass, CQComboBoxDict.
    The caller never touches setModel(), never converts a key to a
    row, and never has to remember to save the selected key across
    a set_dict().  Compare:

        # tab_q_combo_box_dict.py, model outside the widget
        keys = self.save_keys()
        self.dict_model.set_dict( BIG_DICT )
        self.restore_keys( keys )

        # here, model inside the widget
        self.combo_box.set_dict( BIG_DICT )

    The price is that the model is no longer shareable.  In
    tab_q_combo_box_dict.py both combo boxes ran off one model,
    here each CQComboBoxDict has its own, which is why mutate_2
    changes one combo box and leaves the other alone.
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
class DictKeyListModel( QAbstractListModel ):
    """
    this stores the data, but does not keep current
    selection info

    the data is a dict:  key -> value

    display_keys True    the drop down shows str( key )
    display_keys False   the drop down shows the value

    either way KEY_ROLE gives the key and VALUE_ROLE the value,
    so what is displayed and what you read back are independent

    row order is dict insertion order, python 3.7+ guarantees it
    self._keys is just a row -> key lookup so we do not rebuild
    a key list on every call to data()
    """
    # -----------------------
    def __init__( self, a_dict = None, display_keys = True, parent = None ):
        super().__init__( parent )

        self.KEY_ROLE       = Qt.UserRole
        self.VALUE_ROLE     = Qt.UserRole + 1

        if a_dict is None:
            a_dict          = NUMBER_DICT

        self._original_dict = dict( a_dict )   # for reset_dict()
        self._dict          = dict( a_dict )
        self._keys          = list( self._dict.keys() )
        self._display_keys  = display_keys

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

        # the display, key or value depending on the flag
        # str() because a key may be an int and a view wants text
        if role in ( Qt.DisplayRole, Qt.EditRole ):
            if self._display_keys:
                return str( key )
            return value

        # both are always available, whatever is on display
        if role == self.KEY_ROLE:
            return key

        if role == self.VALUE_ROLE:
            return value

        if role == Qt.ToolTipRole:
            if col == 0:
                return f"key={key}  value={value}"
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

    # ---- what gets displayed

    # -----------------------
    def set_display_keys( self, display_keys ):
        """
        show keys or show values

        only the DisplayRole changes, no row comes or goes, so this
        is a dataChanged over every row and NOT a model reset --
        which is why the combo box keeps its selection
        """
        if display_keys == self._display_keys:
            return

        self._display_keys  = display_keys

        last_row    = len( self._keys ) - 1
        if last_row < 0:
            return

        self.dataChanged.emit( self.index( 0, 0 ),
                               self.index( last_row, 0 ) )

    # -----------------------
    def get_display_keys( self ):
        return self._display_keys

    # ---- set and reset the whole dict

    # -----------------------
    def set_dict( self, a_dict ):
        """
        replace all the data with a new dict

        this is a model reset, every view attached to the model
        throws away what it knew, including a QComboBox current
        index.  CQComboBoxDict.set_dict() puts the selection back.
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


# --------------------------------------------------
class CQComboBoxDict( QComboBox ):
    """
    a QComboBox that builds and owns its own DictKeyListModel

    the whole api is in keys and dicts, rows never leave this class

        combo   = CQComboBoxDict( NUMBER_DICT )
        combo.set_current_key( 3 )
        combo.set_dict( COLOR_DICT )    # selection kept if key survives
        combo.current_key()             # 3
        combo.current_value()           # "blue"

    the model is reachable as combo.dict_model if you need the raw
    thing, but you should not need it
    """
    # -----------------------
    def __init__( self, a_dict = None, display_keys = True, parent = None ):
        super().__init__( parent )

        self.dict_model     = DictKeyListModel( a_dict,
                                                display_keys = display_keys,
                                                parent       = self )
        self.setModel( self.dict_model )
        # With QAbstractListModel descendants, use column 0 for combo stability.
        self.setModelColumn( 0 )
        self.setSizeAdjustPolicy( QComboBox.AdjustToContents )
        self.setMaxVisibleItems( 10 )
        self.setMinimumWidth( 320 )
        self.setMinimumHeight( 32 )
        self.view().setMinimumWidth( 320 )
        self.view().setMinimumHeight( 120 )

    # ---- selection, in keys not rows

    # -----------------------
    def current_key( self ):
        """
        None when nothing is selected, empty model for instance
        """
        return self.currentData( self.dict_model.KEY_ROLE )

    # -----------------------
    def current_value( self ):
        """
        the value even when the key is what is on display
        """
        return self.currentData( self.dict_model.VALUE_ROLE )

    # -----------------------
    def set_current_key( self, key ):
        """
        select the row holding key, returns True if we found it
        a key we do not have leaves the combo box with nothing
        selected, index -1
        """
        row     = self.dict_model.row_for_key( key )
        self.setCurrentIndex( row )
        return row >= 0

    # ---- the dict, pass through to the model

    # -----------------------
    def set_dict( self, a_dict, keep_key = True ):
        """
        new data for the combo box

        keep_key True   remember the selected key over the model
                        reset and select it again if the new dict
                        still has it
        keep_key False  take what the reset leaves us, row 0

        this is the reason for the subclass, the caller does not
        have to remember to do the save and restore
        """
        old_key     = self.current_key()

        self.dict_model.set_dict( a_dict )

        if keep_key and ( old_key is not None ):
            self.set_current_key( old_key )

    # -----------------------
    def reset_dict( self, keep_key = True ):
        """
        put back the dict we were built with
        """
        old_key     = self.current_key()

        self.dict_model.reset_dict()

        if keep_key and ( old_key is not None ):
            self.set_current_key( old_key )

    # -----------------------
    def get_dict( self ):
        return self.dict_model.get_dict()

    # -----------------------
    def set_item( self, key, value ):
        """
        no selection juggling needed, an insert or a dataChanged
        does not disturb the current row
        """
        self.dict_model.set_item( key, value )

    # -----------------------
    def remove_key( self, key ):
        return self.dict_model.remove_key( key )

    # ---- display

    # -----------------------
    def set_display_keys( self, display_keys ):
        """
        show the keys in the drop down, or the values
        """
        self.dict_model.set_display_keys( display_keys )

    # -----------------------
    def get_display_keys( self ):
        return self.dict_model.get_display_keys()

    # -----------------------
    def toggle_display_keys( self ):
        """
        handy for a button, returns the new setting
        """
        display_keys    = not self.dict_model.get_display_keys()
        self.set_display_keys( display_keys )
        return display_keys


# ------------------------
class CQComboBoxDictTab( tab_base.TabBase ):
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

        # ---- combo one, keys on display
        sub_layout  = QHBoxLayout()
        layout.addLayout( sub_layout )

        label       = QLabel( "combo_box ( shows keys ) ->" )
        sub_layout.addWidget( label )

        self.combo_box  = CQComboBoxDict( NUMBER_DICT, display_keys = True )
        self.combo_box.currentIndexChanged.connect( self.combo_changed )
        self.combo_box.set_current_key( 1 )
        sub_layout.addWidget( self.combo_box )

        # ---- combo two, its own model, values on display
        sub_layout_2    = QHBoxLayout()
        layout.addLayout( sub_layout_2 )

        label_2         = QLabel( "combo_box_2 ( shows values ) ->" )
        sub_layout_2.addWidget( label_2 )

        self.combo_box_2    = CQComboBoxDict( NUMBER_DICT, display_keys = False )
        self.combo_box_2.currentIndexChanged.connect( self.combo_changed )
        self.combo_box_2.set_current_key( 5 )
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

        widget          = QPushButton( "toggle\nkey/value" )
        widget.clicked.connect( self.toggle_display )
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

        note currentText() is whatever is on display, while
        current_key() and current_value() do not care
        """
        combo   = self.combo_box
        self.append_msg(
            f"show_selection()  combo_box:   currentText={combo.currentText()!r} "
            f"current_key()={combo.current_key()!r} current_value()={combo.current_value()!r} "
            f"display_keys={combo.get_display_keys()}"
        )

        combo   = self.combo_box_2
        self.append_msg(
            f"show_selection()  combo_box_2: currentText={combo.currentText()!r} "
            f"current_key()={combo.current_key()!r} current_value()={combo.current_value()!r} "
            f"display_keys={combo.get_display_keys()}"
        )

    # -----------------------
    def show_dict( self ):
        """
        the dict inside each combo box, they are not the same object
        """
        self.append_msg( f"show_dict()  combo_box:   {self.combo_box.get_dict() = }" )
        self.append_msg( f"show_dict()  combo_box_2: {self.combo_box_2.get_dict() = }" )

    # -----------------------
    def toggle_display( self ):
        """
        the button, flips both combo boxes
        """
        self.append_function_msg( "toggle_display()" )

        display_keys    = self.combo_box.toggle_display_keys()
        self.combo_box_2.toggle_display_keys()

        self.append_msg( f"combo_box now showing {'keys' if display_keys else 'values'}, "
                          "and the selection did not move" )
        self.show_selection()

    # ------------------------------------
    def mutate_0( self ):
        """
        a mutation... read

        back to where we started, this is also run once
        as the tab is built
        """
        self.append_function_msg( "mutate_0()" )

        msg    = ( "reset_dict() on both, box 1 shows keys, box 2 shows values\n"
                   "box 1 -> key 1, box 2 -> key 5\n" )
        self.append_msg( msg )

        self.combo_box.reset_dict( keep_key = False )
        self.combo_box_2.reset_dict( keep_key = False )

        self.combo_box.set_display_keys( True )
        self.combo_box_2.set_display_keys( False )

        self.combo_box.set_current_key( 1 )
        self.combo_box_2.set_current_key( 5 )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        a mutation... read

        swap what is on display, nothing else moves
        """
        self.append_function_msg( "mutate_1()" )

        msg    = ( "set_display_keys() the other way round on both boxes\n"
                   "a dataChanged not a reset, so the selected key stays put\n"
                   "watch currentText change while current_key does not\n" )
        self.append_msg( msg )

        self.combo_box.set_display_keys( False )
        self.combo_box_2.set_display_keys( True )

        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        a mutation... read

        a new dict for box 1 only, the models are separate
        """
        self.append_function_msg( "mutate_2()" )

        msg    = ( "combo_box.set_dict( COLOR_DICT, keep_key = False )\n"
                   "keep_key False so the reset drops us on row 0\n"
                   "combo_box_2 has its own model and does not notice\n" )
        self.append_msg( msg )

        self.combo_box.set_dict( COLOR_DICT, keep_key = False )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        a mutation... read

        a new dict for box 1, this time the widget keeps the key
        """
        self.append_function_msg( "mutate_3()" )

        msg    = ( "combo_box.set_dict( BIG_DICT ) with the default keep_key = True\n"
                   "no save/restore in this code, the widget does it\n" )
        self.append_msg( msg )

        self.combo_box.set_current_key( 3 )
        self.append_msg( f"before the swap current_key() = {self.combo_box.current_key()!r}" )

        self.combo_box.set_dict( BIG_DICT )

        self.show_dict()
        self.show_selection()

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        a mutation... read

        edits that are not a whole new dict
        """
        self.append_function_msg( "mutate_4()" )

        msg    = ( "set_item( 9, 'nueve' ) new key, appended\n"
                   "set_item( 1, 'UNO changed' ) key we have, value changed\n"
                   "remove_key( 2 ) gone\n"
                   "none of these is a reset, the selection rides through\n" )
        self.append_msg( msg )

        self.combo_box.set_current_key( 3 )

        self.combo_box.set_item( 9, "nueve" )
        self.combo_box.set_item( 1, "UNO changed" )
        self.append_msg( f"remove_key( 2 ) -> {self.combo_box.remove_key( 2 )}" )
        self.append_msg( f"remove_key( 99 ) -> {self.combo_box.remove_key( 99 )}" )

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

        self_combo_box      = self.combo_box
        self_combo_box_2    = self.combo_box_2
        self_dict_model     = self.combo_box.dict_model

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
