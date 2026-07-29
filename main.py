# -*- coding: utf-8 -*-
"""
launcher for the app


"""


import os
import sys

# vaapisink can't render surfaces on this machine (i965 + intel-media-va-driver
# both installed) -- rank it and vaapi decode elements down so gstreamer
# autoplugs a working software sink instead of erroring out on video playback.
os.environ["GST_PLUGIN_FEATURE_RANK"] = "vaapisink:0,vaapidecodebin:0,vaapidecode:0"

import adjust_path   # noqa  stops auto removal by pycln

# QtWebEngineWidgets ( used by tabs/experiments/tab_webengine_widget.py ) must be
# imported -- or Qt.AA_ShareOpenGLContexts set -- before the QApplication is
# constructed in pyqt_by_example.main(). Import it here, early, as a one line
# side-effecting import so that later, lazy import doesn't blow up.
import qtpy.QtWebEngineWidgets   # noqa  import-only, required before QApplication()

# Get the directory of the current .py file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)
print(os.getcwd())  # Prints the new working directory

import pyqt_by_example


print( f"sys.argv  = >>>{sys.argv}<<< ")

pyqt_by_example.main()

# ---- eof


