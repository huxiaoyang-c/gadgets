import cv2

from loguru import logger

from ._path_utils import valid_path


__all__ = ['play_frames', 'VideoWriter']


KEY_ESC = 27
KEY_SPACE = 32
KEY_LEFT_ARROW = 81
KEY_RIGHT_ARROW = 83


def play_frames(frames, wait_ms=100):
    num_frames = len(frames)
    frame_idx = -1
    paused = False
    while True:
        if not paused:
            key = cv2.waitKey(wait_ms)

            if key == KEY_RIGHT_ARROW or key == -1:
                frame_idx += 1
            elif key == KEY_ESC:
                break
            elif key == KEY_SPACE:
                logger.debug('paused')
                paused = not paused
                continue
            else:
                logger.warning(f'play: key ({key}) no effect')

            if frame_idx == num_frames:
                break
        else:
            key = cv2.waitKey()

            if key == KEY_LEFT_ARROW:
                frame_idx -= 1
            elif key == KEY_RIGHT_ARROW:
                frame_idx += 1
            elif key == KEY_ESC:
                break
            elif key == KEY_SPACE:
                logger.debug('play')
                paused = not paused
                frame_idx += 1
            else:
                logger.warning(f'paused: key ({key}) no effect')

            frame_idx = num_frames - 1 if frame_idx < 0 else frame_idx
            frame_idx = 0 if frame_idx >= num_frames else frame_idx

        logger.debug(f'frame: {frame_idx}/{num_frames}')
        cv2.imshow('', frames[frame_idx])
        cv2.waitKey(1)


class VideoWriter:
    def __init__(self, path, fps=8):
        self.path = valid_path(path, 'w')
        self.format = self.path.suffix
        if self.format == '.mp4':
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        elif self.format == '.avi':
            self.fourcc = cv2.VideoWriter_fourcc(*'XIVD')
        else:
            raise NameError(f'{self.path.as_posix()} is not a valid video save path')

        self.fps = fps

        self._writer = None

    def write(self, frame):
        if self._writer is None:
            h, w, _ = frame.shape
            self._writer = cv2.VideoWriter(self.path.as_posix(), self.fourcc, self.fps, (w, h))
        self._writer.write(frame)
