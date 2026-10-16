#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
# we do not run from here has its own main, else run from the tab
#  /pyqt_by_example/tabs/more/tab_scale_slider.py
"""
scale_slider.py


a linear scale of integers with a pointer that sits on it --
a custom QAbstractSlider that does all its own painting.

built in steps:
    1   static painting: track, minor and major ticks, pointer at the value
    2   value <-> pixel mapping checked with the keyboard ( free from QAbstractSlider )
    3   mouse drag, click on the track  <-- here
    4   tick labels through a callable
    5   magnifier bubble while dragging

why QAbstractSlider and not QWidget:
    minimum, maximum, value, singleStep, pageStep, orientation, tracking,
    valueChanged / sliderMoved, keyboard and wheel handling all come for free.
    we only paint and handle the mouse.  sliderChange() already calls
    update(), so a setValue() repaints without any help from us.

    value vs sliderPosition:
        while the pointer is held down they can differ.  with tracking on ( the
        default ) value follows every move; with setTracking( False ) value
        only changes on release.  the pointer is always painted at
        sliderPosition, so it follows the mouse either way.

    the api, so far
        setRange( lo, hi ) setValue( v ) value() ...   all from QAbstractSlider
        set_major_tick_interval( n )     tall tick every n, 0 for none
        set_minor_tick_interval( n )     short tick every n, 0 for none
        value_to_pixel( value )          -> float x of that value on the track
        pixel_to_value( x )              -> nearest int value, clamped to the range
        text_from_value( value )         -> the text over the pointer, str( value ) unless
                                         changed; "" or None hides it.  override it in a
                                         subclass, like QSpinBox.textFromValue, or ...
        set_text_function( fn )          ... hand it a function int -> str, None for plain
        click_jumps                      attribute, True: a click on the track jumps
                                         there and starts a drag, phone style
                                         False: a click pages toward it, QSlider style

    mouse, left button only:
        press on the pointer             grab it, no jump -- the grab offset is kept
        drag                             sliderMoved, and valueChanged if tracking
        press elsewhere                  see click_jumps -- when paging, holding the
                                         button repeats until the pointer reaches the
                                         mouse, which may move meanwhile
        release                          sliderReleased, and valueChanged if not tracking
        escape during a drag             cancel, pointer back where the drag began
        hover over the pointer           open hand cursor, pointer lightens

    keys, all from QAbstractSlider, nothing of ours:
        left / right  up / down          singleStep
        page up / page down              pageStep
        home / end                       minimum / maximum
        mouse wheel                      singleStep * QApplication.wheelScrollLines()
                                         per notch, 3 by default, capped at pageStep

horizontal only for now -- the vertical orientation is ignored.

runs on its own for a look:
    python scale_slider.py

Qt5 and Qt6 both, every enum spelled the scoped way.
"""

import sys

from qtpy.QtCore import ( QPointF, QRectF, QSize, Qt, QTimer )
from qtpy.QtGui  import ( QColor, QFontMetrics, QPainter, QPalette, QPen, QPolygonF )
from qtpy.QtWidgets import ( QAbstractSlider,
                             QApplication,
                             QSizePolicy,
                             QVBoxLayout,
                             QWidget,
                             )

# ---- end imports

POINTER_WIDTH       = 14                # px, base of the pointer triangle
POINTER_HEIGHT      = 12                # px
MAJOR_TICK_LEN      = 12                # px, below the track
MINOR_TICK_LEN      = 6                 # px
TRACK_THICKNESS     = 3                 # px
MIN_MINOR_SPACING   = 3                 # px, closer than this and minor ticks are skipped
GAP                 = 3                 # px, general breathing room between bands
LABEL_BAND          = 16                # px, reserved under the ticks for step 4
HIT_SLOP            = 6                 # px, the pointer grabs this much wider than drawn
PAGE_REPEAT_DELAY   = 400               # ms, hold on the track this long before repeating
PAGE_REPEAT_EVERY   = 60                # ms, then one page step this often


# -----------------------------------------------
class ScaleSlider( QAbstractSlider ):
    """
    a horizontal integer scale with a pointer.

    vertical layout of the widget, top to bottom:
        value readout text
        pointer triangle, tip touching the track
        track line
        ticks hanging below the track
        label band ( empty until step 4 )
    """
    def __init__( self, parent = None ):
        """
        what it says -- defaults to 0 .. 100 at 50
        """
        super().__init__( parent )

        self.major_tick_interval    = 10
        self.minor_tick_interval    = 1
        self.click_jumps            = True     # False -> page toward the click

        self._drag_offset           = None     # None when not dragging, else px
        self._hover                 = False    # mouse over the pointer
        self._drag_start            = None     # sliderPosition when the drag began, for escape
        self._page_target_x         = None     # None when not paging, else mouse x

        self._page_timer            = QTimer( self )
        self._page_timer.timeout.connect( self._page_repeat )

        self._text_function         = None     # int -> str for the readout, see text_from_value

        self.setOrientation( Qt.Orientation.Horizontal )
        # self.setOrientation( Qt.Orientation.Vertical ) ignored
        self.setRange( 0, 100 )
        self.setValue( 50 )
        self.setSingleStep( 1 )
        self.setPageStep( 10 )

        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        self.setSizePolicy( QSizePolicy.Policy.Expanding,
                            QSizePolicy.Policy.Fixed )
        self.setMouseTracking( True )          # move events without a button, for hover

    # ---- readout text
    # ------------------------------------
    def set_text_function( self, text_function ):
        """
        text_function takes the int under the pointer and returns the text to
        show over it -- "" or None hides the readout.  None for the function
        itself goes back to the plain number
        """
        self._text_function     = text_function
        self.update()

    # ------------------------------------
    def text_from_value( self, value ):
        """
        the text over the pointer for value.  the same idea as
        QSpinBox.textFromValue: override this in a subclass, or use
        set_text_function to change it without one.
        value is sliderPosition, so the text follows a drag even with
        tracking off.  one line only, the readout band is one line high
        """
        if self._text_function is None:
            return ( str( value ) )
        text        = self._text_function( value )
        return ( "" if text is None else str( text ) )

    # ---- tick settings
    # ------------------------------------
    def set_major_tick_interval( self, interval ):
        """
        what it says, 0 for none
        """
        self.major_tick_interval    = max( 0, int( interval ) )
        self.update()

    # ------------------------------------
    def set_minor_tick_interval( self, interval ):
        """
        what it says, 0 for none
        """
        self.minor_tick_interval    = max( 0, int( interval ) )
        self.update()

    # ---- geometry
    # ------------------------------------
    def _margin( self ):
        """
        left and right margin -- half the pointer plus a little, so the
        pointer is never clipped at minimum or maximum
        """
        return POINTER_WIDTH / 2 + GAP

    # ------------------------------------
    def _text_height( self ):
        """
        what it says
        """
        return QFontMetrics( self.font() ).height()

    # ------------------------------------
    def _track_y( self ):
        """
        y of the track line, everything else hangs off this
        """
        return GAP + self._text_height() + GAP + POINTER_HEIGHT

    # ------------------------------------
    def value_to_pixel( self, value ):
        """
        x of value on the track, a float.
        one of the two central methods -- pixel_to_value comes in step 2
        """
        lo          = self.minimum()
        hi          = self.maximum()
        margin      = self._margin()
        span_px     = self.width() - 2 * margin

        if hi == lo:                    # degenerate range, park in the middle
            return margin + span_px / 2

        return margin + ( value - lo ) * span_px / ( hi - lo )

    # ------------------------------------
    def pixel_to_value( self, x ):
        """
        nearest integer value to pixel x, clamped to the range.
        the other central method -- the inverse of value_to_pixel,
        the mouse will use it in step 3
        """
        lo          = self.minimum()
        hi          = self.maximum()
        margin      = self._margin()
        span_px     = self.width() - 2 * margin

        if hi == lo or span_px <= 0:
            return lo

        value       = lo + ( x - margin ) * ( hi - lo ) / span_px
        value       = int( round( value ) )
        return min( max( value, lo ), hi )

    # ------------------------------------
    def _pointer_hit_rect( self ):
        """
        where a press grabs the pointer -- the triangle and the readout above
        it, widened by HIT_SLOP each side so a finger or a sloppy mouse works
        """
        x           = self.value_to_pixel( self.sliderPosition() )
        half        = POINTER_WIDTH / 2 + HIT_SLOP
        bottom      = self._track_y() + HIT_SLOP
        return QRectF( x - half, 0, 2 * half, bottom )

    # ------------------------------------
    def sizeHint( self ):
        """
        what it says -- width is only a suggestion, height is what we need
        """
        height      = ( self._track_y() + MAJOR_TICK_LEN + GAP
                        + LABEL_BAND + GAP )
        return QSize( 300, int( height ) )

    # ------------------------------------
    def minimumSizeHint( self ):
        """
        what it says
        """
        return QSize( 80, self.sizeHint().height() )

    # ---- painting
    # ------------------------------------
    def paintEvent( self, event ):
        """
        what it says -- order matters, pointer goes on top
        """
        painter     = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )

        self._paint_track( painter )
        self._paint_ticks( painter )
        self._paint_pointer( painter )

        painter.end()

    # ------------------------------------
    def _paint_track( self, painter ):
        """
        what it says
        """
        palette     = self.palette()
        track_y     = self._track_y()
        x_lo        = self.value_to_pixel( self.minimum() )
        x_hi        = self.value_to_pixel( self.maximum() )

        pen         = QPen( palette.color( QPalette.ColorRole.WindowText ) )
        pen.setWidth( TRACK_THICKNESS )
        pen.setCapStyle( Qt.PenCapStyle.FlatCap )
        painter.setPen( pen )
        painter.drawLine( QPointF( x_lo, track_y ), QPointF( x_hi, track_y ) )

    # ------------------------------------
    def _paint_ticks( self, painter ):
        """
        minor ticks are skipped when they would crowd closer than
        MIN_MINOR_SPACING px; major ticks are always drawn
        ticks start at the first multiple of the interval at or above minimum,
        so a range of 3 .. 47 still gets ticks on the tens
        """
        palette     = self.palette()
        lo          = self.minimum()
        hi          = self.maximum()
        track_y     = self._track_y() + TRACK_THICKNESS / 2

        pen         = QPen( palette.color( QPalette.ColorRole.WindowText ) )
        pen.setWidth( 1 )
        painter.setPen( pen )

        major       = self.major_tick_interval
        minor       = self.minor_tick_interval

        draw_minor  = False
        if minor and hi > lo:
            minor_px    = minor * ( self.value_to_pixel( hi ) - self.value_to_pixel( lo ) ) / ( hi - lo )
            draw_minor  = minor_px >= MIN_MINOR_SPACING

        if draw_minor:
            first       = -( -lo // minor ) * minor      # ceiling to a multiple
            for i_value in range( first, hi + 1, minor ):
                if major and i_value % major == 0:
                    continue                             # major tick draws it
                x       = self.value_to_pixel( i_value )
                painter.drawLine( QPointF( x, track_y ),
                                  QPointF( x, track_y + MINOR_TICK_LEN ) )

        if major:
            pen.setWidth( 2 )
            painter.setPen( pen )
            first       = -( -lo // major ) * major
            for i_value in range( first, hi + 1, major ):
                x       = self.value_to_pixel( i_value )
                painter.drawLine( QPointF( x, track_y ),
                                  QPointF( x, track_y + MAJOR_TICK_LEN ) )

    # ------------------------------------
    def _paint_pointer( self, painter ):
        """
        a downward triangle, tip on the track, with the value above it.
        highlight colour when we have focus, dimmed when disabled
        """
        palette     = self.palette()
        x           = self.value_to_pixel( self.sliderPosition() )
        track_y     = self._track_y()
        half        = POINTER_WIDTH / 2

        if not self.isEnabled():
            color   = palette.color( QPalette.ColorGroup.Disabled,
                                     QPalette.ColorRole.WindowText )
        else:
            color   = palette.color( QPalette.ColorRole.Highlight )
            if self._hover and not self.isSliderDown():
                color   = color.lighter( 130 )

        triangle    = QPolygonF( [ QPointF( x - half, track_y - POINTER_HEIGHT ),
                                   QPointF( x + half, track_y - POINTER_HEIGHT ),
                                   QPointF( x,        track_y ),
                                   ] )
        painter.setPen( Qt.PenStyle.NoPen )
        painter.setBrush( color )
        painter.drawPolygon( triangle )

        # ---- readout, centred over the pointer but kept inside the widget
        text        = self.text_from_value( self.sliderPosition() )
        metrics     = QFontMetrics( self.font() )
        text_w      = metrics.horizontalAdvance( text )
        text_x      = min( max( x - text_w / 2, 0 ), self.width() - text_w )
        text_rect   = QRectF( text_x, GAP, text_w, self._text_height() )

        if text:                                # "" hides the readout
            painter.setPen( palette.color( QPalette.ColorRole.WindowText ) )
            painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, text )

        # ---- focus cue, a frame round pointer and readout, so you can
        #      tell which scale the arrow keys will move
        if self.hasFocus():
            if text:
                left    = min( text_rect.left(),  x - half ) - 2
                right   = max( text_rect.right(), x + half ) + 2
                top     = 1
            else:                               # no readout, frame the pointer only
                left    = x - half - 2
                right   = x + half + 2
                top     = track_y - POINTER_HEIGHT - 2
            focus_rect  = QRectF( left, top, right - left, track_y - top )
            pen         = QPen( palette.color( QPalette.ColorRole.Highlight ) )
            pen.setWidth( 1 )
            painter.setPen( pen )
            painter.setBrush( Qt.BrushStyle.NoBrush )
            painter.drawRoundedRect( focus_rect, 3, 3 )

    # ---- mouse
    # ------------------------------------
    def mousePressEvent( self, event ):
        """
        left button only.  on the pointer: grab it, keeping the offset between
        the press and the pointer so it does not jump.  elsewhere: jump there
        and drag, or page toward it, depending on click_jumps
        """
        if event.button() != Qt.MouseButton.LeftButton:
            event.ignore()
            return

        event.accept()
        press_x     = event.position().x()        # qtpy shims position() onto Qt5
        pointer_x   = self.value_to_pixel( self.sliderPosition() )

        if self._pointer_hit_rect().contains( event.position() ):
            self._start_drag( press_x - pointer_x )
            return

        if self.click_jumps:
            self._start_drag( 0 )
            self.setSliderPosition( self.pixel_to_value( press_x ) )
            return

        # ---- paging: one step now, then repeat while held
        self._page_target_x     = press_x
        self._page_step()
        self._page_timer.start( PAGE_REPEAT_DELAY )

    # ------------------------------------
    def _page_step( self ):
        """
        one page step toward the mouse, unless the pointer is already there.
        returns True if it stepped
        """
        target      = self.pixel_to_value( self._page_target_x )
        position    = self.sliderPosition()
        if target > position:
            self.triggerAction( QAbstractSlider.SliderAction.SliderPageStepAdd )
            return True
        if target < position:
            self.triggerAction( QAbstractSlider.SliderAction.SliderPageStepSub )
            return True
        return False

    # ------------------------------------
    def _page_repeat( self ):
        """
        timer tick while the button is held on the track.  like QSlider, stop
        once a whole page step would carry the pointer past the mouse, so it
        does not bounce back and forth around it
        """
        self._page_timer.setInterval( PAGE_REPEAT_EVERY )
        target      = self.pixel_to_value( self._page_target_x )
        gap         = abs( target - self.sliderPosition() )
        if gap < self.pageStep() or not self._page_step():
            self._page_timer.stop()

    # ------------------------------------
    def _stop_paging( self ):
        """
        what it says
        """
        self._page_timer.stop()
        self._page_target_x     = None

    # ------------------------------------
    def _start_drag( self, offset ):
        """
        what it says -- setSliderDown emits sliderPressed
        """
        self._drag_offset   = offset
        self._drag_start    = self.sliderPosition()
        self.setSliderDown( True )
        self.setCursor( Qt.CursorShape.ClosedHandCursor )

    # ------------------------------------
    def mouseMoveEvent( self, event ):
        """
        dragging: move the pointer, setSliderPosition emits sliderMoved and,
        with tracking on, valueChanged.  not dragging: just hover.
        uses our own drag flag, not event.buttons() -- more robust, and
        QTest.mouseMove does not carry the buttons anyway
        """
        if self._page_target_x is not None:
            self._page_target_x     = event.position().x()     # like QSlider, chase the mouse
            if not self._page_timer.isActive():
                self._page_timer.start( PAGE_REPEAT_EVERY )
            return

        if self._drag_offset is None:
            self._set_hover( self._pointer_hit_rect().contains( event.position() ) )
            return

        x           = event.position().x() - self._drag_offset
        self.setSliderPosition( self.pixel_to_value( x ) )

    # ------------------------------------
    def mouseReleaseEvent( self, event ):
        """
        setSliderDown( False ) emits sliderReleased, and when tracking is off
        it is also what copies sliderPosition into value
        """
        if event.button() != Qt.MouseButton.LeftButton:
            event.ignore()
            return

        if self._page_target_x is not None:
            event.accept()
            self._stop_paging()
            return

        if self._drag_offset is None:           # escape already ended it
            event.ignore()
            return

        event.accept()
        self._end_drag( event.position() )

    # ------------------------------------
    def _end_drag( self, mouse_pos ):
        """
        what it says -- shared by release and escape
        """
        self._drag_offset   = None
        self._drag_start    = None
        self.setSliderDown( False )
        self._hover         = False             # force the cursor refresh below
        self._set_hover( self._pointer_hit_rect().contains( mouse_pos ) )

    # ------------------------------------
    def keyPressEvent( self, event ):
        """
        escape during a drag puts the pointer back where the drag began and
        ends the drag; the button is still down but later moves just hover.
        escape while paging stops the repeat.  every other key, and escape
        when idle, goes to QAbstractSlider as before
        """
        if event.key() == Qt.Key.Key_Escape:
            if self._drag_offset is not None:
                event.accept()
                self.setSliderPosition( self._drag_start )
                self._end_drag( QPointF( self.mapFromGlobal( self.cursor().pos() ) ) )
                return
            if self._page_target_x is not None:
                event.accept()
                self._stop_paging()
                return

        super().keyPressEvent( event )

    # ------------------------------------
    def leaveEvent( self, event ):
        """
        what it says
        """
        if self._drag_offset is None:
            self._set_hover( False )
        super().leaveEvent( event )

    # ------------------------------------
    def _set_hover( self, hover ):
        """
        hover state, cursor and a repaint, only when it changes
        """
        if hover == self._hover and self.cursor().shape() != Qt.CursorShape.ClosedHandCursor:
            return
        self._hover     = hover
        if hover:
            self.setCursor( Qt.CursorShape.OpenHandCursor )
        else:
            self.unsetCursor()
        self.update()


# -------------------------------
def main():
    """
    what it says -- stand alone run, three scales to try.
    the second pages on a track click, the other two jump
    """
    app                 = QApplication( sys.argv )

    a_window            = QWidget()
    layout              = QVBoxLayout( a_window )

    widget              = ScaleSlider()                  # defaults 0 .. 100 at 50
    layout.addWidget( widget )

    widget              = ScaleSlider()
    widget.setRange( 3, 47 )                             # odd ends, ticks still on 5s
    widget.set_major_tick_interval( 5 )
    widget.setValue( 3 )
    widget.click_jumps  = False                          # this one pages, QSlider style
    layout.addWidget( widget )

    widget              = ScaleSlider()
    widget.setRange( 0, 1000 )                           # minor ticks too dense, skipped
    widget.set_major_tick_interval( 100 )
    widget.setValue( 1000 )
    layout.addWidget( widget )

    layout.addStretch()

    a_window.setWindowTitle( "scale_slider.py -- step 3, drag the pointer or click the track, escape cancels a drag" )
    a_window.resize( 600, 260 )
    a_window.show()

    sys.exit( app.exec_() if hasattr( app, "exec_" ) else app.exec() )

# --------------------
if __name__ == "__main__":
    #----- the widget, not a tab, so run it on its own
    main()
# --------------------

# ---- eof
