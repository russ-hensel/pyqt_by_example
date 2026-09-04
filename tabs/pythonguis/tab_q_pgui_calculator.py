#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
--- metadata here including WIKI_LINK as Constant ( not comment )


KEY_WORDS:      pythonguis Python GUIs
CLASS_NAME:     ExamplePguiCalculatorTab
WIDGETS:        QLCDNumber QFont
STATUS:         ??works at first blush
TAB_TITLE:      Example / Calculator
DESCRIPTION:    An example of a calculator from github pythonguis-examples
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/pythonguis/pythonguis-examples/blob/main/pyqt6/demos/calculator/README.md"

"""
Some Notes:

/mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/pythonguis-examples-main/pyqt6/demos/calculator


"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

import wat_inspector

import operator








from qtpy.QtWidgets import (QMainWindow,
                            QHBoxLayout,
                            QVBoxLayout)

import tab_base
import utils_for_tabs as uft

# was qt6
from calc_window    import Ui_MainWindow
from qtpy.QtWidgets import QMainWindow



# ---- end imports

print_func_header   = uft.print_func_header
# Calculator state.
READY = 0
INPUT = 1


class AMainWindow( QMainWindow, Ui_MainWindow ):
    # was MainWindow in original example
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Setup numbers.
        for n in range(0, 10):
            getattr(self, "pushButton_n%s" % n).pressed.connect(lambda v=n: self.input_number(v))

        # Setup operations.
        self.pushButton_add.pressed.connect(lambda: self.operation(operator.add))
        self.pushButton_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.pushButton_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.pushButton_div.pressed.connect(lambda: self.operation(operator.truediv))  # operator.div for Python2.7

        self.pushButton_pc.pressed.connect(self.operation_pc)
        self.pushButton_eq.pressed.connect(self.equals)

        # Setup actions
        self.actionReset.triggered.connect(self.reset)
        self.pushButton_ac.pressed.connect(self.reset)

        self.actionExit.triggered.connect(self.close)

        self.pushButton_m.pressed.connect(self.memory_store)
        self.pushButton_mr.pressed.connect(self.memory_recall)

        self.memory = 0
        self.reset()

        self.show()

    def display(self):
        self.lcdNumber.display(self.stack[-1])

    def reset(self):
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def memory_store(self):
        self.memory = self.lcdNumber.value()

    def memory_recall(self):
        self.state = INPUT
        self.stack[-1] = self.memory
        self.display()

    def input_number(self, v):
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + v

        self.display()

    def operation(self, op):
        if self.current_op:  # Complete the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def operation_pc(self):
        self.state = INPUT
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        # Support to allow '=' to repeat previous operation
        # if no further input has been added.
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display("Err")
                self.stack = [0]
            else:
                self.current_op = None
                self.state = READY
                self.display()


# -------------------------------
class ExamplePguiCalculatorTab( tab_base.TabBase ):
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
        msg    = "use next mutate to create calculator window "
        self.append_msg( msg, clear = False )


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
        msg    = "create Calculator"
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
        self.calc_window  =  AMainWindow(   )
        # self.a_main_window.show()
        self.calc_window.show()



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
