#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 11:24:39 2026

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------




import sys
import os

print("--- Diagnostic Report ---")
print(f"Python Executable: {sys.executable}")

try:
    from PyQt5 import QtCore
    print(f"PyQt5 Version: {QtCore.PYQT_VERSION_STR}")
    print(f"Qt Version (at runtime): {QtCore.QT_VERSION_STR}")

    # This is the "secret sauce" - it shows where the binaries live
    lib_path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.LibrariesPath)
    plugins_path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath)

    print(f"\nQt Libraries Path: {lib_path}")
    print(f"Qt Plugins Path: {plugins_path}")

except ImportError as e:
    print(f"Error: Could not import PyQt5: {e}")

print("\n--- Environment Variables ---")
for var in ['QT_API', 'QT_SELECT', 'QT_PLUGIN_PATH', 'LD_LIBRARY_PATH']:
    print(f"{var}: {os.environ.get(var, 'Not Set')}")

# ---- eof

