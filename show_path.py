#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
show_path.py -- print $PATH, one directory per line

The python version of show_path.sh, same output.

The process inherits PATH from the terminal that runs it, so what
you see here is what that terminal would search for a command.

    ./show_path.py          numbered list, marks dirs that are missing
    ./show_path.py -p       plain, one bare directory per line, good for piping

An empty entry in PATH ( "::" or a leading/trailing ":" ) means the
current directory, so it is called out rather than printed as nothing.
"""

# ---- tof

import os
import sys


# ------------------------------------
def get_path_dirs():
    """
    PATH as a list of strings, may include "" entries

    os.pathsep is ":" on linux, ";" on windows, so this is
    the portable split
    """
    a_path      = os.environ.get( "PATH", "" )
    return a_path.split( os.pathsep )


# ------------------------------------
def note_for_dir( a_dir ):
    """
    the "<-- something" tail for one directory, "" when
    there is nothing to say about it
    """
    if a_dir == "":
        return ( "  <-- empty entry, means the current directory" )

    if not os.path.isdir( a_dir ):
        return ( "  <-- does not exist" )

    if not os.access( a_dir, os.X_OK ):
        return ( "  <-- not searchable" )

    return ( "" )


# ------------------------------------
def show_path( plain = False ):
    """
    do the printing
    """
    dirs    = get_path_dirs()

    for ix, i_dir in enumerate( dirs, start = 1 ):

        if plain:
            print( i_dir )
            continue

        note    = note_for_dir( i_dir )
        print( f"{ix:2d}  {i_dir}{note}" )


# ------------------------------------
def main():
    """
    -p for the plain listing, anything else and we explain ourselves
    """
    args    = sys.argv[ 1: ]

    if args == []:
        show_path( plain = False )

    elif args == [ "-p" ]:
        show_path( plain = True )

    else:
        print( __doc__.strip() )
        return 2

    return 0


# --------------------
if __name__ == "__main__":
    sys.exit( main() )

# ---- eof
