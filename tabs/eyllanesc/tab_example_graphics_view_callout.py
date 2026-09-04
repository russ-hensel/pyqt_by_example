#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
--- metadata here including WIKI_LINK as Constant ( not comment )


KEY_WORDS:      eyllanesc plot graph plot chart graph graphics
CLASS_NAME:     ExampleGraphicsCalloutTab
WIDGETS:        QGraphicsItem QGraphicsView QChart QLineSeries QSplineSeries
STATUS:         works at first blush
TAB_TITLE:      GraphicsCallout / Example
DESCRIPTION:    An example of a Graphics Callout from eyllanesc/QtExamples
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QTcpServer"

"""
Some Notes:

eyllanesc/QtExamples: Translations of the official Qt examples into PyQt5 (also PySide2) and more. :octocat:
https://github.com/eyllanesc/QtExamples

QtExamples/official/charts/barchart/main.py at master · eyllanesc/QtExamples
https://github.com/eyllanesc/QtExamples/blob/master/official/charts/barchart/main.py

this example based on /mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/QtExamples-master/official/network/loopback/main.py

"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

import qtpy
import wat_inspector
from qtpy.QtCharts import (QBarSet,
                           QChart,
                           QLineSeries,
                           QSplineSeries)
from qtpy.QtCore import (QPoint,
                         QPointF,
                         QRect,
                         QRectF,
                         QSizeF,
                         Qt)
from qtpy.QtGui import (QColor,
                        QFont,
                        QFontMetrics,
                        QPainter,
                        QPainterPath)
#from qtpy.QtNetwork import QAbstractSocket, QHostAddress, QTcpServer, QTcpSocket
from qtpy.QtWidgets import (QGraphicsItem,
                            QGraphicsScene,
                            QGraphicsSimpleTextItem,
                            QGraphicsView,
                            QHBoxLayout,
                            QVBoxLayout)

import tab_base
import utils_for_tabs as uft

#from callout import Callout










# ---- end imports

print_func_header   = uft.print_func_header



class Callout( QGraphicsItem ):
    def __init__( self, chart ):
        super().__init__(chart)

        self.m_chart    = chart
        self.m_text     = ""
        self.m_textRect = QRectF()
        self.m_rect     = QRectF()
        self.m_anchor   = QPointF()
        self.m_font     = QFont()

    def boundingRect(self):
        anchor = self.mapFromParent(self.m_chart.mapToPosition(self.m_anchor))
        rect = QRectF()
        rect.setLeft(min(self.m_rect.left(), anchor.x()))
        rect.setRight(max(self.m_rect.right(), anchor.x()))
        rect.setTop(min(self.m_rect.top(), anchor.y()))
        rect.setBottom(max(self.m_rect.bottom(), anchor.y()))
        return rect

    def paint( self, painter, option, widget=None ):
        path = QPainterPath()
        path.addRoundedRect(self.m_rect, 5, 5)

        anchor = self.mapFromParent(self.m_chart.mapToPosition(self.m_anchor))
        if not self.m_rect.contains(anchor):
            point1 = QPointF()
            point2 = QPointF()

            # establish the position of the anchor point in relation to m_rect
            above = anchor.y() <= self.m_rect.top()
            aboveCenter = (
                anchor.y() > self.m_rect.top()
                and anchor.y() <= self.m_rect.center().y()
            )
            belowCenter = (
                anchor.y() > self.m_rect.center().y()
                and anchor.y() <= self.m_rect.bottom()
            )
            below = anchor.y() > self.m_rect.bottom()

            onLeft = anchor.x() <= self.m_rect.left()
            leftOfCenter = (
                anchor.x() > self.m_rect.left()
                and anchor.x() <= self.m_rect.center().x()
            )
            rightOfCenter = (
                anchor.x() > self.m_rect.center().x()
                and anchor.x() <= self.m_rect.right()
            )
            onRight = anchor.x() > self.m_rect.right()

            # get the nearest m_rect corner.
            x = (onRight + rightOfCenter) * self.m_rect.width()
            y = (below + belowCenter) * self.m_rect.height()
            cornerCase = (
                (above and onLeft)
                or (above and onRight)
                or (below and onLeft)
                or (below and onRight)
            )
            vertical = abs(anchor.x() - x) > abs(anchor.y() - y)

            x1 = (
                x
                + leftOfCenter * 10
                - rightOfCenter * 20
                + cornerCase * int(not vertical) * (onLeft * 10 - onRight * 20)
            )
            y1 = (
                y
                + aboveCenter * 10
                - belowCenter * 20
                + cornerCase * int(vertical) * (above * 10 - below * 20)
            )
            point1.setX(x1)
            point1.setY(y1)

            x2 = (
                x
                + leftOfCenter * 20
                - rightOfCenter * 10
                + cornerCase * int(not vertical) * (onLeft * 20 - onRight * 10)
            )
            y2 = (
                y
                + aboveCenter * 20
                - belowCenter * 10
                + cornerCase * int(vertical) * (above * 20 - below * 10)
            )
            point2.setX(x2)
            point2.setY(y2)

            path.moveTo(point1)
            path.lineTo(anchor)
            path.lineTo(point2)
            path = path.simplified()

        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)
        painter.drawText( self.m_textRect, self.m_text )

    #------------------------------
    def mousePressEvent( self, event ):
        event.setAccepted( True )

    #------------------------------
    def mouseMoveEvent(self, event):
        """
        """
        if event.buttons() & qtpy.LeftButton:
            self.setPos(
                self.mapToParent( event.pos() - event.buttonDownPos(qtpy.LeftButton) )
                )
            event.setAccepted( True )

        else:
            event.setAccepted( False )

    #------------------------------
    def setText( self, text ):
        """
        """
        self.m_text     = text
        metrics         = QFontMetrics(self.m_font)
        self.m_textRect = QRectF(
            metrics.boundingRect(QRect(0, 0, 150, 150), Qt.AlignLeft, self.m_text)
            )
        self.m_textRect.translate(5, 5)
        self.prepareGeometryChange()
        self.m_rect     = self.m_textRect.adjusted(-5, -5, 5, 5)

    #------------------------------
    def setAnchor(self, point):
        """ """
        self.m_anchor = point

    # def updateGeometry(self):
    #     self.prepareGeometryChange()
    #     self.setPos(self.m_chart.mapToPosition(self.m_anchor) + QPoint(10, -50))

    #------------------------------
    def updateGeometry(self):
        """ """
        self.prepareGeometryChange()
        self.setPos(
            self.m_chart.mapToPosition( self.m_anchor ) + QPointF( 10, -50 )
                     )

# --------------------------------------------
class View( QGraphicsView ):
    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
        scene               = QGraphicsScene(self)
        self.setScene(scene)

        self.m_tooltip      = None
        self.m_callouts     = []

        self.setDragMode( QGraphicsView.NoDrag )
        self.setVerticalScrollBarPolicy(   Qt.ScrollBarPolicy.ScrollBarAlwaysOff )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarPolicy.ScrollBarAlwaysOff )

        # chart
        self.m_chart = QChart()
        self.m_chart.setMinimumSize(640, 480)
        self.m_chart.setTitle(
            "Hover the line to show callout. Click the line to make it stay"
            )
        self.m_chart.legend().hide()

        series = QLineSeries()
        series.append(1, 3)
        series.append(4, 5)
        series.append(5, 4.5)
        series.append(7, 1)
        series.append(11, 2)
        self.m_chart.addSeries(series)

        series2 = QSplineSeries()
        series2.append(1.6, 1.4)
        series2.append(2.4, 3.5)
        series2.append(3.7, 2.5)
        series2.append(7, 4)
        series2.append(10, 2)
        self.m_chart.addSeries(series2)

        self.m_chart.createDefaultAxes()
        self.m_chart.setAcceptHoverEvents(True)

        self.setRenderHint(QPainter.Antialiasing)
        self.scene().addItem( self.m_chart )

        self.m_coordX = QGraphicsSimpleTextItem( self.m_chart )
        self.m_coordX.setPos(
            self.m_chart.size().width() / 2 - 50, self.m_chart.size().height()
            )
        self.m_coordX.setText("X: ")
        self.m_coordY = QGraphicsSimpleTextItem(self.m_chart)
        self.m_coordY.setPos(
            self.m_chart.size().width() / 2 + 50, self.m_chart.size().height()
            )
        self.m_coordY.setText("Y: ")

        series.clicked.connect(self.keepCallout)
        series.hovered.connect(self.tooltip)

        series2.clicked.connect(self.keepCallout)
        series2.hovered.connect(self.tooltip)

        self.setMouseTracking(True)

    # ---------------------------
    def resizeEvent(self, event):
        if self.scene() is not None:
            self.scene().setSceneRect(QRectF(QRect(QPoint(0, 0), event.size())))
            self.m_chart.resize(QSizeF(event.size()))
            self.m_coordX.setPos(
                self.m_chart.size().width() / 2 - 50, self.m_chart.size().height() - 20
                )
            self.m_coordY.setPos(
                self.m_chart.size().width() / 2 + 50, self.m_chart.size().height() - 20
                )

            for callout in self.m_callouts:
                callout.updateGeometry()

        super().resizeEvent(event)

    # -------------------------------
    def mouseMoveEvent( self, event ):
        """
        """
        pos     = QPointF( event.pos() )

        value   = self.m_chart.mapToValue( pos )

        self.m_coordX.setText("X: %f" % value.x())
        self.m_coordY.setText("Y: %f" % value.y())


        # self.m_coordX.setText("X: %f" % self.m_chart.mapToValue(event.pos()).x())
        # self.m_coordY.setText("Y: %f" % self.m_chart.mapToValue(event.pos()).y())

        super().mouseMoveEvent(event)

    # -------------------------------
    def keepCallout(self):
        """
        """
        self.m_callouts.append(self.m_tooltip)
        self.m_tooltip = Callout( self.m_chart )

    # -------------------------------
    def tooltip( self, point, state ):
        """ """
        if self.m_tooltip is None:
            self.m_tooltip = Callout( self.m_chart )

        if state:
            self.m_tooltip.setText("X: {:f} \nY: {:f} ".format(point.x(), point.y()))
            self.m_tooltip.setAnchor(point)
            self.m_tooltip.setZValue(11)
            self.m_tooltip.updateGeometry()
            self.m_tooltip.show()

        else:
            self.m_tooltip.hide()


# -------------------------------
class ExampleGraphicsCalloutTab( tab_base.TabBase ):
    """
    Examples for


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



        view = View(   )
        #chartView.setRenderHint( QPainter.Antialiasing )

        row_layout.addWidget( view )

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
