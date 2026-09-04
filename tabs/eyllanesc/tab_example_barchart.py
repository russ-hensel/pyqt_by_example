#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which should
# be named xxxxTab.py     among other things
# this example based on /mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/QtExamples-master/official/network/loopback/main.py

KEY_WORDS:      eyllanesc plot chart graph graphics
CLASS_NAME:     ExampleBarChartTab
WIDGETS:        QBarSet  QBarSeries QChart QChartView QPainter
STATUS:         works at first blush
TAB_TITLE:      BarChart / Example
DESCRIPTION:    An example of a bar chart from eyllanesc/QtExamples
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QTcpServer"

"""
Some Notes:

eyllanesc/QtExamples: Translations of the official Qt examples into PyQt5 (also PySide2) and more. :octocat:
https://github.com/eyllanesc/QtExamples

QtExamples/official/charts/barchart/main.py at master · eyllanesc/QtExamples
https://github.com/eyllanesc/QtExamples/blob/master/official/charts/barchart/main.py


"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

import wat_inspector
from qtpy.QtCharts import (QBarCategoryAxis,
                           QBarSeries,
                           QBarSet,
                           QChart,
                           QChartView,
                           QValueAxis)
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter
from qtpy.QtWidgets import (QHBoxLayout,
                            QVBoxLayout)

import tab_base
import utils_for_tabs as uft

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class ExampleBarChartTab( tab_base.TabBase ):
    """
    Examples for  ....


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

        # # ---- new row c -- testing never used
        # row_layout          = QHBoxLayout(   )
        # layout.addLayout( row_layout )

        # ---- New Row button_1 and _2 ....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        set0 = QBarSet("Jane")
        set1 = QBarSet("John")
        set2 = QBarSet("Axel")
        set3 = QBarSet("Mary")
        set4 = QBarSet("Samantha")

        set0 << 1 << 2 << 3 << 4 << 5 << 6
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2

        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Simple barchart example")

        # chart.setAnimationOptions(QChart.SeriesAnimations)
        # # Qt5 (old)
        # chart.setAnimationOptions(QChart.SeriesAnimations)

        # Qt6 (new)
        chart.setAnimationOptions( QChart.AnimationOption.SeriesAnimations )

        categories  = ("Jan", "Feb", "Mar", "Apr", "May", "Jun")
        axisX       = QBarCategoryAxis()
        axisX.append(categories)
        #chart.addAxis(axisX, qtpy.AlignBottom)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)

        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 15)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft )
        series.attachAxis(axisY)

        chart.legend().setVisible( True )
        chart.legend().setAlignment( Qt.AlignmentFlag.AlignBottom )

        chartView = QChartView( chart )
        chartView.setRenderHint( QPainter.Antialiasing )

        row_layout.addWidget( chartView )

        # ---- new row, for build_gui_last_buttons
        button_layout           = QHBoxLayout(   )
        layout.addLayout( button_layout, )


        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )


    # ------------------------------------
    def signal_sent( self, msg ):
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
        # self_q_push_button_1    = self.q_push_button_1
        # self_q_push_button_2    = self.q_push_button_1

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
