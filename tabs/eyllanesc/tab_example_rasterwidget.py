#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
--- metadata here including WIKI_LINK as Constant ( not comment )


KEY_WORDS:      eyllanesc  raster paint
CLASS_NAME:     ExampleRasterTab
WIDGETS:        QPaintDevice QBackingStore QPainter
STATUS:         ??works at first blush
TAB_TITLE:      Example / Raster Widget
DESCRIPTION:    An example of painting on a top level window
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Example-Clocks"

"""
Some Notes:

eyllanesc/QtExamples: Translations of the official Qt examples into PyQt5 (also PySide2) and more. :octocat:
https://github.com/eyllanesc/QtExamples

QtExamples/official/demos/clocks at master · eyllanesc/QtExamples
https://github.com/eyllanesc/QtExamples/tree/master/official/demos/clocks



"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

import wat_inspector
from qtpy.QtCore import (QEvent,
                         QRect,
                         QRectF,
                         Qt)
from qtpy.QtGui import (QBackingStore,
                        QExposeEvent,
                        QGradient,
                        QPaintDevice,
                        QPainter,
                        QRegion,
                        QResizeEvent,
                        QWindow)
#from qtpy.QtNetwork import QAbstractSocket, QHostAddress, QTcpServer, QTcpSocket
from qtpy.QtWidgets import (QHBoxLayout,
                            QVBoxLayout)

import tab_base
import utils_for_tabs as uft

# ---- end imports

print_func_header   = uft.print_func_header




class RasterWindow( QWindow ):
    def __init__(self, parent: QWindow = None) -> None:
        super().__init__( parent )
        self.m_backingStore = QBackingStore(self)
        self.setGeometry(100, 100, 300, 200)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.UpdateRequest:
            self.renderNow()
            return True
        return super().event(event)

    def renderLater(self) -> None:
        self.requestUpdate()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.m_backingStore.resize(event.size())

    def exposeEvent(self, event: QExposeEvent) -> None:
        if self.isExposed():
            self.renderNow()

    def renderNow(self) -> None:
        if not self.isExposed():
            return

        rect = QRect(0, 0, self.width(), self.height())
        self.m_backingStore.beginPaint( QRegion(rect) )

        device: QPaintDevice = self.m_backingStore.paintDevice()
        painter = QPainter(device)

        painter.fillRect(0, 0, self.width(), self.height(), QGradient.NightFade)
        self.render(painter)
        painter.end()

        self.m_backingStore.endPaint()
        self.m_backingStore.flush(QRegion(rect))

    def render(self, painter: QPainter) -> None:
        painter.drawText(
            QRectF(0, 0, self.width(), self.height()), Qt.AlignmentFlag.AlignCenter, "QWindow"
        )



#
# -------------------------------
class ExampleRasterTab( tab_base.TabBase ):
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
        self.mutate_dict[1]     = self.mutate_1
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

        # ---- New Row
        # make a layout to put the buttons in
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )



        # ---- new row, for build_gui_last_buttons
        button_layout   = QHBoxLayout(   )
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

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
            these mutations will try to mimic a typical default state
            of a widget for the first push button the
            second will not be modified by mutate_0

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_1()" )

        # ---- change widget
        msg    = "create RasterMainWindow"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        # widget          = self.q_push_button_1
        # widget.setText( "text set in mutate_0()" )
        # widget.width    = 300
        # widget.setToolTip( None )
        # widget.setStyleSheet( "" )
        # self.a_main_window   =  QMainWindow()
        self.raster_window   =  RasterWindow(   )
        # self.a_main_window.show()
        self.raster_window.show()



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
        self_clock_widget   = self.clock_widget

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
