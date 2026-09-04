#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
--- metadata here including WIKI_LINK as Constant ( not comment )


KEY_WORDS:      pythonguis Python GUIs Game
CLASS_NAME:     PguMineSweeperTab
WIDGETS:        QImage QPainter QPalette QFont
STATUS:         ??works at first blush
TAB_TITLE:      Minesweeper / Game
DESCRIPTION:    An minesweeper game from github pythonguis-examples
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/pythonguis/pythonguis-examples/blob/main/pyqt6/demos/minesweeper/README.md"

"""
Some Notes:  pythonguis

/mnt/8ball1/first6_root/russ/0000/python00/python3/_examples/pythonguis-examples-main/pyqt6/demos/minesweeper
"https://github.com/russ-hensel/pyqt_by_example/wiki/Pythonguis-Examples"

"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------



import random

import time


from qtpy.QtCore import QSize, Qt, Signal

from qtpy.QtCore  import Qt, QSize, Qt, QTimer

from qtpy.QtCore import Qt
from qtpy.QtCore import Qt


from qtpy.QtGui import QFont, QIcon, QPixmap


from qtpy.QtGui import (
    QPainter,
)




from qtpy.QtCore import (Qt)

from qtpy.QtGui import (QFont,
                        QPainter)

from qtpy.QtGui import (
                            QBrush,
                            QPainter,
                            QPalette,
                            QPen,
                            QPixmap,
                        )
from qtpy.QtWidgets import QWidget



from qtpy.QtWidgets import (QGridLayout,
                            QMainWindow,
                            QHBoxLayout,
                            QLabel,
                            QPushButton,
                            QVBoxLayout,
                            QWidget)

import tab_base
import utils_for_tabs as uft
import wat_inspector

# was qt6
#from MainWindow     import Ui_MainWindow
from qtpy.QtWidgets import QMainWindow

from constants import (
    IMG_BOMB,
    IMG_FLAG,
    IMG_START,
    NUM_COLORS,
)

from constants import (
    IMG_BOMB,
    IMG_CLOCK,
    LEVELS,
    STATUS_ICONS,
    Status,
)



# ---- end imports

print_func_header   = uft.print_func_header
# Calculator state.
READY = 0
INPUT = 1


from pathlib import Path
image_dir    = Path( __file__ ).parent
image_dir    = Path().joinpath( str( image_dir ), "images" )

# was in its own module in original demo widgets.py

class PositionSquare( QWidget ):
    expandable  = Signal(int, int)
    clicked     = Signal()
    ohno        = Signal()

    def __init__(self, x, y):
        super().__init__()

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.ColorRole.Window)
            outer, inner = color, color
        else:
            outer, inner = Qt.GlobalColor.gray, Qt.GlobalColor.lightGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            elif self.adjacent_n > 0:
                pen = QPen( NUM_COLORS[self.adjacent_n] )
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(
                    r,
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                    str(self.adjacent_n),
                )

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMG_FLAG))

    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton and not self.is_revealed:
            self.flag()

        elif e.button() == Qt.MouseButton.LeftButton:
            self.click()

            if self.is_mine:
                self.ohno.emit()


#-----------------------------------------------
class AMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.b_size, self.n_mines = LEVELS[1]

        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.clock = QLabel()
        self.clock.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight( QFont.Weight.Thin )
        self.mines.setFont(f)
        self.clock.setFont(f)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        self.mines.setText("%03d" % self.n_mines)
        self.clock.setText("000")

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon( f"{image_dir}/smiley.png" ) )
        self.button.setFlat(True)

        self.button.pressed.connect(self.button_pressed)

        label = QLabel()
        label.setPixmap(QPixmap.fromImage(IMG_BOMB))
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        hb.addWidget(label)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        label = QLabel()
        label.setPixmap(QPixmap.fromImage( IMG_CLOCK ))
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hb.addWidget(label)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.init_map()
        self.update_status(Status.READY)

        self.reset_map()
        self.update_status(Status.READY)

        self.setWindowTitle("Moonsweeper")

        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = PositionSquare(x, y)
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
                w.clicked.connect(self.trigger_start)
                w.expandable.connect(self.expand_reveal)
                w.ohno.connect(self.game_over)

    def reset_map(self):
        # Clear all mine positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()

        # Add mines to the positions
        positions = []
        while len(positions) < self.n_mines:
            x, y = (
                random.randint(0, self.b_size - 1),
                random.randint(0, self.b_size - 1),
            )
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        def get_adjacency_n(x, y):
            positions = self.get_surrounding(x, y)
            n_mines = sum(1 if w.is_mine else 0 for w in positions)

            return n_mines

        # Add adjacencies to the positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.adjacent_n = get_adjacency_n(x, y)

        # Place starting marker
        while True:
            x, y = (
                random.randint(0, self.b_size - 1),
                random.randint(0, self.b_size - 1),
            )
            w = self.grid.itemAtPosition(y, x).widget()
            # We don't want to start on a mine.
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_start = True

                # Reveal all positions around this, if they are not mines either.
                for w in self.get_surrounding(x, y):
                    if not w.is_mine:
                        w.click()
                break

    def get_surrounding(self, x, y):
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions

    def button_pressed(self):
        if self.status == Status.FAILED:
            self.update_status(Status.FAILED)
            self.reveal_map()

        elif self.status == Status.FAILED:
            self.update_status(Status.READY)
            self.reset_map()

    def reveal_map(self):
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reveal()

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def trigger_start(self, *args):
        if self.status != Status.PLAYING:
            # First click.
            self.update_status(Status.PLAYING)
            # Start timer.
            self._timer_start_nsecs = int(time.time())

    def update_status(self, status):
        self.status = status
        self.button.setIcon(QIcon(STATUS_ICONS[self.status]))

    def update_timer(self):
        if self.status == Status.PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)

    def game_over(self):
        self.reveal_map()
        self.update_status(Status.FAILED)


# -------------------------------
class PguMineSweeperTab( tab_base.TabBase ):
    """
    Examples for


    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK     # helps the link to the wiki

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]     = self.mutate_2
        # self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4

        self._build_gui()

    #--------------------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        This code is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        # ---- New Row
        # make a layout to put the buttons in
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )


        # ---- new row, for build_gui_last_buttons
        button_layout   = QHBoxLayout(   )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find ???

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "signal_sent()" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
            these mutations will try to mimic a typical default state
            of a widget for the first push button the
            second will not be modified by mutate_0

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_0()" )

        # ---- change widget
        msg    = "use next mutate to create calculator window "
        self.append_msg( msg, clear = False )


        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
            these mutations will try to mimic a typical default state
            of a widget for the first push button the
            second will not be modified by mutate_0

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_1()" )

        # ---- change widget
        msg    = "create Calculator"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        # widget          = self.q_push_button_1
        # widget.setText( "text set in mutate_0()" )
        # widget.width    = 300
        # widget.setToolTip( None )
        # widget.setStyleSheet( "" )
        # self.a_main_window   =  QMainWindow()
        self.calc_window  =  AMainWindow(   )
        # self.a_main_window.show()
        self.calc_window.show()



        self.append_msg( tab_base.DONE_MSG )


    # ------------------------
    def inspect(self):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them
        self_clock_widget   = self.clock_widget

        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tab's code

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
