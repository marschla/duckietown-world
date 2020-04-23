# -*- coding: utf-8 -*-

import pickle
import sys

from zuper_commons.fs.types import Path
from . import logger
from .zc_debug_pickler import find_pickling_error
from .zc_safe_write import safe_read, safe_write

__all__ = ["safe_pickle_dump", "safe_pickle_load"]

debug_pickling = False


def safe_pickle_dump(
    value: object,
    filename: Path,
    protocol=pickle.HIGHEST_PROTOCOL,
    **safe_write_options,
):
    # sys.setrecursionlimit(15000)
    with safe_write(filename, **safe_write_options) as f:
        try:
            pickle.dump(value, f, protocol)
        except KeyboardInterrupt:
            raise
        except BaseException:
            msg = f"Cannot pickle object of class {type(value)}."
            logger.error(msg)

            if debug_pickling:
                msg = find_pickling_error(value, protocol)
                logger.error(msg)
            raise


def safe_pickle_load(filename):
    # TODO: add debug check
    with safe_read(filename) as f:
        return pickle.load(f)
        # TODO: add pickling debug
