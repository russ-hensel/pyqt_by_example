#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
# we do not run from here has its own main, else run from the tab
#  /pyqt_by_example/tabs/more/tab_image_overlay.py
"""
image_overlay_view.py


show one image over another, see through the transparent parts
of the top one, and drag / nudge / rotate / scale it into
                position while watching.  save the result at full resolution.

this is the re-usable widget, not a tab -- tabs/more/tab_image_overlay.py is
the tab that hosts it and supplies the controls.  the split is deliberate:
everything about images and interaction lives here, everything about buttons
and layout lives in the tab, and they talk only through the api below.

    the api
        set_base_image( source )         source is a file name, QPixmap or QImage
        set_overlay_image( source )
        overlay_offset()  / set_overlay_offset( x, y )   user units, x and y calibrated
        overlay_x_scale() / set_overlay_x_scale( x_scale )   pixel = user * x_scale
        overlay_y_scale() / set_overlay_y_scale( y_scale )   pixel = user * y_scale
        overlay_rotation() / set_overlay_rotation( degrees )
        overlay_scale()   / set_overlay_scale( factor )
        set_overlay_opacity( 0.0 - 1.0 )
        set_composition_mode( mode )     a QPainter.CompositionMode
        fill_overlay_transparent( color = None )   yellow by default
        nudge( dx, dy )
        reset_overlay()
        fit_to_view()  zoom_in()  zoom_out()  zoom_reset()
        render_to_image( background = None )   -> QImage, full resolution
        save_result( file_name, background = None )  -> bool
        overlay_changed  signal ( x, y, rotation, scale )

runs on its own for a look:
    python image_overlay_view.py                     demo images, no files needed
    python image_overlay_view.py base.png over.png

Qt5 and Qt6 both -- no multimedia here, just QtGui and QtWidgets, and every
enum is spelled the scoped way, which both bindings accept ( checked ).
"""

import sys

from qtpy.QtCore import ( QPointF, QRectF, Qt, Signal )
from qtpy.QtGui  import ( QBrush, QColor, QImage, QPainter, QPixmap )
from qtpy.QtWidgets import ( QApplication,
                             QGraphicsItem,
                             QGraphicsPixmapItem,
                             QGraphicsScene,
                             QGraphicsView,
                             )

# ---- end imports

CHECKER_SIZE    = 12                    # px, the transparency checkerboard
CHECKER_LIGHT   = QColor( 200, 200, 200 )
CHECKER_DARK    = QColor( 160, 160, 160 )

ZOOM_STEP       = 1.25
ZOOM_MIN        = 0.02
ZOOM_MAX        = 50.0

NUDGE_SMALL     = 1                     # px, arrow key
NUDGE_LARGE     = 10                    # px, shift + arrow key


# -----------------------------------------------
class OverlayPixmapItem( QGraphicsPixmapItem ):
    """
    the top image.  a plain QGraphicsPixmapItem can not do two things this
    needs, so both are added here:

        * tell somebody it moved -- itemChange with ItemPositionHasChanged,
          which only fires at all if ItemSendsGeometryChanges is set
        * paint with a composition mode other than SourceOver -- there is no
          setCompositionMode on an item, so paint() sets it on the painter
          before letting the base class draw

    positions are snapped to whole user units on the way in ( ItemPositionChange ),
    because the point of this widget is alignment and a fractional
    offset can not be typed back in or reproduced

    x and y calibration -- two kinds of position:
        * user units     -- what a host shows and types, the spin boxes
        * scene pixels   -- pos() / setPos()
            pixel x = user x  * x_scale         pixel y = user y  * y_scale
            user x  = pixel x * x_scale_inverse user y  = pixel y * y_scale_inverse
    x_scale defaults to 1.0, y_scale to -1.0, which is the old "+y goes up"
    flip and nothing more.  a y_scale of -0.5 is two user units per pixel,
    still up.  use user_pos / set_user_pos to cross over, and set_x_scale /
    set_y_scale to change them -- never assign a scale directly or its
    inverse goes stale
    """

    def __init__( self, on_moved = None, parent = None ):
        """
        on_moved is a plain callable, not a signal -- a QGraphicsItem is not a
        QObject and can not emit
        """
        super().__init__( parent )

        self.on_moved           = on_moved
        self.composition_mode   = None      # None means leave the painter alone

        self.x_scale            = 1.0       # set only by set_x_scale
        self.x_scale_inverse    = 1.0

        self.y_scale            = -1.0      # set only by set_y_scale
        self.y_scale_inverse    = -1.0

        self.setFlag( QGraphicsItem.GraphicsItemFlag.ItemIsMovable,            True )
        self.setFlag( QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True )

        # items default to fast transformation, which makes a rotated or
        # scaled overlay visibly ragged -- and it would save that way too
        self.setTransformationMode( Qt.TransformationMode.SmoothTransformation )

    # -------------------------------
    def itemChange( self, change, value ):
        """
        read it -- snap going in, report movement coming out.  see _snap
        """
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            return super().itemChange( change, self._snap( value ) )

        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.on_moved is not None:
                self.on_moved()

        return super().itemChange( change, value )

    # -------------------------------
    def _snap( self, a_point ):
        """
        read it -- a scene point snapped to whole user units, x and y both.
        rounding in user units and scaling back means every position is an
        exact multiple of the scale, so pixel -> user -> pixel always comes
        back where it started
        """
        a_x                     = round( a_point.x() * self.x_scale_inverse ) * self.x_scale
        a_y                     = round( a_point.y() * self.y_scale_inverse ) * self.y_scale
        return QPointF( a_x, a_y )

    # -------------------------------
    def set_x_scale( self, x_scale ):
        """
        read it -- the only place x_scale and x_scale_inverse are set, so they
        can not disagree.  negative for +x left.  the position is kept in
        pixels and re-snapped to the new grid, so the user value is what changes
        """
        x_scale                 = float( x_scale )

        if x_scale == 0.0:
            raise ValueError( "x_scale can not be 0" )

        self.x_scale            = x_scale
        self.x_scale_inverse    = 1.0 / x_scale

        # setPos returns early if the point is unchanged, so snap here rather
        # than hoping itemChange runs
        self.setPos( self._snap( self.pos() ) )

    # -------------------------------
    def set_y_scale( self, y_scale ):
        """
        read it -- the only place y_scale and y_scale_inverse are set, so they
        can not disagree.  negative for +y up.  the position is kept in pixels
        and re-snapped to the new grid, so the user value is what changes
        """
        y_scale                 = float( y_scale )

        if y_scale == 0.0:
            raise ValueError( "y_scale can not be 0" )

        self.y_scale            = y_scale
        self.y_scale_inverse    = 1.0 / y_scale

        # setPos returns early if the point is unchanged, so snap here rather
        # than hoping itemChange runs
        self.setPos( self._snap( self.pos() ) )

    # -------------------------------
    def user_pos( self, ):
        """ what it says -- pos() in user units, a QPointF """
        a_point                 = self.pos()
        return QPointF( a_point.x() * self.x_scale_inverse,
                        a_point.y() * self.y_scale_inverse )

    # -------------------------------
    def set_user_pos( self, x, y ):
        """ what it says -- setPos() from user units """
        self.setPos( QPointF( float( x ) * self.x_scale,
                              float( y ) * self.y_scale ) )

    # -------------------------------
    def paint( self, painter, option, widget = None ):
        """
        read it -- the only way to get a composition mode onto a pixmap item.
        Difference is the useful one for alignment work: identical pixels come
        out black, so a misregistration lights up
        """
        if self.composition_mode is not None:
            painter.setCompositionMode( self.composition_mode )

        super().paint( painter, option, widget )


# -----------------------------------------------
class ImageOverlayView( QGraphicsView ):
    """
    two images, one over the other, the top one draggable.

    derives from QGraphicsView rather than wrapping one in a QWidget -- the
    thing is a view, and wrapping would only add a layer to forward calls
    through.  drop it straight into a layout.

    two different things both want to be called "scale" and they must not be
    confused:
        * view zoom      -- how big it looks on screen, zoom_in / zoom_out.
                            NOT part of the result, never saved
        * overlay scale  -- part of the transform being aligned,
                            set_overlay_scale.  saved
    """

    # x, y, rotation degrees, scale factor -- so a host can follow a mouse drag
    overlay_changed         = Signal( float, float, float, float )

    def __init__( self, parent = None ):
        """
        """
        super().__init__( parent )

        self.base_item          = None      # QGraphicsPixmapItem, the bottom image
        self.overlay_item       = None      # OverlayPixmapItem, the top one

        a_scene                 = QGraphicsScene( self )
        self.setScene( a_scene )
        self.a_scene            = a_scene

        # AnchorUnderMouse is what makes wheel zoom feel right -- the point
        # under the pointer stays put instead of the view jumping to centre
        self.setTransformationAnchor( QGraphicsView.ViewportAnchor.AnchorUnderMouse )
        self.setResizeAnchor(         QGraphicsView.ViewportAnchor.AnchorViewCenter )

        # NoDrag, or the view would pan and fight the item drag for the mouse
        self.setDragMode( QGraphicsView.DragMode.NoDrag )

        self.setRenderHint( QPainter.RenderHint.Antialiasing,          True )
        self.setRenderHint( QPainter.RenderHint.SmoothPixmapTransform, True )

        # or the arrow keys go to the scroll bars and never reach keyPressEvent
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

        # and use as an api
        self.last_overlay_source    = None
        self.last_base_source       = None



    # ---- loading -----------------------------------------------------------

    # -------------------------------
    def _to_pixmap( self, source ):
        """
        what it says -- accept a file name, a QPixmap or a QImage, hand back a
        QPixmap, or None if it could not be loaded

        source    file name, a QPixmap or a QImage
        used by
        """
        if isinstance( source, QPixmap ):
            a_pixmap            = source

        elif isinstance( source, QImage ):
            a_pixmap            = QPixmap.fromImage( source )

        else: # think this is a file
            a_pixmap            = QPixmap( str( source ) )

        if a_pixmap.isNull():
            return None

        return a_pixmap

    # -------------------------------
    def set_base_image( self, source ):
        """
        read it -- the bottom image.  it also defines the canvas: sceneRect
        comes from its rect, so it is what gets saved, and an overlay hanging
        off the edge is cropped by it.

        returns True if the image loaded
        """
        a_pixmap                = self._to_pixmap( source )

        if a_pixmap is None:
            return False

        self.last_base_source   = str( source )

        if self.base_item is None:
            self.base_item      = self.a_scene.addPixmap( a_pixmap )
            self.base_item.setZValue( 0 )
            self.base_item.setTransformationMode( Qt.TransformationMode.SmoothTransformation )

        else:
            self.base_item.setPixmap( a_pixmap )

        self._update_scene_rect()

        return True

    # -------------------------------
    def set_overlay_image( self, source ):
        """
        read it -- the top image, the one that moves.  transparent parts of it
        show whatever is underneath, which is just what QPainter does by
        default ( SourceOver ) -- nothing here arranges it

        returns True if the image loaded

        args

            source    file name, a QPixmap or a QImage

        """
        a_pixmap            = self._to_pixmap( source )

        if a_pixmap is None:
            return False

        if self.overlay_item is None:
            a_item              = OverlayPixmapItem( on_moved = self._emit_overlay_changed )
            self.a_scene.addItem( a_item )
            a_item.setZValue( 1 )
            self.overlay_item   = a_item

        self.last_overlay_source = str( source )
        self.overlay_item.setPixmap( a_pixmap )

        # rotate and scale about the middle, not the top left corner, or the
        # image swings away from the pointer and feels broken
        a_rect              = QRectF( a_pixmap.rect() )
        self.overlay_item.setTransformOriginPoint( a_rect.center() )

        self._update_scene_rect()
        self._emit_overlay_changed()

        return True

    # -------------------------------
    def has_images( self, ):
        """ what it says """
        return ( self.base_item is not None ) and ( self.overlay_item is not None )

    # -------------------------------
    def _update_scene_rect( self, ):
        """
        read it -- the canvas is the base image's rect when there is one.  no
        assumption anywhere that the two images are the same size, so a
        mismatched pair later is not a rewrite
        """
        if self.base_item is not None:
            a_rect              = self.base_item.mapRectToScene( self.base_item.boundingRect() )

        elif self.overlay_item is not None:
            a_rect              = self.overlay_item.mapRectToScene( self.overlay_item.boundingRect() )

        else:
            return

        self.a_scene.setSceneRect( a_rect )

    # ---- the overlay transform ---------------------------------------------

    # -------------------------------
    def overlay_offset( self, ):
        """
        what it says -- the top left of the overlay in user units, as a
        QPointF.  ( 0, 0 ) means its corner is on the base image's corner.
        x and y are calibrated, see OverlayPixmapItem
        """
        if self.overlay_item is None:
            return QPointF( 0.0, 0.0 )

        return self.overlay_item.user_pos()

    # -------------------------------
    def set_overlay_offset( self, x, y ):
        """
        what it says -- in user units, calibrated by x_scale and y_scale.
        y_scale by default makes +y go up
        """
        if self.overlay_item is None:
            return

        self.overlay_item.set_user_pos( x, y )
        # setPos trips itemChange, which calls _emit_overlay_changed for us

    # -------------------------------
    def overlay_x_scale( self, ):
        """ what it says -- scene pixels per user unit in x, negative is +x left """
        if self.overlay_item is None:
            return 1.0

        return self.overlay_item.x_scale

    # -------------------------------
    def set_overlay_x_scale( self, x_scale ):
        """
        read it -- the x calibration, pixel = user * x_scale.  the overlay
        does not move ( beyond a re-snap ), the reported x changes
        """
        if self.overlay_item is None:
            return

        self.overlay_item.set_x_scale( x_scale )
        self._emit_overlay_changed()    # setPos may not have fired, pos unchanged

    # -------------------------------
    def overlay_y_scale( self, ):
        """ what it says -- scene pixels per user unit in y, negative is +y up """
        if self.overlay_item is None:
            return -1.0

        return self.overlay_item.y_scale

    # -------------------------------
    def set_overlay_y_scale( self, y_scale ):
        """
        read it -- the y calibration, pixel = user * y_scale.  the overlay
        does not move ( beyond a re-snap ), the reported y changes
        """
        if self.overlay_item is None:
            return

        self.overlay_item.set_y_scale( y_scale )
        self._emit_overlay_changed()    # setPos may not have fired, pos unchanged

    # -------------------------------
    def overlay_rotation( self, ):
        """ what it says -- degrees, clockwise """
        if self.overlay_item is None:
            return 0.0

        return self.overlay_item.rotation()

    # -------------------------------
    def set_overlay_rotation( self, degrees ):
        """ what it says """
        if self.overlay_item is None:
            return

        self.overlay_item.setRotation( float( degrees ) )
        self._emit_overlay_changed()    # rotation does not trip itemChange

    # -------------------------------
    def overlay_scale( self, ):
        """ what it says -- 1.0 is the image's own size """
        if self.overlay_item is None:
            return 1.0

        return self.overlay_item.scale()

    # -------------------------------
    def set_overlay_scale( self, factor ):
        """
        what it says -- this is the overlay's own scale, part of the result.
        it is NOT the view zoom, see the class docstring
        """
        if self.overlay_item is None:
            return

        factor              = max( float( factor ), 0.01 )
        self.overlay_item.setScale( factor )
        self._emit_overlay_changed()

    # -------------------------------
    def set_overlay_opacity( self, opacity ):
        """
        what it says -- 0.0 to 1.0.  a half transparent overlay is often
        easier to align by than a fully opaque one
        """
        if self.overlay_item is None:
            return

        self.overlay_item.setOpacity( max( 0.0, min( 1.0, float( opacity ) ) ) )

    # -------------------------------
    def set_overlay_visible( self, is_visible ):
        """
        what it says -- for blinking the overlay on and off, which the eye is
        far better at than judging a steady overlay
        """
        if self.overlay_item is None:
            return

        self.overlay_item.setVisible( bool( is_visible ) )

    # -------------------------------
    def is_overlay_visible( self, ):
        """ what it says """
        if self.overlay_item is None:
            return False

        return self.overlay_item.isVisible()

    # -------------------------------
    def set_composition_mode( self, mode ):
        """
        what it says -- a QPainter.CompositionMode, or None for the default.
        see OverlayPixmapItem.paint
        """
        if self.overlay_item is None:
            return

        self.overlay_item.composition_mode = mode
        self.overlay_item.update()

    # -------------------------------
    def fill_overlay_transparent( self, color = None ):
        """
        read it -- paint the transparent parts of the overlay a solid color,
        yellow by default.  a new pixmap is filled with the color and the old
        one drawn over it ( SourceOver ), so partly transparent pixels, say an
        antialiased edge, blend into the color rather than snapping to it.

        this replaces the overlay's pixmap -- the transparency is gone, and a
        second call with a different color does nothing visible.  reload the
        overlay with set_overlay_image to get it back.

        position, rotation, scale and the transform origin are untouched,
        the size does not change

        color     a QColor, or anything QColor accepts ( "yellow", "#ffff00" )
        returns True if there was an overlay to fill
        """
        if self.overlay_item is None:
            return False

        if color is None:
            color               = QColor( "yellow" )

        a_old_pixmap        = self.overlay_item.pixmap()

        a_new_pixmap        = QPixmap( a_old_pixmap.size() )
        a_new_pixmap.setDevicePixelRatio( a_old_pixmap.devicePixelRatio() )
        a_new_pixmap.fill( QColor( color ) )

        painter             = QPainter( a_new_pixmap )
        painter.drawPixmap( 0, 0, a_old_pixmap )
        painter.end()

        self.overlay_item.setPixmap( a_new_pixmap )

        return True

    # -------------------------------
    def nudge( self, dx, dy ):
        """ what it says -- move the overlay by whole user units, +dy is up by default """
        if self.overlay_item is None:
            return

        a_point             = self.overlay_item.user_pos()
        self.overlay_item.set_user_pos( a_point.x() + dx, a_point.y() + dy )

    # -------------------------------
    def reset_overlay( self, ):
        """ what it says -- back to corner on corner, no rotation, no scale """
        if self.overlay_item is None:
            return

        self.overlay_item.setRotation( 0.0 )
        self.overlay_item.setScale( 1.0 )
        self.overlay_item.setPos( 0.0, 0.0 )
        self._emit_overlay_changed()

    # -------------------------------
    def _emit_overlay_changed( self, ):
        """
        what it says -- one place, so a drag, a nudge and a setter all report
        the same way.  a host listening to this must block its own widgets'
        signals while it follows, or the two chase each other
        """
        if self.overlay_item is None:
            return

        a_point             = self.overlay_item.user_pos()
        self.overlay_changed.emit( a_point.x(),
                                   a_point.y(),
                                   self.overlay_item.rotation(),
                                   self.overlay_item.scale() )

    # ---- the view, ie zoom -- none of this is part of the result -----------

    # -------------------------------
    def fit_to_view( self, ):
        """ what it says """
        if self.a_scene.sceneRect().isEmpty():
            return

        self.fitInView( self.a_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio )

    # -------------------------------
    def zoom_by( self, factor ):
        """
        what it says -- with limits, or a few wheel clicks reach a scale where
        qt's transform stops being usable
        """
        a_scale             = self.transform().m11() * factor

        if a_scale < ZOOM_MIN or a_scale > ZOOM_MAX:
            return

        self.scale( factor, factor )

    # -------------------------------
    def zoom_in( self, ):
        """ what it says """
        self.zoom_by( ZOOM_STEP )

    # -------------------------------
    def zoom_out( self, ):
        """ what it says """
        self.zoom_by( 1.0 / ZOOM_STEP )

    # -------------------------------
    def zoom_reset( self, ):
        """ what it says -- back to one screen pixel per image pixel """
        self.resetTransform()

    # -------------------------------
    def view_zoom( self, ):
        """ what it says -- current zoom, 1.0 being actual size """
        return self.transform().m11()

    # ---- events ------------------------------------------------------------

    # -------------------------------
    def wheelEvent( self, event ):
        """
        what it says -- plain wheel zooms, the usual image viewer behaviour.
        the base class would scroll instead, so this does not call up to it
        """
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

        event.accept()

    # -------------------------------
    def keyPressEvent( self, event ):
        """
        read it -- arrow keys nudge the overlay a user unit, ten with shift.
        a QGraphicsView would scroll on the arrows, so these are swallowed
        here and never reach the base class.  nudge is in user units, so Up
        is +y and Right is +x, and the scales decide which way that is on screen
        """
        a_key               = event.key()

        is_shift            = bool( event.modifiers() & Qt.KeyboardModifier.ShiftModifier )
        a_step              = NUDGE_LARGE if is_shift else NUDGE_SMALL

        a_nudge_dict        = { Qt.Key.Key_Left  : ( -a_step,       0 ),
                                Qt.Key.Key_Right : (  a_step,       0 ),
                                Qt.Key.Key_Up    : (       0,  a_step ),
                                Qt.Key.Key_Down  : (       0, -a_step ),
                                }

        if a_key in a_nudge_dict:
            dx, dy              = a_nudge_dict[ a_key ]
            self.nudge( dx, dy )
            event.accept()
            return

        super().keyPressEvent( event )

    # -------------------------------
    def drawBackground( self, painter, rect ):
        """
        read it -- the grey checkerboard behind everything, so transparent
        areas read as transparent instead of as "some colour".

        this is deliberately the VIEW's background and not the SCENE's:
        QGraphicsScene.render() draws the scene, so a checkerboard put here
        can never leak into a saved file.  see render_to_image
        """
        super().drawBackground( painter, rect )

        painter.fillRect( rect, QBrush( CHECKER_LIGHT ) )

        # start on a multiple of the square size so the pattern does not crawl
        # about while scrolling
        left                = int( rect.left() )   - ( int( rect.left() )   % ( CHECKER_SIZE * 2 ) )
        top                 = int( rect.top() )    - ( int( rect.top() )    % ( CHECKER_SIZE * 2 ) )

        a_brush             = QBrush( CHECKER_DARK )
        y                   = top
        row                 = 0

        while y < rect.bottom():
            x                   = left + ( CHECKER_SIZE if ( row % 2 ) else 0 )
            while x < rect.right():
                painter.fillRect( QRectF( x, y, CHECKER_SIZE, CHECKER_SIZE ), a_brush )
                x                  += CHECKER_SIZE * 2
            y                  += CHECKER_SIZE
            row                += 1

    # ---- the result --------------------------------------------------------

    # -------------------------------
    def render_to_image( self, background = None ):
        """
        read it -- the composite at FULL resolution, not a screen grab: the
        target is the size of sceneRect in image pixels, so the view's zoom
        has nothing to do with it.

        background None keeps the alpha ( a png will have transparent parts ),
        or pass a QColor to flatten onto it.

        returns a QImage, null if there is nothing to render
        """
        a_rect              = self.a_scene.sceneRect()

        if a_rect.isEmpty():
            return QImage()

        a_image             = QImage( int( round( a_rect.width() ) ),
                                      int( round( a_rect.height() ) ),
                                      QImage.Format.Format_ARGB32_Premultiplied )

        if background is None:
            a_image.fill( Qt.GlobalColor.transparent )
        else:
            a_image.fill( background )

        painter             = QPainter( a_image )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing,          True )
        painter.setRenderHint( QPainter.RenderHint.SmoothPixmapTransform, True )

        self.a_scene.render( painter, QRectF( a_image.rect() ), a_rect )

        painter.end()

        return a_image

    # -------------------------------
    def save_result( self, file_name, background = None ):
        """
        what it says -- format comes from the extension, so .png keeps the
        alpha and .jpg will not.  returns True on success
        """
        a_image             = self.render_to_image( background = background )

        if a_image.isNull():
            return False

        return a_image.save( str( file_name ) )

# -----------------------------------------------
def make_demo_pixmaps():
    """
    read it -- two images made in code, so the module demonstrates itself with
    no files to find: a solid blue/green base, and a red ring over a
    transparent middle, which is what you look through
    """
    base                = QPixmap( 400, 300 )
    base.fill( QColor( 40, 90, 140 ) )

    painter             = QPainter( base )
    painter.setRenderHint( QPainter.RenderHint.Antialiasing, True )
    painter.fillRect( 0, 150, 400, 150, QColor( 60, 140, 90 ) )
    painter.setPen( QColor( 255, 255, 255 ) )
    for ix in range( 0, 400, 40 ):
        painter.drawLine( ix, 0, ix, 300 )
    painter.end()

    overlay             = QPixmap( 400, 300 )
    overlay.fill( Qt.GlobalColor.transparent )      # the whole point

    painter             = QPainter( overlay )
    painter.setRenderHint( QPainter.RenderHint.Antialiasing, True )
    painter.setBrush( QBrush( QColor( 200, 40, 40, 220 ) ) )
    painter.setPen( QColor( 255, 220, 0 ) )
    painter.drawEllipse( 60, 40, 280, 220 )
    painter.setBrush( QBrush( Qt.GlobalColor.transparent ) )
    painter.setCompositionMode( QPainter.CompositionMode.CompositionMode_Clear )
    painter.drawEllipse( 120, 90, 160, 120 )        # punch a hole to see through
    painter.end()

    return ( base, overlay )

# -------------------------------
def main():
    """
    what it says -- stand alone run, for a look at the widget on its own.
    the tab is the real host, see tabs/more/tab_image_overlay.py
    """
    app                 = QApplication( sys.argv )

    a_widget            = ImageOverlayView()

    if len( sys.argv ) >= 3:
        a_widget.set_base_image(    sys.argv[1] )
        a_widget.set_overlay_image( sys.argv[2] )
    else:
        base, overlay       = make_demo_pixmaps()
        a_widget.set_base_image( base )
        a_widget.set_overlay_image( overlay )

    a_widget.setWindowTitle( "image_overlay_view.py -- drag the top image, arrows nudge, wheel zooms" )
    a_widget.resize( 700, 560 )
    a_widget.show()
    a_widget.fit_to_view()

    sys.exit( app.exec_() if hasattr( app, "exec_" ) else app.exec() )

# --------------------
if __name__ == "__main__":
    #----- the widget, not a tab, so run it on its own
    main()
# --------------------

# ---- eof
