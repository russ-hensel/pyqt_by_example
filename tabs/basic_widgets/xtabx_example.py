#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
this tab is not functional
        requires more installs
        not really py5 compatible
        used qml, which I do not
        may put in more time to fix in future, but likely not



KEY_WORDS:      qq Data Visualization Tool Tutorial   -- DataVisToolTutorial
CLASS_NAME:     DataVisToolTutorialTab
WIDGETS:        tbc
STATUS:         April 2026 started
TAB_TITLE:      Data Visualizationn / Example
DESCRIPTION:    Chapter 6 - Plot the data in the GraphsView
HOW_COMPLETE:   0  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QPushButtonsxxxx"

"""
Some Notes:

Chapter 6 - Plot the data in the GraphsView - Qt for Python
https://doc.qt.io/qtforpython-6/tutorials/datavisualize/plot_datapoints.html

Data Visualization Tool Tutorial   -- DataVisToolTutorial


"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    pass
# --------------------------------

import time
from   math import floor, ceil

import pandas as pd


from qtpy.QtCore import Qt, QAbstractTableModel, QModelIndex
from qtpy.QtGui import QColor

from qtpy.QtCore import QDateTime, QTime, QTimeZone
from qtpy.QtWidgets import (QHeaderView, QHBoxLayout, QTableView,
                               QSizePolicy)
from qtpy.QtQuickWidgets import QQuickWidget


# # seems to be only in qt6, this might make somewhat compatible -- but fails with qt5
# try:
#     from PySide6.QtGraphs import QLineSeries, QDateTimeAxis, QValueAxis, QGraphsTheme
#     HAS_GRAPHS_THEME    = True

# except ImportError:
#     from qtpy.QtCharts import QLineSeries, QDateTimeAxis, QValueAxis
#     QGraphsTheme        = None
#     HAS_GRAPHS_THEME    = False


from qtpy.QtCharts import QLineSeries, QDateTimeAxis, QValueAxis
QGraphsTheme        = None
HAS_GRAPHS_THEME    = False


#from table_model import CustomTableModel



from qtpy.QtCore import ( QDateTime,
                          QModelIndex,
                          Qt,
                          QTime)

from qtpy.QtGui import QColor


from qtpy.QtWidgets import (QHBoxLayout,
                             QLabel,
                             QMenu,
                             QPushButton,
                             QSizePolicy,
                             QTableView,
                             QVBoxLayout)



import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header



def transform_date(utc, timezone=None):
    utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"
    new_date = QDateTime().fromString(utc, utc_fmt)
    if timezone:
        new_date.setTimeZone(timezone)
    return new_date


def read_data(fname):
    # Read the CSV content
    df = pd.read_csv(fname)

    # Remove wrong magnitudes
    df = df.drop(df[df.mag < 0].index)
    magnitudes = df["mag"]

    # My local timezone
    timezone = QTimeZone(b"Europe/Berlin")

    # Get timestamp transformed to our timezone
    times = df["time"].apply(lambda x: transform_date(x, timezone))

    return times, magnitudes



#  --------
class DataVisToolTutorialTab( tab_base.TabBase ):
    """
    Reference examples for QPushButton

        this is also the place for documentation on the methods normally found
        in a tab_.... file and should display its naming and other coding conventions
        other tab_xxx files may not be as well commented, you should be familiar with
        the conventions and be able to read the code.
    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        self.mutate_dict[4]     = self.mutate_4

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

        # ---- new row c
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row button_1 and _2 ....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        self.widget_init( layout )



        # a label that points to q_pbutton_1
        widget          = QLabel( "q_pbutton_1 -> ", alignment=Qt.AlignRight)
            # no instance variable as we will not use after __init__

        # layout ( add to the windows ) the widget
        row_layout.addWidget( widget )

        # we use a local variable because it reduces the amount of code
        # and does not run any slower
        # we use this local variable idea in many places
        # because we will refer to the bu
        widget              = QPushButton( "q_pbutton_1" )
        self.q_push_button_1    = widget

            # save a reference for later use
        # this function will be called when the button is clicked
        # the code is a little indirect, do on one line if you wish
        connect_to          = self.pb_1_clicked
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        widget              = QLabel("q_pbutton_2 -> ", alignment=Qt.AlignRight)
        row_layout.addWidget( widget )

        widget              = QPushButton( "q_pbutton_2" )
        self.q_push_button_2    = widget
        connect_to          = self.pb_2_clicked
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget, )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #----------------------------
    def get_button_style_sheet( self ):
        """
        what it says

        when applied to a button changes a bit of its appearance

        this is important content for the widgets referenced on this tab
        """
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """






    # ------------------------------------
    def pb_1_clicked( self ):
        """
        What it says

            this function may be connected to a button normally
            q_push_button_1

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "pb_1_clicked()" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def pb_2_clicked( self ):
        """
        What it says

            this function may be connected to a button normally
            q_push_button_1

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "pb_2_clicked()" )

        self.append_msg( tab_base.DONE_MSG  )

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
        msg    = "for q_push_button_1 we more or less reset it"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        widget          = self.q_push_button_1
        widget.setText( "text set in mutate_0()" )
        widget.width     = 300
        widget.setToolTip( None )
        widget.setStyleSheet( "" )

        # ---- change widget
        msg    = "for q_push_button_2 no mutations"
        self.append_msg( msg, )

        widget          = self.q_push_button_2
        # self.q_push_button_1.setDisabled( True )
        # self.q_push_button_2.setDisabled( False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_1()" )
        # msg    = "begin implementation"
        # self.append_msg( msg, clear     = False )
        # for self.q_push_button_1

        msg    = "mess with q_push_button_1"
        self.append_msg( msg, )

        widget        = self.q_push_button_1
            # it is often convenient to use a local variable,
            # you will see this a lot in our code, it does not seem to
            # be typical but we think it should be

        msg    = "q_push_button_1 set a tooltip"
        self.append_msg( msg, )

        widget.setToolTip( "this is a tool tip" )
        widget.setText( "text set in \nmutate_1()" )
            # note \n
        widget.width     = 200

        # ---- change widget
        msg    = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        # ---- self.q_push_button_2
        widget        = self.q_push_button_2
        # msg    = "setChecked(True )"
        # self.append_msg( msg, )

        # msg        = f"{self.q_push_button_1.isChecked() = } "
        # self.append_msg( msg, )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_2()" )

        msg    = "change some attributes..."
        self.append_msg( msg,  )


        widget     = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setVisible( False )

        msg    = "q_push_button_1 mess with checkable enabled..."
        self.append_msg( msg,  )

        self.q_push_button_1.setCheckable( True )
        self.q_push_button_1.setChecked( True )
        self.q_push_button_1.setDisabled( True )

        self.q_push_button_1.setVisible( True )

        # next does not seem to work
        self.q_push_button_1.setCheckable( True )

        # ---- change widget
        msg    = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        widget     = self.q_push_button_2
        widget.setCheckable( True )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_3()" )

        msg    = "re-enable some stuff -- change attributes"
        self.append_msg( msg, clear = False )

        # ---- first widget
        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setDisabled( False )
        self.q_push_button_1.setVisible( True )
        self.q_push_button_1.setCheckable( True )
        self.q_push_button_1.toggle()

        msg    = "add menu to q_push_button_1"
        self.append_msg( msg, clear = False )

        menu                = QMenu(self)
        menu.addAction("Option 1")
        menu.addAction("Option 2")
        widget.setMenu( menu )

        # ---- change widget
        widget      = self.q_push_button_2
        msg         = "\nsome changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        msg    = "q_push_button_2 mess with style sheet... hover ... color "
        self.append_msg( msg,  )

        widget.setCheckable( False )
        widget.setStyleSheet( self.get_button_style_sheet() )
        msg     = f"get style sheet from widget \n {widget.styleSheet()}"
        self.append_msg( msg,  )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "mutate_4()" )

        msg    = "undo many of earlier mutations"
        self.append_msg( msg, clear = False )

        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setDisabled( False )
        self.q_push_button_1.setVisible( True )
        self.q_push_button_1.setCheckable( True )

        # seems to make togable, how to turn off
        #self.q_push_button_1.toggle()

        msg    = "add menu to q_push_button_1"
        self.append_msg( msg, clear = False )
        menu                = QMenu(self)
        menu.addAction("Menu Option 1")
        menu.addAction("Menu Option 2")
        # try to clear the menu
        widget.setMenu( None )

        # ---- change widget
        widget      = self.q_push_button_2
        msg         = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        widget.setStyleSheet("")
            # no style sheet

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
        self_q_push_button_1    = self.q_push_button_1
        self_q_push_button_2    = self.q_push_button_1

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





# class Widget(QWidget):
    def widget_init(self, layout ):   #data):
        # super().__init__()
        data = read_data(  "./all_day.csv" )
        # Getting the Model
        self.model = CustomTableModel(data)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # QTableView Headers
        resize = QHeaderView.ResizeMode.ResizeToContents
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(resize)
        self.vertical_header.setSectionResizeMode(resize)
        self.horizontal_header.setStretchLastSection(True)

        # Create QGraphView via QML
        self.populate_series()
        self.quick_widget = QQuickWidget(self)
        self.quick_widget.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.theme = QGraphsTheme()
        self.theme.setTheme(QGraphsTheme.Theme.BlueSeries)
        initial_properties = {"theme": self.theme,
                              "axisX": self.axis_x,
                              "axisY": self.axis_y,
                              "seriesList": self.series}
        self.quick_widget.setInitialProperties(initial_properties)
        self.quick_widget.loadFromModule("QtGraphs", "GraphsView")

        # QWidget Layout
        self.main_layout = QHBoxLayout(self)
        size = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Right Layout
        size.setHorizontalStretch(4)
        self.quick_widget.setSizePolicy(size)
        layout.addWidget(self.quick_widget)

    def populate_series(self):
        def seconds(qtime: QTime):
            return qtime.minute() * 60 + qtime.second()

        self.series = QLineSeries()
        self.series.setName("Magnitude (Column 1)")

        # Filling QLineSeries
        time_min = QDateTime(2100, 1, 1, 0, 0, 0)
        time_max = QDateTime(1970, 1, 1, 0, 0, 0)
        # time_zone = QTimeZone( QTimeZone.Initialization.UTC )
        time_zone = QTimeZone(b"UTC")


        y_min =  1e37
        y_max = -1e37
        date_fmt = "yyyy-MM-dd HH:mm:ss.zzz"
        for i in range(self.model.rowCount()):
            t = self.model.index(i, 0).data()
            time = QDateTime.fromString(t, date_fmt)
            time.setTimeZone(time_zone)
            y = float(self.model.index(i, 1).data())
            if time.isValid() and y > 0:
                if time > time_max:
                    time_max = time
                if time < time_min:
                    time_min = time
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                self.series.append(time.toMSecsSinceEpoch(), y)

        # Setting X-axis
        self.axis_x = QDateTimeAxis()
        # self.axis_x.setLabelFormat("dd.MM (h:mm)")
        self.axis_x.setTitleText("Date")
        self.axis_x.setMin(time_min.addSecs(-seconds(time_min.time())))
        self.axis_x.setMax(time_max.addSecs(3600 - seconds(time_max.time())))
        #self.series.setAxisX(self.axis_x)

        # Setting Y-axis
        self.axis_y = QValueAxis()
        #self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("Magnitude")
        self.axis_y.setMin(floor(y_min))
        self.axis_y.setMax(ceil(y_max))
        #self.series.setAxisY(self.axis_y)

        # older version of
        # self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        # self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)




class CustomTableModel( QAbstractTableModel ):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.input_dates = data[0].values
        self.input_magnitudes = data[1].values

        self.column_count = 2
        self.row_count = len(self.input_magnitudes)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return ("Date", "Magnitude")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                date = self.input_dates[row].toPython()
                return str(date)[:-3]
            elif column == 1:
                magnitude = self.input_magnitudes[row]
                return f"{magnitude:.2f}"
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.white)
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        return None

