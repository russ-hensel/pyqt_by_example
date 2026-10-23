#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 11:44:12 2024

Utilities and now the resting place of the globals
which need to move out
seems a bit of a mess, so perhaps factor out

"""


import importlib

from qtpy.QtGui import QColor, QPalette
# ----QtWidgets layouts
# ---- tof
from qtpy.QtWidgets import (QDialog,
                             QLabel,
                             QPushButton,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import re


# ---- end imports

INDENT          = "    "   # {INDENT}
BEGIN_MARK_1    = "\n\n ------------ "
BEGIN_MARK_2    =     " ------------ "    # uft.

parameters      = None   # patche in by main program for now
display_parms   = None   # fixed on first call

main_window     = None

# for now lets get app globals here is None causeing a problem

# --------------------------------
def print_func_header( what ):
    """
    what it says
        in use before we have a message area
    """
    #what    = "fix_me"
    print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")

# --------------------------
class ColoredFiller(QWidget):
    """
    M Fitzpatrick's book,  is source
    ColoredFiller('red')
    colored so you can see it, used as a filler object
        think used one place in misc widgets, consider move
    """
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground( True )
        palette = self.palette()
        palette.setColor( QPalette.Window, QColor(color) )
        self.setPalette( palette )




# -------------------------------------------------------
def create_class_from_stringsxx( module_name, class_name):
    """
    !! same as create instance in app_services, remove dupe
    instance   = uft.create_class_from_strings(   module_name, class_name)
    this will load a class from string names
    this makes it easier to specify classes in the parameter file.

    args:  strings as named
    ret:   instance of the class

    example:
    if not ( self.parameters.ext_processing_module is None ):
        self.ext_processing =  self.create_class_from_strings( self.parameters.ext_processing_module,
                                                               self.parameters.ext_processing_class  )
    """
    a_class    = getattr( importlib.import_module(module_name), class_name )
    instance   = a_class(  )
    return instance


# ---------------------------
def camel_to_snakexxx( camel_str ):
    # Add underscores before uppercase letters and convert to lowercase
    # might be better as s string util
    # camel_to_snake splits on every capital, so it gives h_t_m_l_parser for HTMLParser. It's unused, so delete it or use the usual two-step regex.
    snake_str = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
    return snake_str


# ---------------------------
def to_help_file_name( module_name ):
        """
        take a class name and convert to a help file name
        using the conventions in this code
        or should we just use the module name ?
        module seems simpler
        """
        help_file_name = f"{module_name}.txt"

        return help_file_name


# def class_name_to_help_file( class_name ):
#         """
#         take a class name and convert to a help file name
#         using the conventions in this code
#         or should we just use the module name ?
#         module seems simpler
#         """
#         help_file_name = "may drop this "

#         return help_file_name



#-----------------------------------------------
class SeparatorTabxxxx( QWidget ):
    """
    utils_for_tabs.py
    think not currently in use seem to be buggy
    """
    def __init__( self, msg = None ):
        """
        """
        super().__init__( )
        if msg is None:
            msg         = "This tab indicates the status of the tabs to the right --->"

        self.msg    = msg

        self._build_gui()

    # ------------------------------
    def _build_gui( self,   ):
        """
        the usual
        """
        tab_page        = self

        a_layout        = QVBoxLayout( tab_page )
        self.layout     = a_layout

        widget  = QLabel( self.msg )
        a_layout.addWidget( widget )



# -----------------------
def show_parametersxxx( ):
    """
    what it says,
    """
       # display_parms   = DisplayParameters( None ) # parent = self
    dialog     = DisplayParameters( parent = main_window  )
    if dialog.exec_() == QDialog.Accepted:
        pass

# -----------------------
class DisplayParametersxxx( QDialog ):
    """
    dialog to display parameters
    # think dup of what is in show parameters so this is dead?
    """
    # ------------------------------------------
    def __init__(self, parent ):
        """
        Args:


        Returns:
            None.

        """
        super().__init__( parent )
        self.parent         = parent  # parent may be a function use parent_window
        self.parent_window  = parent
        msg   = "Display Parameters "

        self.setWindowTitle( msg  )

        qt_xpos     = 10
        qt_ypos     = 10
        qt_width    = 1000
        qt_height   = 500
        self.tab_help_dict   = { }
        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        a_layout            = QVBoxLayout( self )
        self.layout         = a_layout

        # ---- code_gen: edit_fields_for_form  -- end table entries

        # Create QTextEdit widget
        text_edit           = QTextEdit()
        # a_layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit
        a_layout.addWidget( text_edit )

        parm_text      = str( parameters )

        cursor = text_edit.textCursor()
        cursor.insertText( parm_text )

        # # ---- buttons
        # self.setLayout( self.layout )
        #self.button_layout      = QVBoxLayout()
        button_layout           = a_layout


        a_widget                = QPushButton( "OK" )
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.accept )
        button_layout.addWidget( a_widget )



# ---- eof