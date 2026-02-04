#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lets use the module name, pyly /help/ and .txt
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof


"ex_h.__file__"

print( __file__ )


class TestClass():

    def __init__( self ):

        print( __file__ )
        self.file     = __file__

        #class_name             = str( type( self ) ).lower()
        #print( class_name )
        #<class 'tab_checkbox.qcheckboxtab'>
        splits                 = self.file.split( "/" )
        #self.help_file_name    = splits[ 1 ].replace( ".", "__") + ".txt"
        #self.help_file_name    = splits[ 1 ] + ".txt"

        file_path           = "/".join( splits[ 0:-1 ]  )
        print( f"{file_path =}" )
        file_name           = splits[ -1 ].split( "." )[0] + ".txt"
        print( f"{file_name =}" )
        file_path           =  file_path + "/help/" + file_name
        print( f"{file_path =}" )
        # splits                = class_name.split( "." )
        # #class_name            = splits[1]
        # self.help_file_name    = splits[ 1 ] + ".txt"

x = TestClass()