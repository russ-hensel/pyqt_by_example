#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY_WORDS:      combo box model key value q qcombo
CLASS_NAME:     QComboBoxModelTab
WIDGETS:        QComboBox, QAbstractListModel
STATUS:         works
TAB_TITLE:      QComboBox / Model
DESCRIPTION:    A QComboBox backed by a 2-column key/value model

What We Know About QComboBox with Model · russ-hensel/pyqt_by_example Wiki
https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QComboBox-with-Model



"""
WIKI_LINK = "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QComboBox-with-Model"

# ---- tof
if __name__ == "__main__":
    # ----- run the full app
    import main
# --------------------

from qtpy.QtCore import QAbstractListModel, QModelIndex, Qt
from qtpy.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

import tab_base
import utils_for_tabs as uft
import wat_inspector
import tab_base


# --------------------------------------------------
class KeyValueListModel(QAbstractListModel):
    """
    A small 2-column model:
    column 0 = key (int)
    column 1 = value (str)
    """
    # -----------------------
    def __init__(self, parent=None):
        super().__init__(parent)
        self.KEY_ROLE = Qt.UserRole
        self.VALUE_ROLE = Qt.UserRole + 1
        self._rows = [
            (1, "one"),
            (2, "two"),
            (3, "three"),
            (4, "four"),
            (5, "five"),
        ]

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 2

    # -----------------------
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._rows):
            return None

        key, value = self._rows[row]

        # For combo rendering, always provide the string value.
        if role in (Qt.DisplayRole, Qt.EditRole):
            return value

        # Always provide the integer key as user data.
        if role == self.KEY_ROLE:
            return key

        if role == self.VALUE_ROLE:
            return value

        # Optional: if a caller asks for "column-like" values by display role,
        # still allow access to both fields by QModelIndex column.
        if role == Qt.ToolTipRole:
            if col == 0:
                return f"key={key}"
            if col == 1:
                return f"value={value}"

        return None

    # -----------------------
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "key"
            if section == 1:
                return "value"
        return None

    # -----------------------
    def row_for_key(self, target_key):
        for row, (key, _value) in enumerate(self._rows):
            if key == target_key:
                return row
        return -1

    # -----------------------
    def append_row(self, key, value):
        insert_row = len(self._rows)
        self.beginInsertRows(QModelIndex(), insert_row, insert_row)
        self._rows.append((key, value))
        self.endInsertRows()

    # -----------------------
    def prepend_row(self, key, value):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._rows.insert(0, (key, value))
        self.endInsertRows()

    # -----------------------
class QComboBoxModelTab(tab_base.TabBase):
    def __init__(self):
        super().__init__()

        self.module_file = __file__
        self.wiki_link = WIKI_LINK

        self.mutate_dict[0] = self.mutate_0
        self.mutate_dict[1] = self.mutate_1
        self.mutate_dict[2] = self.mutate_2
        self.mutate_dict[3] = self.mutate_3
        self.mutate_dict[4] = self.mutate_4
        self._build_gui()

    # ----------------------------------------------
    def _build_gui_widgets(self, main_layout):
        layout = QVBoxLayout()
        main_layout.addLayout(layout)

        # ---- combo with model
        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        label = QLabel("combo_model ->")
        sub_layout.addWidget(label)

        self.combo_model = QComboBox()
        self.key_value_model = KeyValueListModel(self)
        self.combo_model.setModel(self.key_value_model)
        # With QAbstractListModel descendants, use column 0 for combo stability.
        self.combo_model.setModelColumn(0)
        self.combo_model.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combo_model.setMaxVisibleItems(10)
        self.combo_model.currentIndexChanged.connect(self.combo_changed)
        self.combo_model.setCurrentIndex(0)
        self.combo_model.setMinimumWidth(320)
        self.combo_model.setMinimumHeight(32)
        self.combo_model.view().setMinimumWidth(320)
        self.combo_model.view().setMinimumHeight(120)
        sub_layout.addWidget(self.combo_model)

        # ---- button
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        widget = QPushButton("show\nselection")
        widget.clicked.connect(self.show_selection)
        button_layout.addWidget(widget)

        self.build_gui_last_buttons( button_layout )

    # -----------------------
    def combo_changed(self, _arg):
        self.show_selection()

    # -----------------------
    def show_selection(self):
        key     = self.combo_model.currentData(Qt.UserRole)
        text    = self.combo_model.currentText()
        msg     = f"show_selection()  combo_model: currentText={text!r} currentData(Qt.UserRole)={key!r}"
        self.append_msg(msg)

    # ------------------------------------
    def mutate_0(self):
        self.append_function_msg("mutate_0()")
        row = self.key_value_model.row_for_key(1)
        self.combo_model.setCurrentIndex(row)
        self.show_selection()
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def mutate_1( self):
        self.append_function_msg("mutate_1()")
        row = self.key_value_model.row_for_key(2)
        self.combo_model.setCurrentIndex(row)
        self.show_selection()
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def mutate_2(self):
        self.append_function_msg("mutate_2()")
        # Set combo to the entry whose key is 3.
        row = self.key_value_model.row_for_key(3)
        self.combo_model.setCurrentIndex(row)
        self.show_selection()
        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def mutate_3(self):
        self.append_function_msg("mutate_3()")
        current_key = self.combo_model.currentData(self.key_value_model.KEY_ROLE)

        # Add one new row at the end.
        self.key_value_model.append_row(6, "six")

        if current_key is not None:
            row = self.key_value_model.row_for_key(current_key)
            self.combo_model.setCurrentIndex(row)
        self.show_selection()
        self.append_msg("mutate_3 added (6, 'six') at end")

        self.append_msg(tab_base.DONE_MSG)

    # ------------------------------------
    def mutate_4(self):
        self.append_function_msg("mutate_4()")
        current_key = self.combo_model.currentData(self.key_value_model.KEY_ROLE)

        # Add zero row at the beginning.
        self.key_value_model.prepend_row(0, "zero")

        if current_key is not None:
            row = self.key_value_model.row_for_key(current_key)
            self.combo_model.setCurrentIndex(row)
        self.show_selection()
        self.append_msg("mutate_4 added (0, 'zero') at beginning")

        self.append_msg(tab_base.DONE_MSG)

    # ------------------------
    def inspect(self):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them

        self_combo_model    = self.combo_model

        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tab's code

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )



# ---- eof
