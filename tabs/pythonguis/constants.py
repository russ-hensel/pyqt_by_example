
# ---- tof

from enum import IntEnum

from qtpy.QtGui import (
    QColor,
    QImage,
)



from pathlib import Path

image_dir    = Path( __file__ ).parent
image_dir    = Path().joinpath( str( image_dir ), "images" )


IMG_BOMB    = QImage( f"{image_dir}/bug.png" )
IMG_FLAG    = QImage( f"{image_dir}/flag.png" )
IMG_START   = QImage( f"{image_dir}/rocket.png" )
IMG_CLOCK   = QImage( f"{image_dir}/clock-select.png" )

NUM_COLORS = {
    1: QColor("#f44336"),
    2: QColor("#9C27B0"),
    3: QColor("#3F51B5"),
    4: QColor("#03A9F4"),
    5: QColor("#00BCD4"),
    6: QColor("#4CAF50"),
    7: QColor("#E91E63"),
    8: QColor("#FF9800"),
}

LEVELS = [(8, 10), (16, 40), (24, 99)]


class Status( IntEnum ):
    READY    = 0
    PLAYING  = 1
    FAILED   = 2
    SUCCESS  = 3


STATUS_ICONS = {
    Status.READY:   f"{image_dir}/lus.png",
    Status.PLAYING: f"{image_dir}/smiley.png",
    Status.FAILED:  f"{image_dir}/cross.png",
    Status.SUCCESS: f"{image_dir}/smiley-lol.png",
}


# ---- eof