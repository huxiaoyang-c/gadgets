import cv2

from pathlib import PosixPath

from ._path_utils import _valid_path


__all__ = ['imread', 'imshow', 'imwrite']


def imread(filename: [str, PosixPath]):
    filename = _valid_path(filename)
    img = cv2.imread(filename=filename.as_posix())
    return img


def imwrite(filename: [str, PosixPath], img):
    filename = _valid_path(filename, 'w')
    cv2.imwrite(filename=filename.as_posix(), img=img)


def imshow(img, win_name='imshow', wait_ms=None):
    cv2.imshow(winname=win_name, mat=img)
    key = cv2.waitKey(wait_ms)
    return key
