#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
--- metadata here including WIKI_LINK as Constant ( not comment )


KEY_WORDS:      eyllanesc qml quick calculator calqlatr demo zz
CLASS_NAME:     ExampleCalqlatrTab
WIDGETS:        QQuickWidget
STATUS:         works, qt5 and qt6
TAB_TITLE:      Example Calqlatr / QML Calculator
DESCRIPTION:    The Qt calqlatr QML demo embedded in a tab as a QQuickWidget
HOW_COMPLETE:   15  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Example-Calculator"

"""
Some Notes:

eyllanesc/QtExamples: Translations of the official Qt examples into PyQt5 (also PySide2) and more.
https://github.com/eyllanesc/QtExamples

ported from
/mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/QtExamples-master/official/demos/calqlatr/main.py

the original opened a QQuickView, which is a QWindow and so gets its own
top level window.  here we use QQuickWidget instead, which is a real
QWidget and drops straight into a layout.  see tab_example_clocks.py,
which had the same treatment.

what had to change to run on qtpy / qt6:

    main.py             from Qt.QtCore ...      -> from qtpy.QtCore ...
                        Qt.AA_EnableHighDpiScaling gone in qt6
                        QQuickView.Error        -> QQuickView.Status.Error
                        SizeRootObjectToView    -> ResizeMode.SizeRootObjectToView
                        app.exec_()             -> app.exec()
    calqlatr_rc.py      from PyQt5 import QtCore -> from qtpy import QtCore
    calqlatr.qml        Keys.onPressed: {}      -> Keys.onPressed: ( event ) => {}
                            qt6 deprecates injected signal handler parameters
    content/Display.qml fontSize got a floor, Screen.pixelDensity alone
                            gives an unreadable ~5px font on a desktop monitor

the other qml -- Button.qml, NumberPad.qml, calculator.js -- needed nothing.

calqlatr_fit.qml is new, not part of the original demo.  the demo is
laid out at a fixed 320 x 480 and clips rather than scales, and a tab
in a 600 high window does not have 480 to give it, so the fitter holds
the demo at its natural size and scales it to the room available.

the qml sources live in ./calqlatr, but what actually runs is the copy
compiled into calqlatr_rc.py.  edit the sources then regenerate, see the
comment at the top of calqlatr_rc.py.
"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

import wat_inspector

from qtpy.QtCore          import QUrl
from qtpy.QtQuickWidgets  import QQuickWidget

from qtpy.QtWidgets import (QHBoxLayout,
                            QVBoxLayout)

import tab_base
import utils_for_tabs as uft

# ---- end imports

print_func_header   = uft.print_func_header


import calqlatr_rc  # noqa: F401

# -------------------------------
class ExampleCalqlatrWidget( QQuickWidget ):
    """
    The calqlatr QML scene embedded as an ordinary widget.

    QQuickWidget is a real QWidget, so it drops straight into a layout.
    QQuickView, used by the original, is a QWindow: it needs
    QWidget.createWindowContainer() or it opens as its own window.

    All the work is per instance, in __init__, so closing and reopening
    the tab builds a fresh scene each time.
    """

    def __init__( self, parent = None ):

        super().__init__( parent )

        self.setResizeMode( QQuickWidget.ResizeMode.SizeRootObjectToView )

        a_url       = QUrl( "qrc:/demos/calqlatr/calqlatr_fit.qml" )
        self.setSource( a_url )

        if self.status() == QQuickWidget.Status.Error:
            for ix, i_error in enumerate( self.errors() ):
                msg     = ( f"calqlatr_fit.qml error {ix}: {i_error.toString()}" )
                print( msg )

        # calqlatr_fit.qml scales the 320 x 480 demo to whatever we give
        # it, so a modest minimum is enough
        self.setMinimumSize( 200, 300 )

# -------------------------------
class ExampleCalqlatrTab( tab_base.TabBase ):
    """
    Examples for QML embedded in a widget tab


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
        main_layout.addLayout( layout := QVBoxLayout() )

        # ---- new row, the qml calculator
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout, 1 )
            # the 1 is a stretch factor, this row gets the spare height

        widget              = ExampleCalqlatrWidget()
        self.calqlatr       = widget            # keep a ref, handy for inspect
        widget.setMaximumWidth( 420 )
            # the demo is tall and narrow, without a cap it is smeared
            # across the whole width of the tab

        row_layout.addWidget( widget )
        row_layout.addStretch( 1 )

        # ---- new row, for build_gui_last_buttons
        button_layout           = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #--------------------------
    def _build_gui_bot( self, layout ):
        """
        the ancestor puts a QTextEdit here with an expanding size policy,
        which eats most of the tab.  the qml scene wants its full 480 high,
        so cap the message widget and let the calculator have the rest.
        """
        super()._build_gui_bot( layout )

        self.msg_widget.setMaximumHeight( 100 )

    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find ???

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "signal_sent()" )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_0()" )

        # ---- change widget
        msg    = ( "click the keypad, or type digits and + - * / enter,\n"
                   "drag the paper display sideways to slide the pad" )
        self.append_msg( msg, clear = False )

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
        self_calqlatr           = self.calqlatr                # noqa
        self_calqlatr_root      = self.calqlatr.rootObject()   # noqa

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
