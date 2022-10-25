import cv2
import numpy as np


__all__ = ['getTextSize', 'putText', 'line', 'rectangle']


def int_coord(coord):
    return [max(0, int(v)) for v in coord]


""" opencv Text
        new_org __________
        cv2_org|_abcdefgh_| th (offset)
               |__________| tb            th+tb (height)
                tw (width)
        cv2_org.y = new_org.y + offset
"""


def getTextSize(text, fontFace, fontScale, thickness):
    """ extend 'cv2.getTextSize', return real text width and height, and offset helps putText from left-top """
    (tw, th), tb = cv2.getTextSize(text, fontFace, fontScale, thickness)
    width = tw
    height = th + tb
    offset = th
    return width, height, offset


def putText(img, text, org, fontFace, fontScale, color, thickness,
            bg_color=(255, 255, 255), bg_alpha=0.):
    """ extend 'cv2.putText', 'org' indicates left-top, with background when bg_alpha>0, and return right-bottom """
    x0, y0 = int_coord(org)
    w, h, o = getTextSize(text, fontFace, fontScale, thickness)
    if bg_alpha > 0:
        rectangle(img, (x0, y0), (x0+w, y0+h), bg_color, thickness, bg_alpha, with_line=False)
    cv2.putText(img, text, (x0, y0 + o), fontFace, fontScale, color, thickness)
    return x0 + w, y0 + h


def line(img, pt1, pt2, color, thickness):
    pt1 = int_coord(pt1)
    pt2 = int_coord(pt2)
    cv2.line(img, pt1, pt2, color, thickness)


def rectangle(img, pt1, pt2, color, thickness,
              bg_alpha=0., with_line=True):
    """ extend cv2.rectangle, with background, and without four sides when bg_alpha>0 and with_line=False """
    h, w, _ = img.shape
    x0, y0 = int_coord(pt1)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = int_coord(pt2)
    x1, y1 = min(w, x1), min(h, y1)

    if bg_alpha > 0:
        bg = np.zeros((y1-y0, x1-x0, 3), np.uint8)
        bg[:] = color
        img[y0:y1, x0:x1] = cv2.addWeighted(img[y0:y1, x0:x1], 1-bg_alpha, bg, bg_alpha, 0)
    if with_line:
        cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness)


