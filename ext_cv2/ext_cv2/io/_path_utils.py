from pathlib import PosixPath, Path


def _valid_path(path: [str, PosixPath], mode: str = 'r') -> PosixPath:
    """
    Convert str to PosixPath and check existence
      - if mode is 'r': make sure the path exists
      - if mode is 'w': make sure the path's parent exists
    :param path:
    :param mode:
    :return:
    """
    assert mode in ['r', 'w'], f'mode only support ["r", "w"]'

    if isinstance(path, str):
        # path = Path(path).absolute()
        path = Path(path)

    if mode == 'r':
        assert path.exists(), f'not exists: {path}'
    elif mode == 'w':
        assert path.parent.exists(), f'not exists: {path.parent}'
    return path