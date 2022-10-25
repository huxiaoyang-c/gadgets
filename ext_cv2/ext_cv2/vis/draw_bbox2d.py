import cv2

from .._opencv._opencv import *

__all__ = ['draw_bbox2d']


# DEFAULT_FONT_FACE = cv2.FONT_HERSHEY_PLAIN
# DEFAULT_FONT_SCALE = 1
# DEFAULT_FONT_THICK = 1
#
# DEFAULT_LINE_THICK = 1

DEFAULT_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
DEFAULT_FONT_SCALE = 0.6
DEFAULT_FONT_THICK = 1

DEFAULT_LINE_THICK = 2


def draw_bbox2d(img, pt1, pt2, color, label='', label_bg_color='same', label_loc='left-top'):
    """

    loc: label location
         (0, 0) 'left top' --------------- 'right, top' (1, 0)
                          |               |
                          |               |
         (0, 1) 'left bot' --------------- 'right bot' (1, 1)

    :param img:
    :param pt1:
    :param pt2:
    :param color:
    :param label:
    :param label_bg_color:
    :param label_loc:
    :return:
    """
    # x0, y0 = int_coord(pt1)
    # x1, y1 = int_coord(pt2)
    # bw, bh = x1 - x0, y1 - y0
    # area = bw * bh
    img_h, img_w, _ = img.shape

    x0, y0 = pt1
    x1, y1 = pt2
    area = (x1-x0) * (y1-y0)

    # rect_thickness = DEFAULT_LINE_THICK if area < 10000 else 2 * DEFAULT_LINE_THICK
    # text_font_scale = DEFAULT_FONT_SCALE / 2 if area < 10000 else DEFAULT_FONT_SCALE

    if label_bg_color == 'same':
        label_bg_color = color

    text_color = (0, 0, 0) if sum(label_bg_color) > 128 * 3 else (255, 255, 255)

    rectangle(img, pt1, pt2, color, DEFAULT_LINE_THICK)

    if label:

        tw, th, _ = getTextSize(label, fontFace=DEFAULT_FONT_FACE, fontScale=DEFAULT_FONT_SCALE, thickness=DEFAULT_FONT_THICK)

        if label_loc == 'top-left':
            tx = x0
            ty = y0 - th if y0 > th else y0
        elif label_loc == 'bot-right':
            tx = x1 - tw if x1 > tw else x0
            ty = y1 if y1 + th < img_h else y1 - th
        else:
            tx = x0
            ty = y0

        # auto label location relative to bbox when loc is (0, 0), (1, 0), (1, 1) or (0, 1)
        # tx = x0 + loc[0] * (bw - tw) + int(tw >= 4 * bw) * tw * (loc[0] - 1 / 2) / abs(loc[0] - 1 / 2)
        # ty = y0 + loc[1] * (bh - th) + int(th >= bh / 3) * th * (loc[1] - 1 / 2) / abs(loc[1] - 1 / 2)

        putText(img, label, (tx, ty),
                fontFace=DEFAULT_FONT_FACE, fontScale=DEFAULT_FONT_SCALE, color=text_color, thickness=DEFAULT_FONT_THICK,
                bg_color=label_bg_color, bg_alpha=0.5)
