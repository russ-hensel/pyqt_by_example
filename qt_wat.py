#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this shows wat_inspector being call from a script that is not inside
a qt application.

Note the setup code that allows it to work.

"""

import sys
import time

from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QDateEdit,
                             QMainWindow,
                             QMenu,
                             QSizePolicy)

#import qt_wat_app.py
import wat_inspector


def wat_setup():
    """ """

    app                 = QApplication( sys.argv )
    a_wat_inspector     = wat_inspector.WatInspector( app )

    #a_wat_function()
    print( "end function 1")


def a_wat_function():
    """ """
    print( "start" )
    time.sleep( .1 )
    #app.exec()
    something_local   = 1
    a_local_list      = [1,2,3,4]
    wat_inspector.go(
          msg            = "inspect from a_function",
          a_locals       = locals(),
          a_globals      = globals(), )
    print( "end a_wat_function")
    #app.exec()
    return


# def wat_setup_2():
#     """ """
#     TEXT_EDITOR     = "xed"
#     app             = QApplication( sys.argv )
#     dialog          = wat_inspector_2.WatInspector( app )
#     #a_wat_function()
#     print( "end wat_setup_2 ")


# def a_wat_function_2():
#     """ """
#     print( "start" )
#     time.sleep( .1 )
#     #app.exec()
#     something_local   = 1
#     a_local_list      = [1,2,3,4]
#     wat_inspector_2.go(
#          msg            = "inspect from a_function",
#          a_locals       = locals(),
#          a_globals      = globals(), )
#     print( "a_wat_function_2 end")
#     #app.exec()
#     return



# --------------------
if __name__ == "__main__":
    pass


    # wat_setup()
    # a_wat_function()


    wat_setup()
    a_wat_function()


    # #a_function()   TEXT_EDITOR     = "xed"
    #    app             = QApplication( sys.argv )
    #    dialog          = wat_inspector.DisplayWat( app )  # Create an instance of your custom QDialog
    #    a_wat_function()
    #    print( "end function 1")
    # window          = QtWidgetExamples()
    # window.show()
    #sys.exit(
    #app.exec()

    #sys.exit( 0 )