#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
A basic app for qt6
"""


# ---- imports
# Changed PyQt5 to PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

class MainWindow( QMainWindow ):
    def __init__(self):
        """Build the main window """
        super().__init__()

        self.setWindowTitle( "Simple Qt6 App" )
        self.setFixedSize(300, 100)

        # Create central widget
        a_central_widget    = QWidget()
        self.setCentralWidget( a_central_widget )

        # Set up layout and add to the central widget
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
        a_layout.addWidget( widget )

    def on_button_click(self):
        """
        Simple action: set text in line edit when button is clicked
        """
        print("Button Clicked!")
        self.line_edit.setText("Hello PyQt6!") # Added a small action to see it work

if __name__ == '__main__':
    """
    Create and run a minimum application
    """
    app         = QApplication( [] )
    window      = MainWindow()
    window.show()

    # Changed .exec_() to .exec()
    app.exec()


# ---- eof