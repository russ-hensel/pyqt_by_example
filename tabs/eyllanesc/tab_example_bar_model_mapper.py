#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which should
# be named xxxxTab.py     among other things
# this example based on /mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/QtExamples-master/official/network/loopback/main.py

KEY_WORDS:      eyllanesc plot graph plot chart graph graphics
CLASS_NAME:     ExampleBarModelMapperTab
WIDGETS:        QAbstractTableModel QTableView QChartView QChart.AnimationOption.AllAnimations
STATUS:         works at first blush
TAB_TITLE:      BarModelMapper / Example
DESCRIPTION:    An example of a BarModelMapper from eyllanesc/QtExamples
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Example Bar_Model Mapper"

"""
Some Notes:


eyllanesc/QtExamples: Translations of the official Qt examples into PyQt5 (also PySide2) and more. :octocat:
https://github.com/eyllanesc/QtExamples

QtExamples/official/charts/barmodelmapper at master · eyllanesc/QtExamples
https://github.com/eyllanesc/QtExamples/tree/master/official/charts/barmodelmapper

# /mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/QtExamples-master/official/charts/barmodelmapper/main.py

"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

# ---- imports

import random
from collections import defaultdict

import wat_inspector

from qtpy.QtCharts import (QBarCategoryAxis,
                           QBarSeries,
                           QChart,
                           QChartView,
                           QValueAxis,
                           QVBarModelMapper)
from qtpy.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
from qtpy.QtGui import QColor, QPainter
from qtpy.QtWidgets import (QGridLayout,
                            QHBoxLayout,
                            QHeaderView,
                            QTableView,
                            QVBoxLayout,
                            QWidget)

import tab_base
import utils_for_tabs as uft

# ---- end imports

print_func_header   = uft.print_func_header

#---------------------------------
class CustomTableModel( QAbstractTableModel ):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_data = []
        self.m_mapping = defaultdict(list)

        self.m_columnCount = 6
        self.m_rowCount = 12

        for i in range(self.m_rowCount):
            dataVec = []
            for k in range(self.m_columnCount):
                if k % 2 == 0:
                    dataVec.append(i * 50 + random.randint(0, 20))
                else:
                    dataVec.append(random.randint(0, 100))
            self.m_data.append(dataVec)

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_data)

    def columnCount(self, paren=QModelIndex()):
        return self.m_columnCount

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return

        if orientation == Qt.Horizontal:
            return "201%d" % section

        else:
            return "%d" % (section + 1)

    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self.m_data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            for key, rect in self.m_mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(key)
            return QColor(Qt.white)

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self.m_data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def addMapping(self, color, area):
        self.m_mapping[color] = area


#---------------------------------
class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_model = CustomTableModel()

        tableView = QTableView()
        tableView.setModel(self.m_model)
        tableView.setMinimumWidth(300)
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.m_model.setParent(tableView)

        chart = QChart()
        # chart.setAnimationOptions( QChart.AllAnimations )

        chart.setAnimationOptions( QChart.AnimationOption.AllAnimations )

        series = QBarSeries()

        first   = 3
        count   = 5
        mapper  = QVBarModelMapper(self)
        mapper.setFirstBarSetColumn(1)
        mapper.setLastBarSetColumn(4)
        mapper.setFirstRow(first)
        mapper.setRowCount(count)
        mapper.setSeries(series)
        mapper.setModel(self.m_model)
        chart.addSeries(series)

        seriesColorHex = "#000000"

        barsets = series.barSets()

        for i, barset in enumerate(barsets):
            seriesColorHex = barset.brush().color().name()
            self.m_model.addMapping(
                seriesColorHex, QRect(1 + i, first, 1, barset.count())
                )

        categories  = ("April", "May", "June", "July", "August")
        axisX       = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY       = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chartView   = QChartView( chart )
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setMinimumSize(640, 480)

        mainLayout  = QGridLayout( self )
        mainLayout.addWidget(tableView, 1, 0)
        mainLayout.addWidget(chartView, 1, 1)
        mainLayout.setColumnStretch( 1, 1 )
        mainLayout.setColumnStretch( 0, 0 )

# -------------------------------
class ExampleBarModelMapperTab( tab_base.TabBase ):
    """
    Example for


    """
    def __init__(self):
        """
        set up the tab
            this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK     # helps the link to the wiki

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        # self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]     = self.mutate_2
        # self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4

        self._build_gui()

    #--------------------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        This code is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- TableWidget
        widget              = TableWidget()
        self.table_widget   = widget
        row_layout.addWidget( widget )

        # ---- new row, for build_gui_last_buttons
        button_layout           = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # ------------------------------------
    def signal_sentxxx( self, msg ):
        """
        when a signal is sent, use find ???

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "signal_sent()" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( tab_base.DONE_MSG )


    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
            these mutations will try to mimic a typical default state
            of a widget for the first push button the
            second will not be modified by mutate_0

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_0()" )

        # ---- change widget
        msg    = "this example has no instructive mutations"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        # widget          = self.q_push_button_1
        # widget.setText( "text set in mutate_0()" )
        # widget.width    = 300
        # widget.setToolTip( None )
        # widget.setStyleSheet( "" )

        self.append_msg( tab_base.DONE_MSG )

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
        self_table_widget   = self.table_widget

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
