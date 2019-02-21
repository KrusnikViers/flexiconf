import os
import sys


def split_key_path(key_path: str):
    sequence = key_path.lower().split('.')
    return sequence[:-1], sequence[-1]


# Hack to get the caller's module path.
def get_caller_path():
    # Frame offset = current frame + loader constructor frame.
    relative_frame_offset = 2
    frame = sys._getframe(relative_frame_offset)
    path = os.path.dirname(os.path.abspath(frame.f_code.co_filename))
    return str(path)


# Default cast function, which does nothing.
def no_cast(x): return x


# Special type to distinguish None, explicitly set by user, and not specified default value.
class NotSet:
    pass


NOT_SET = NotSet()
