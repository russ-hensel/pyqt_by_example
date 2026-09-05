#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""


KEY_WORDS:      signals
CLASS_NAME:     QSignalsTab
WIDGETS:        QWidget
STATUS:         in dev am mess from pushbutton
TAB_TITLE:      Signals / Reference
DESCRIPTION:    A reference Signals, need work for the QPushButton widget
HOW_COMPLETE:   15 #  AND A COMMENT -- =<10 major probs  =<15 runs but =<20 fair not finished <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QPushButtons"

"""
Some Notes:

Home · russ-hensel/pyqt_by_example Wiki
https://github.com/russ-hensel/pyqt_by_example/wiki


What We Know About QPushButtons · russ-hensel/pyqt_by_example Wiki
https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QPushButtons


"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------


import time

from qtpy.QtCore import ( QEvent, Qt, Signal )

from qtpy.QtWidgets import ( QHBoxLayout,
                             QLabel,
                             QMenu,
                             QPushButton,
                             QWidget,
                             QVBoxLayout
                             )



import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class EventWidget( QWidget ):
    """
    plain QWidget has no signals for focus/mouse-over/click -- those only
    arrive as *events* ( focusInEvent(), enterEvent(), etc ), which a
    widget has to override to notice at all. this subclass overrides the
    ones we want and re-emits each as a Signal, so a host tab can
    .connect() to it just like a QPushButton's clicked signal
    """

    focus_in_signal         = Signal( int )         # reason -- Qt.FocusReason, see QFocusEvent.reason()
    focus_out_signal        = Signal( int )         # reason -- Qt.FocusReason, see QFocusEvent.reason()
    mouse_enter_signal      = Signal( int, int )    # x, y -- widget-relative, mouse entered the widget -- "mouse over" start
    mouse_leave_signal      = Signal()              # QEvent.Leave carries no position -- mouse left the widget -- "mouse over" end
    mouse_press_signal      = Signal( int, int, int )    # x, y, button -- Qt.MouseButton, see QMouseEvent.button()
    mouse_release_signal    = Signal( int, int, int )    # x, y, button -- Qt.MouseButton, see QMouseEvent.button()
    mouse_move_signal       = Signal( int, int )    # x, y -- widget-relative

    MOUSE_MOVE_THROTTLE_SEC = 0.2    # min gap between mouse_move_signal emits -- see mouseMoveEvent()

    def __init__( self, parent = None ):
        """
        """
        super().__init__( parent )

        # QWidget defaults to Qt.NoFocus -- without this it can never
        # become focused ( by click or Tab ), so focusInEvent/
        # focusOutEvent below would never fire
        self.setFocusPolicy( Qt.StrongFocus )

        # without this, mouseMoveEvent() only fires while a button is
        # held down -- this makes it fire on every move, button or not
        self.setMouseTracking( True )

        self.last_mouse_move_time = 0.0    # monotonic clock, see mouseMoveEvent()

        # a plain QWidget() auto-paints its stylesheet background/border,
        # but a QWidget SUBCLASS does not -- Qt assumes a subclass will do
        # its own custom painting in paintEvent() and skips the stylesheet
        # background unless this attribute opts back in. without it,
        # qwidget_2's green background/border would silently not paint
        self.setAttribute( Qt.WA_StyledBackground, True )

    # -------------------------------------
    def focusInEvent( self, event ):
        """
        what it says -- forwards event.reason(), a Qt.FocusReason
            event
                info on the event, we could send the whole thing forward
                but we just send .reason, this is a choice ...
                similar in other functions
        """
        self.focus_in_signal.emit( int( event.reason() ) )
        super().focusInEvent( event )

    # -------------------------------------
    def focusOutEvent( self, event ):
        """ what it says -- forwards event.reason(), a Qt.FocusReason """
        self.focus_out_signal.emit( int( event.reason() ) )
        super().focusOutEvent( event )

    # -------------------------------------
    def enterEvent( self, event ):
        """ what it says -- mouse entered the widget's area, forwards widget-relative x, y """
        pos    = event.pos()
        self.mouse_enter_signal.emit( pos.x(), pos.y() )
        super().enterEvent( event )

    # -------------------------------------
    def leaveEvent( self, event ):
        """
        what it says -- mouse left the widget's area

        QEvent.Leave carries no position -- unlike enterEvent()'s
        QEnterEvent, there is nothing here to forward
        """
        self.mouse_leave_signal.emit()
        super().leaveEvent( event )

    # -------------------------------------
    def mousePressEvent( self, event ):
        """ what it says -- forwards widget-relative x, y and event.button(), a Qt.MouseButton """
        pos    = event.pos()
        self.mouse_press_signal.emit( pos.x(), pos.y(), int( event.button() ) )
        super().mousePressEvent( event )

    # -------------------------------------
    def mouseReleaseEvent( self, event ):
        """ what it says -- forwards widget-relative x, y and event.button(), a Qt.MouseButton """
        pos    = event.pos()
        self.mouse_release_signal.emit( pos.x(), pos.y(), int( event.button() ) )
        super().mouseReleaseEvent( event )

    # -------------------------------------
    def mouseMoveEvent( self, event ):
        """
        what it says -- fires continuously ( see setMouseTracking() above ),
        far faster than MOUSE_MOVE_THROTTLE_SEC, so only emit the signal
        at most once per throttle window instead of flooding whatever is
        connected ( e.g. the tab's message log ) with every pixel of movement
        """
        now                  = time.monotonic()
        if now - self.last_mouse_move_time >= self.MOUSE_MOVE_THROTTLE_SEC:
            self.last_mouse_move_time    = now
            pos                          = event.pos()
            self.mouse_move_signal.emit( pos.x(), pos.y() )

        super().mouseMoveEvent( event )


#  --------
class QSignalsTab( tab_base.TabBase ):
    """
    Reference examples for some typical signals


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
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        self.mutate_dict[4]     = self.mutate_4

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

        # # ---- new row c -- testing never used
        # row_layout          = QHBoxLayout(   )
        # layout.addLayout( row_layout )

        # ---- New Row button_1 and _2 ....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # a label that points to q_pbutton_1
        widget          = QLabel( "q_pbutton_1 -> ", alignment=Qt.AlignRight )
            # no instance variable as we will not use after __init__

        # layout ( add to the windows ) the widget
        row_layout.addWidget( widget )

        # we use a local variable, widget, because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
            # if we need an instance variable we do an assignment as here
        widget                  = QPushButton( "q_pbutton_1" )
        self.q_push_button_1    = widget
            # save a reference for later use

        # this function, the "connect_to" will be called when the button is clicked
        # the code is a little indirect, do on one line if you wish
        connect_to              = self.pb_1_clicked
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        widget                  = QLabel( "q_pbutton_2 -> ", alignment = Qt.AlignRight )
        row_layout.addWidget( widget )

        widget                  = QPushButton( "q_pbutton_2" )
        self.q_push_button_2    = widget
        connect_to              = self.pb_2_clicked
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget, )

        # ---- widget
        widget                  = QWidget(   )
        self.qwidget_1          = widget
        widget.setFixedSize( 80, 40 )
        widget.setStyleSheet( "background-color: red; border: 2px solid black;" )

        # qwidget_1 stays a PLAIN QWidget -- no EventWidget subclass, no
            # overridden focusInEvent()/mousePressEvent()/etc. installEventFilter()
            # is Qt's built-in way to watch another object's events without
            # subclassing it: notify() offers installed filters first look at
            # every event before the widget's own handler runs. turns out
            # every event we handled for qwidget_2 -- focus, enter/leave,
            # press/release, move -- is filterable this way, so there were no
            # events left over that actually required subclassing
        widget.setFocusPolicy( Qt.StrongFocus )    # plain setter -- still needed, or FocusIn/Out never fire
        widget.setMouseTracking( True )            # plain setter -- still needed, or MouseMove only fires while a button is down
        widget.installEventFilter( self )
        self.qwidget_1_last_move_time = 0.0        # throttle state for eventFilter()'s MouseMove case

        row_layout.addWidget( widget, )

        # ---- widget subclassed
        widget                  = EventWidget(   )
        self.qwidget_2          = widget
        widget.setFixedSize( 80, 40 )
        widget.setStyleSheet( "background-color: green; border: none;" )
        widget.focus_in_signal.connect(      self.q2_focus_in )
        widget.focus_out_signal.connect(     self.q2_focus_out )
        widget.mouse_enter_signal.connect(   self.q2_mouse_enter )
        widget.mouse_leave_signal.connect(   self.q2_mouse_leave )
        widget.mouse_press_signal.connect(   self.q2_mouse_press )
        widget.mouse_release_signal.connect( self.q2_mouse_release )
        widget.mouse_move_signal.connect(    self.q2_mouse_move )
        row_layout.addWidget( widget, )

        # ---- new row, for build_gui_last_buttons
        button_layout           = QHBoxLayout( )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some standard buttons
        self.build_gui_last_buttons( button_layout )

    #----------------------------
    def get_button_style_sheet( self ):
        """
        what it says

        when applied to a button changes a bit of its appearance

        this is important content for the widgets referenced on this tab
        """
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """
        # i do not know what the default state, perhaps wat_inspector can tell

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

    # ---- connects signals...   --------
    # --------------------------
    def return_pressed( self ):
        """
        what is says  -- not connected, delete?

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "return_pressed()" )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def pb_1_clicked( self ):
        """
        What it says

            this function may be connected to a button normally
            q_push_button_1

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "pb_1_clicked()" )
        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def pb_2_clicked( self ):
        """
        What it says

            this function may be connected to a button: normally
            q_push_button_1

        this code is important content for the widgets referenced on this tab
        """
        self.append_msg( "pb_2_clicked()" )

        self.append_msg( tab_base.DONE_MSG  )

    # ---- qwidget_2 ( EventWidget ) event handlers -----
    # ------------------------------------
    def q2_focus_in( self, reason ):
        """
        Args:
            reason -- Qt.FocusReason ( as int ), from EventWidget.focus_in_signal,
                      Signal( int )
        """
        self.append_msg( f"q2_focus_in() {reason = }" )

    # ------------------------------------
    def q2_focus_out( self, reason ):
        """
        Args:
            reason -- Qt.FocusReason ( as int ), from EventWidget.focus_out_signal,
                      Signal( int )
        """
        self.append_msg( f"q2_focus_out() {reason = }" )

    # ------------------------------------
    def q2_mouse_enter( self, x, y ):
        """
        Args:
            x, y -- widget-relative mouse position, from EventWidget.mouse_enter_signal,
                    Signal( int, int )
        """
        self.append_msg( f"q2_mouse_enter() {x = } {y = }" )

    # ------------------------------------
    def q2_mouse_leave( self ):
        """
        Args: none -- connected to EventWidget.mouse_leave_signal, Signal() carries no payload
                      ( QEvent.Leave itself carries no position to forward )
        """
        self.append_msg( "q2_mouse_leave()" )

    # ------------------------------------
    def q2_mouse_press( self, x, y, button ):
        """
        Args:
            x, y   -- widget-relative mouse position
            button -- Qt.MouseButton ( as int ) that was pressed
            from EventWidget.mouse_press_signal, Signal( int, int, int )
        """
        self.append_msg( f"q2_mouse_press() {x = } {y = } {button = }" )

    # ------------------------------------
    def q2_mouse_release( self, x, y, button ):
        """
        Args:
            x, y   -- widget-relative mouse position
            button -- Qt.MouseButton ( as int ) that was released
            from EventWidget.mouse_release_signal, Signal( int, int, int )
        """
        self.append_msg( f"q2_mouse_release() {x = } {y = } {button = }" )

    # ------------------------------------
    def q2_mouse_move( self, x, y ):
        """
        Args:
            x, y -- widget-relative mouse position, from EventWidget.mouse_move_signal,
                    Signal( int, int )
        """
        self.append_msg( f"q2_mouse_move() {x = } {y = }" )

    # ---- qwidget_1 ( plain QWidget ) event handlers, via eventFilter() ----
    # ------------------------------------
    def eventFilter( self, obj, event ):
        """
        read it -- Qt calls this on every event bound for any object we
        installed ourselves as a filter on ( here just self.qwidget_1 ),
        before that object's own event handler runs. this is what lets us
        watch qwidget_1's events without subclassing it, unlike qwidget_2/
        EventWidget above

            obj
            event


            lets limit ourselves to eventFilter( self, obj, event ): whare are obj and event what can we get from them

            In eventFilter( self, obj, event ) (tab_q_signals.py:439):

            obj — the QObject (here always a QWidget) that had installEventFilter(self) called on it, i.e. whichever object this event was actually headed for. In this file that's only ever self.qwidget_1 (installed at line
            ~259), checked with if obj is self.qwidget_1: (line 447). Since it's just a reference to the real widget, you can call anything on it — obj.objectName(), obj.pos(), obj.geometry(), obj.hasFocus(), obj.underMouse(),
            etc. If you'd installed the filter on multiple widgets, obj is how you'd tell them apart.

            event — a QEvent (or subclass) instance describing what happened. Every event, regardless of type, gives you:
            - event.type() — a QEvent.Type enum value (QEvent.FocusIn, QEvent.MouseButtonPress, etc.) — this is what the if/elif chain in the code switches on (line 448 onward).
            - event.spontaneous() — whether it came from the OS/window system vs. was posted programmatically.
            - event.accept() / event.ignore() / event.isAccepted() — bookkeeping for whether the event was handled (matters more for things like QCloseEvent; not used in this file).

            Beyond that, Qt actually constructs a more specific subclass depending on type(), and that subclass has extra fields — which is exactly what the recent edit started pulling out:
            - QEvent.FocusIn / QEvent.FocusOut → the object is a QFocusEvent, adding .reason() (a Qt.FocusReason: mouse click, Tab key, active-window change, popup, shortcut, menu bar, etc.).
            - QEvent.Enter → a QEnterEvent, adding .pos() (widget-relative position) and .globalPos().
            - QEvent.Leave → stays a plain QEvent — no position field exists on it at all.
            - QEvent.MouseButtonPress / QEvent.MouseButtonRelease / QEvent.MouseMove → a QMouseEvent, adding .pos()/.globalPos(), .button() (the one button that triggered this event), .buttons() (all buttons currently held), and
            .modifiers() (Shift/Ctrl/Alt held at the time) — .modifiers() isn't currently read anywhere in this file, but it's there if you wanted it.

            So obj tells you who the event is for, event tells you what kind of event and, via its concrete subclass, the details specific to that kind.

            Crunched for 19s

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


        """
        if obj is self.qwidget_1:
            event_type      = event.type()

            if event_type == QEvent.FocusIn:
                self.q1_focus_in( int( event.reason() ) )
            elif event_type == QEvent.FocusOut:
                self.q1_focus_out( int( event.reason() ) )
            elif event_type == QEvent.Enter:
                pos     = event.pos()
                self.q1_mouse_enter( pos.x(), pos.y() )
            elif event_type == QEvent.Leave:
                # QEvent.Leave carries no position -- unlike Enter, there is
                # nothing here to forward
                self.q1_mouse_leave()
            elif event_type == QEvent.MouseButtonPress:
                pos     = event.pos()
                self.q1_mouse_press( pos.x(), pos.y(), int( event.button() ) )
            elif event_type == QEvent.MouseButtonRelease:
                pos     = event.pos()
                self.q1_mouse_release( pos.x(), pos.y(), int( event.button() ) )
            elif event_type == QEvent.MouseMove:
                # throttled the same way EventWidget.mouseMoveEvent() is,
                # just with the state kept on self instead of on the widget
                now     = time.monotonic()
                if now - self.qwidget_1_last_move_time >= EventWidget.MOUSE_MOVE_THROTTLE_SEC:
                    self.qwidget_1_last_move_time  = now
                    pos                            = event.pos()
                    self.q1_mouse_move( pos.x(), pos.y() )

        return super().eventFilter( obj, event )

    # ------------------------------------
    def q1_focus_in( self, reason ):
        """
        Args:
            reason -- Qt.FocusReason ( as int ), from the QFocusEvent seen by
                      eventFilter() on QEvent.FocusIn, not a signal
        """
        self.append_msg( f"q1_focus_in() {reason = }" )

    # ------------------------------------
    def q1_focus_out( self, reason ):
        """
        Args:
            reason -- Qt.FocusReason ( as int ), from the QFocusEvent seen by
                      eventFilter() on QEvent.FocusOut, not a signal
        """
        self.append_msg( f"q1_focus_out() {reason = }" )

    # ------------------------------------
    def q1_mouse_enter( self, x, y ):
        """
        Args:
            x, y -- widget-relative mouse position, from the event seen by
                    eventFilter() on QEvent.Enter, not a signal
        """
        self.append_msg( f"q1_mouse_enter() {x = } {y = }" )

    # ------------------------------------
    def q1_mouse_leave( self ):
        """
        Args: none -- called directly from eventFilter() on QEvent.Leave, not a signal
                      ( QEvent.Leave itself carries no position to forward )
        """
        self.append_msg( "q1_mouse_leave()" )

    # ------------------------------------
    def q1_mouse_press( self, x, y, button ):
        """
        Args:
            x, y   -- widget-relative mouse position
            button -- Qt.MouseButton ( as int ) that was pressed
            from the event seen by eventFilter() on QEvent.MouseButtonPress, not a signal
        """
        self.append_msg( f"q1_mouse_press() {x = } {y = } {button = }" )

    # ------------------------------------
    def q1_mouse_release( self, x, y, button ):
        """
        Args:
            x, y   -- widget-relative mouse position
            button -- Qt.MouseButton ( as int ) that was released
            from the event seen by eventFilter() on QEvent.MouseButtonRelease, not a signal
        """
        self.append_msg( f"q1_mouse_release() {x = } {y = } {button = }" )

    # ------------------------------------
    def q1_mouse_move( self, x, y ):
        """
        Args:
            x, y -- widget-relative mouse position, passed by eventFilter()
                    on QEvent.MouseMove, not a signal
        """
        self.append_msg( f"q1_mouse_move() {x = } {y = }" )

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
        msg    = "for q_push_button_1 we more or less reset it"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        widget          = self.q_push_button_1
        widget.setText( "text set in mutate_0()" )
        widget.width    = 300
        widget.setToolTip( None )
        widget.setStyleSheet( "" )

        # ---- change widget
        msg             = "for q_push_button_2 no mutations"
        self.append_msg( msg, )

        widget          = self.q_push_button_2
        # self.q_push_button_1.setDisabled( True )
        # self.q_push_button_2.setDisabled( False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_1()" )
        # msg    = "begin implementation"
        # self.append_msg( msg, clear     = False )
        # for self.q_push_button_1

        msg         = "mess with q_push_button_1"
        self.append_msg( msg, )

        widget      = self.q_push_button_1
            # it is often convenient to use a local variable,
            # you will see this a lot in our code, it does not seem to
            # be typical but we think it should be

        msg         = "q_push_button_1 set a tool tip"
        self.append_msg( msg, )

        widget.setToolTip( "this is a tool tip" )
        widget.setText( "text set in \nmutate_1()" )
            # note \n above
        widget.width     = 200

        # ---- change widget
        msg         = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        # ---- self.q_push_button_2
        widget      = self.q_push_button_2
        # msg    = "setChecked(True )"
        # self.append_msg( msg, )

        # msg        = f"{self.q_push_button_1.isChecked() = } "
        # self.append_msg( msg, )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_2()" )

        msg         = "change some attributes..."
        self.append_msg( msg,  )

        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setVisible( False )

        msg         = "q_push_button_1 mess with checkable enabled..."
        self.append_msg( msg,  )

        self.q_push_button_1.setCheckable( True )
        self.q_push_button_1.setChecked( True )
        self.q_push_button_1.setDisabled( True )

        self.q_push_button_1.setVisible( True )

        # next does not seem to work
        self.q_push_button_1.setCheckable( True )

        # ---- change widget
        msg         = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        widget      = self.q_push_button_2
        widget.setCheckable( True )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_3()" )

        msg    = "re-enable some stuff -- change attributes"
        self.append_msg( msg, clear = False )

        # ---- first widget
        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setDisabled( False )
        self.q_push_button_1.setVisible( True )
        self.q_push_button_1.setCheckable( True )
        self.q_push_button_1.toggle()

        msg    = "add menu to q_push_button_1"
        self.append_msg( msg, clear = False )

        menu        = QMenu(self)
        menu.addAction("Option 1")
        menu.addAction("Option 2")
        widget.setMenu( menu )

        # ---- change widget
        widget      = self.q_push_button_2
        msg         = "\nsome changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        msg         = "q_push_button_2 mess with style sheet... hover ... color "
        self.append_msg( msg,  )

        widget.setCheckable( False )
        widget.setStyleSheet( self.get_button_style_sheet() )
        msg         = f"get style sheet from widget \n {widget.styleSheet()}"
        self.append_msg( msg,  )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- mutate the widgets

        this is important content for the widgets referenced on this tab
        """
        self.append_function_msg( "mutate_4()" )

        msg         = "undo many of earlier mutations"
        self.append_msg( msg, clear = False )

        widget      = self.q_push_button_1
        self.q_push_button_1.setText( "one line")
        self.q_push_button_1.width     = 500
        self.q_push_button_1.setDisabled( False )
        self.q_push_button_1.setVisible( True )
        self.q_push_button_1.setCheckable( True )

        # seems to make togable, how to turn off
        #self.q_push_button_1.toggle()

        msg    = "add menu to q_push_button_1"
        self.append_msg( msg, clear = False )
        menu        = QMenu(self)
        menu.addAction( "Menu Option 1" )
        menu.addAction( "Menu Option 2" )
        # try to clear the menu
        widget.setMenu( None )

        # ---- change widget
        widget      = self.q_push_button_2
        msg         = "some changes to q_push_button_2"
        self.append_msg( msg, clear = False )

        widget.setStyleSheet( "" )
            # no style sheet

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
        self_q_push_button_1    = self.q_push_button_1
        self_q_push_button_2    = self.q_push_button_1

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
