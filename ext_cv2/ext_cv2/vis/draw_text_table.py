import cv2

from .._opencv._opencv import *

__all__ = ['draw_text_table']


DEFAULT_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
DEFAULT_FONT_SCALE = 0.6
DEFAULT_FONT_THICK = 1

DEFAULT_LINE_THICK = 2


def draw_text_table(img, table, start_pos, col_colors):
    _, text_h, _ = getTextSize('dummy', DEFAULT_FONT_FACE, 0.6, 1)

    cell_widths = [0] * len(table[0])
    for j, row in enumerate(table):
        for i, col in enumerate(row):
            text_width, _, _ = getTextSize(col, DEFAULT_FONT_FACE, 0.6, 1)
            cell_widths[i] = max(cell_widths[i], text_width)
    cell_widths = [w + 10 for w in cell_widths]

    for j, row in enumerate(table):
        for i, col in enumerate(row):
            tx = start_pos[0] + sum(cell_widths[:i])
            ty = start_pos[1] + j * text_h
            putText(img, col, (tx, ty), DEFAULT_FONT_FACE, 0.6, col_colors[i], 1)

    return img