#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KEY_WORDS:      dialog custom modal QDialog own buttons return value
CLASS_NAME:     CustomDialog
WIDGETS:        QDialog, QLineEdit, QCheckBox, QPushButton
DESCRIPTION:    A modal dialog with hand rolled buttons and a return of your own

A starting point to modify, not a finished widget.  No QDialogButtonBox,
the buttons are plain QPushButtons so you can add, remove or rename them
without fighting Qt about what a button "means".

---- example call

    import custom_dialog

    result_code, values = custom_dialog.ask_user( self,
                                                  a_name = "start value",
                                                  a_note = "" )

    if   result_code == custom_dialog.RESULT_OK:
        print( f"user said ok  {values[ 'name' ] = }  {values[ 'wants_email' ] = }" )

    elif result_code == custom_dialog.RESULT_SKIP:
        print( "user skipped, values still readable" )

    else:                                   # RESULT_CANCEL, also Esc and the X
        print( "user cancelled, ignore the values" )

ask_user() blocks until the dialog closes, which is what you want from a
modal dialog.  parent may be None, passing your window centres the dialog
on it and keeps it on top.

---- what to change first

    _build_gui_widgets()    your fields instead of name / note / check box
    get_values()            the dict those fields return
    _build_gui_buttons()    your buttons
    validate()             what counts as a good answer, "" means good
    RESULT_* below          your return codes
"""

# ---- tof
# --------------------
if __name__ == "__main__":
    # ----- see the demo at the end of file
    import main  # noqa  stops auto removal by pycln
# --------------------

from qtpy.QtWidgets import ( QCheckBox,
                             QDialog,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QVBoxLayout )

# ---- end imports


# ---- return codes
# 0 and 1 are what QDialog itself uses for reject and accept, so keeping
# them here means Esc and the window X land on RESULT_CANCEL for free.
# Add your own starting at 2.

RESULT_CANCEL   = 0
RESULT_OK       = 1
RESULT_SKIP     = 2


#  --------
class CustomDialog( QDialog ):
    """
    a modal dialog that returns one of the RESULT_* codes above
    """

    # -----------------------
    def __init__( self, parent = None, title = "Custom Dialog",
                  a_name = "", a_note = "", wants_email = False ):
        """
        build the dialog, the a_* arguments are the starting values
        shown in the fields
        """
        super().__init__( parent )

        self.setWindowTitle( title )
        self.setModal( True )

        self.start_name     = a_name
        self.start_note     = a_note
        self.start_email    = wants_email

        self.result_code    = RESULT_CANCEL   # until a button says otherwise

        self._build_gui()

    # -----------------------
    def _build_gui( self ):
        """
        the whole layout, in the same shape as a tab: widgets then buttons
        """
        layout      = QVBoxLayout( self )

        self._build_gui_widgets( layout )
        self._build_gui_msg(     layout )
        self._build_gui_buttons( layout )

        self.setMinimumWidth( 400 )

    # -----------------------
    def _build_gui_widgets( self, layout ):
        """
        the fields, replace these with your own
        """
        # ---- name
        row_layout  = QHBoxLayout()
        layout.addLayout( row_layout )

        widget      = QLabel( "name  " )
        row_layout.addWidget( widget )

        widget      = QLineEdit( self.start_name )
        self.name_edit  = widget
        widget.setMinimumWidth( 250 )
        row_layout.addWidget( widget )

        # ---- note
        row_layout  = QHBoxLayout()
        layout.addLayout( row_layout )

        widget      = QLabel( "note  " )
        row_layout.addWidget( widget )

        widget      = QLineEdit( self.start_note )
        self.note_edit  = widget
        widget.setMinimumWidth( 250 )
        row_layout.addWidget( widget )

        # ---- check box
        row_layout  = QHBoxLayout()
        layout.addLayout( row_layout )

        widget      = QCheckBox( "wants email" )
        self.email_check    = widget
        widget.setChecked( self.start_email )
        row_layout.addWidget( widget )

    # -----------------------
    def _build_gui_msg( self, layout ):
        """
        the line validate() writes its complaint on, empty most of the time
        """
        widget      = QLabel( "" )
        self.msg_widget = widget
        widget.setWordWrap( True )
        widget.setStyleSheet( "color: red;" )
        layout.addWidget( widget )

    # -----------------------
    def _build_gui_buttons( self, layout ):
        """
        plain push buttons, one method each, add your own here
        """
        row_layout  = QHBoxLayout()
        layout.addLayout( row_layout )

        row_layout.addStretch( 1 )      # push the buttons to the right

        widget      = QPushButton( "ok" )
        self.ok_button  = widget
        widget.setDefault( True )       # the return key presses this one
        widget.clicked.connect( self.on_ok )
        row_layout.addWidget( widget )

        widget      = QPushButton( "skip" )
        widget.clicked.connect( self.on_skip )
        row_layout.addWidget( widget )

        widget      = QPushButton( "cancel" )
        widget.clicked.connect( self.on_cancel )
        row_layout.addWidget( widget )

    # ---- what the buttons do

    # -----------------------
    def on_ok( self ):
        """
        validate first, a complaint keeps the dialog open
        """
        complaint   = self.validate()

        if complaint != "":
            self.msg_widget.setText( complaint )
            return

        self.finish( RESULT_OK )

    # -----------------------
    def on_skip( self ):
        """
        close with the skip code, no validation
        """
        self.finish( RESULT_SKIP )

    # -----------------------
    def on_cancel( self ):
        """
        close with the cancel code, no validation
        """
        self.finish( RESULT_CANCEL )

    # -----------------------
    def finish( self, result_code ):
        """
        remember the code and close, done() is what ends exec()
        """
        self.result_code    = result_code
        self.done( result_code )

    # -----------------------
    def validate( self ):
        """
        what counts as a good answer, return "" for good or the
        complaint to show the user
        """
        a_name      = self.name_edit.text().strip()

        if a_name == "":
            return ( "name cannot be empty" )

        return ( "" )

    # ---- reading the answer

    # -----------------------
    def get_values( self ):
        """
        the fields as a dict, valid whatever button was pressed
        """
        values      = { "name"          : self.name_edit.text().strip(),
                        "note"          : self.note_edit.text().strip(),
                        "wants_email"   : self.email_check.isChecked(), }

        return values

    # -----------------------
    def reject( self ):
        """
        Esc and the window X come here, not through a button, so make
        them mean cancel rather than leaving result_code stale
        """
        self.result_code    = RESULT_CANCEL
        super().reject()


# ------------------------------------
def ask_user( parent = None, title = "Custom Dialog",
              a_name = "", a_note = "", wants_email = False ):
    """
    build, show and read the dialog in one call
    returns ( result_code, values dict )
    """
    dialog      = CustomDialog( parent,
                                title       = title,
                                a_name      = a_name,
                                a_note      = a_note,
                                wants_email = wants_email )

    dialog.exec()       # blocks here until a button closes it
                        # exec() not exec_(), exec_ is gone in PyQt6

    result_code = dialog.result_code
    values      = dialog.get_values()

    return ( result_code, values )


# ------------------------------------
def demo():
    """
    run this file to see the dialog, delete when you no longer want it
    """
    import sys
    from qtpy.QtWidgets import QApplication

    app         = QApplication( sys.argv )

    result_code, values = ask_user( a_name  = "start value",
                                    a_note  = "edit me" )

    print( f"{result_code = }" )
    print( f"{values      = }" )


# --------------------
if __name__ == "__main__":
    demo()

# ---- eof
