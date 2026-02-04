#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:01:21 2024

global variables only ( perhaps sets for them so no monky patch)
only use the set methods so we can track errors
this belongs to qt_by_example

import global_vars
global_vars.CONTROLLER


"""

# ---- tof


SAMPLE_DB_OBJ   = None    # not the connection but the object
TAB_DB_BUILDER  = None    # conndetion to tab db
CONTROLLER      = None    #
TAB_DB          = None    # global_vars.TAB_DB  the db connection for tab search
                          # not clear it needs to be here
EX_DB           = None    # db vor the examples global_vars.EX_DB
    # global_vars.EX_DB
#APP_SERVICES    = None

DEBUG_FUNC      = None





def set_ex_db( obj ):
    """
    global_vars.EX_DB

    """
    global EX_DB
    print( "set_ex_db allow reset " )
    if EX_DB:
        pass
        # 1/0
    EX_DB  = obj
    print_vars()



def set_sample_db_obj( obj ):
    """
    global_vars.SAMPLE_DB_OBJ  =
    """
    global SAMPLE_DB_OBJ
    print( "set_sample_db_obj" )
    if SAMPLE_DB_OBJ:
        1/0
    SAMPLE_DB_OBJ  = obj
    print_vars()


def set_tab_db( db ):
    """
    global_vars.TAB_DB  =
    """
    global TAB_DB
    print( "set_tab_db" )
    if TAB_DB:
        # 1/0
        return
    TAB_DB  = db
    print_vars()

def set_controller( controller ):
    global CONTROLLER
    print( "set_controller" )
    if CONTROLLER:
        #1/0
        # might be or not an error
        return
    CONTROLLER  = controller
    print_vars()

def set_tab_db_builder(  tdbb ):
    global TAB_DB_BUILDER
    print( "set_tab_db_builder" )
    if TAB_DB_BUILDER:
        1/0
    TAB_DB_BUILDER  = tdbb
    print_vars()

# def set_app_services(  var ):
#     global APP_SERVICES
#     print( "set_tab_db_builder" )
#     if APP_SERVICES: = }")
#         1/0
#     APP_SERVICES  = var
#     print_vars()



def print_vars(    ):

    return     # to silence this use return

    print( "qt_by_example  global_vars  vars now")
    print( f"{TAB_DB = }")
    print( f"{CONTROLLER = }")
    print( f"{TAB_DB_BUILDER = }")
    print( f"{SAMPLE_DB_OBJ = }")

# ---- and many more


# --- eof
