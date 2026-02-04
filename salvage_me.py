#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 17:46:20 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports




# --------------------------------
def set_groupbox_style( groupbox ):
    """ """
    groupbox.setStyleSheet("""
        QGroupBox {
            border: 2px solid blue;
            border-radius: 10px;
            margin-top: 15px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: white;
        }
    """)




    # --------------------------
    def set_to_nonexxx( self, arg  ):
        """
        !!What it says
        """
        self.append_function_msg( "set_to_none" )

        self.line_edit_1_widget.set_preped_data( "xxx" )
        self.line_edit_1_widget.set_preped_data( None )
        self.line_edit_1_widget.setText( None  )   #
        raw_data    = self.line_edit_1_widget.get_raw_data(  )
        msg         = f"set then get from line_edit_1 {raw_data = }"
        self.append_msg( msg )

        print()
        self.line_edit_2_widget.set_preped_data( "xxx" )
        self.line_edit_2_widget.set_preped_data( None )
        self.line_edit_2_widget.setText( None  )
        msg         = f"{self.line_edit_2_widget.get_raw_data(  ) = }"
        self.append_msg( msg )

        try:
            self.date_edit_1_widget.set_preped_data( None )

        except Exception as an_except:
            print()
            msg     = f"a_except    >>{an_except}<<  type  >>{type( an_except)}<<"
            self.append_msg( msg )

            msg     = "self.date_edit_1_widget.set_preped_data( None ) raised this "
            self.append_msg( msg )

        try:
            self.date_edit_2_widget.set_preped_data( None )

        except Exception as an_except:
            print()
            msg     = f"a_except    >>{an_except}<<  type  >>{type( an_except)}<<"
            self.append_msg( msg )

            msg     = "self.date_edit_1_widget.set_preped_data( None ) raised this "
            self.append_msg( msg )

#-------------------------------

   # --------------------------
   def mutate_to_refactro( self, arg  ):
       """
       What it says
       """
       self.append_function_msg( f"mutate { self.mutate_ix = }" )

       max_mutate   = 3   # match to if.......
       mutate_ix    = self.mutate_ix

       if   mutate_ix == 0:

           self.text_edit_widget.setText( f"{mutate_ix=}" )
           data   = self.text_edit_widget.toPlainText()
           msg         = f"set then get from self.text_edit_widget {data = }"
           print( msg )

           self.line_edit_1_widget.setText(  f"{mutate_ix=}" )  #
           rdata    = self.line_edit_1_widget.text(  )
           msg         = f"set then get from line_edit_1 {data = }"
           self.append_msg( msg )

           # # this is the general method
           # in_data      = f"some string data {mutate_ix =}"
           # in_type      = "string"             # a list includes  string  "integer", "timestamp" ):
           # self.text_edit_widget.set_data(   in_data, in_type )

       elif mutate_ix == 1:

           self.text_edit_widget.setText( f"{mutate_ix=}" )

           data   = self.text_edit_widget.toPlainText()
           msg         = f"set then get from self.text_edit_widget {data = }"
           self.append_msg( msg )

           self.line_edit_1_widget.setText(  f"{mutate_ix=}" )  #
           rdata    = self.line_edit_1_widget.text(  )
           msg         = f"set then get from line_edit_1 {data = }"
           print( msg )


           # # this is the general method
           # in_data      = f"some string data {mutate_ix =}"
           # in_type      = "string"             # a list includes  string  "integer", "timestamp" ):
           # self.text_edit_widget.set_data(   in_data, in_type )

       elif self.mutate_ix == 2:
           msg      = "set to none and like"
           self.append_msg( msg )

           self.text_edit_widget.setText( f"{mutate_ix=} for set to None" )

           try:
               self.line_edit_1_widget.setText( None )

           except Exception as an_except:
               self.append_msg( " " )
               msg     = f"a_except    >>{an_except}<<  type  >>{type( an_except)}<<"
               self.append_msg( msg )

               msg     = "self.line_edit_1_widget.setText( None ) raised this "
               self.append_msg( msg )



       elif self.mutate_ix == 3:
           self.text_edit_widget.set_preped_data( f"{mutate_ix=} set -> xxx -> None" )

           self.text_edit_widget.set_preped_data( "xxx" )
           self.line_edit_1_widget.set_preped_data( None )
           raw_data    = self.line_edit_1_widget.get_raw_data(  )
           msg         = f"set then get from text_edit_widget {raw_data = }"
           self.append_msg(  msg )


           self.line_edit_1_widget.set_preped_data( "xxx" )
           self.line_edit_1_widget.set_preped_data( None )
           #self.line_edit_1_widget.setText( None  )   #
           raw_data    = self.line_edit_1_widget.get_raw_data(  )
           msg         = f"set then get from line_edit_1 {raw_data = }"
           self.append_msg( msg )

           # this is the general method
           in_data      = f"some string data {mutate_ix =}"
           in_type      = "string"             # a list includes  string  "integer", "timestamp" ):
           self.text_edit_widget.set_data(   in_data, in_type )

       self.mutate_ix         += 1
       if self.mutate_ix >= max_mutate:
           msg   = f"hit {max_mutate = } wrap to 0 *******"
           self.append_msg(  msg )
           self.mutate_ix  = 0



    # ------------------------
    def _build_gui_in_gb_edit(self, layout  ):
        """
        build some of the gui in a groupbox
        """
        lbl_stretch         = self.lbl_stretch
        widget_stretch      = self.widget_stretch

        # ---- CQLineEdit
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QLineEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = QLineEdit(  self,   )
        widget.setReadOnly( False )
        self.line_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQLineEdit_2
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QLineEdit_2")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = QLineEdit(  self,   )
        self.line_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQTextEdit
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        # widget            = QLabel( "QTextEdit")
        # b_layout.addWidget( widget,  stretch = lbl_stretch )

        # widget              = custom_widgets.QTextEdit(  self,  )
        # self.text_edit_widget = widget
        # b_layout.addWidget( widget,  stretch = widget_stretch )


        # ---- CQDateEdit_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QDateEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        # widget              = custom_widgets.CQDateEdit(  self,   )
        # self.date_edit_1_widget = widget
        # b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateEdit_n
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "QDateEdit_n:")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        # widget            = custom_widgets.QDateEdit(  self,   )
        # self.date_edit_2_widget = widget
        # b_layout.addWidget( widget,  stretch = self.widget_stretch )




# ---- eof