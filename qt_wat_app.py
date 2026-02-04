#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 08:49:06 2024

@author: russ
"""
"""


qt_wat.py
qt_wat_app.py

"""

import sys
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QGridLayout,
                             QGroupBox,
                             QLabel,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import wat_inspector  # wat_setup

# ---- end imports


class MainWindow( QMainWindow ):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("QMainWindow")



        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Create buttons
        button1 = QPushButton("Button 1")
        self.button_1    = button1
        button2 = QPushButton("Button 2")

        # Connect button signals to slots
        button1.clicked.connect(lambda: self.print_message(button1.text()))
        button2.clicked.connect(lambda: self.print_message(button2.text()))


        # Create text entry fields and labels
        label1 = QLabel("Text Field 1:")
        label2 = QLabel("Text Field 2:")
        label3 = QLabel("Text Field 3:")
        text_field1 = QLineEdit()
        text_field2 = QLineEdit()
        text_field3 = QLineEdit()

        # Add widgets to the layout
        layout.addWidget(button1, 0, 0)
        layout.addWidget(button2, 0, 1)

        widget   = QPushButton("call_wat_inspector")
        widget.clicked.connect( self.call_wat_inspector )
        layout.addWidget( widget, 0, 2 )

        # bug here
        # widget   = QPushButton("call_wat_inspector twice")
        # widget.clicked.connect( self.call_wat_inspector_twice )
        # layout.addWidget( widget, 0, 3 )


        layout.addWidget(label1, 1, 0)
        layout.addWidget(text_field1, 1, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(text_field2, 2, 1)
        layout.addWidget(label3, 3, 0)
        layout.addWidget(text_field3, 3, 1)

    # -------------------------------
    def print_message(self, text):
        """ """
        print("Button clicked:", text)

    # -------------------------------
    def call_wat_inspector(self,  ):
        """ """
        print("call_wat_inspector" )
        # wat_setup and go
        self_button_1     = self.button_1 # makds a local

        wat_inspector.go(
             msg            = "call_wat_inspector",
             a_locals       = locals(),
             a_globals      = globals(), )

    # -------------------------------
    def call_wat_inspector_twice(self,  ):
        """ """
        print("call_wat_inspector_twice" )
        # wat_setup and go
        self_button_1     = self.button_1 # makds a local

        print( "call wat inspector first time " )
        wat_inspector.go(
             msg            = "call_wat_inspector 1",
             #inspect_me     = self,
             a_locals       = locals(),
             a_globals      = globals(), )


        self.call_wat_inspector_again()

        # wat_inspector.go(
        #      msg            = "call_wat_inspector 2",
        #      #inspect_me     = self,
        #      a_locals       = locals(),
        #      a_globals      = globals(), )

    # # -------------------------------
    # def call_wat_inspector_again(self,  ):

    #     print( "call wat_inspector_again ")
    #     wat_inspector.go(
    #          msg            = "call_wat_inspector 2",
    #          #inspect_me     = self,
    #          a_locals       = locals(),
    #          a_globals      = globals(), )

# ---- run

app                 = QApplication( [] )
a_wat_inspector     = wat_inspector.WatInspector( app )
# dialog      = wat_inspector.DisplayWat( app )  # wat_setup
window = MainWindow()
window.show()
sys.exit(app.exec())