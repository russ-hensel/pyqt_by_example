#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
A basic app for qt5
"""


# ---- imports
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

class MainWindow( QMainWindow ):
    def __init__(self):
        """Build the main window """
        super().__init__()

        self.setWindowTitle( "Simple Qt5 App" )
        self.setFixedSize(300, 100)

        # Create central widget -- covered in more detail later
        a_central_widget    = QWidget()
        self.setCentralWidget( a_central_widget )

        # Set up layout and add to the central widget -- covered in more detail later
        a_layout        = QVBoxLayout()
        a_central_widget.setLayout( a_layout )

        # ---- QLineEdit
        widget         = QLineEdit()
        self.line_edit = widget
        a_layout.addWidget( widget )

        # ---- QPushButton
        widget          = QPushButton( "Click Me" )
        self.button     = widget

        # Connect button-click to a function called self.on_button_click
        self.button.clicked.connect(self.on_button_click)
            # this is a qt style callback
        a_layout.addWidget( widget )

    def on_button_click(self):
        """
        Just so we can see the button do something
        Simple action: set text in line edit when button is clicked
        """
        print("Button Clicked!")

if __name__ == '__main__':
    """
    Create and run a minimum application
    """
    app         = QApplication( [] )
    window      = MainWindow()
    window.show()

    app.exec_()


# ---- eof
