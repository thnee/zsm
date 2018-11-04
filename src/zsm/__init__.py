# SPDX-License-Identifier: BSD-2-Clause
from typing import Optional

import logging
from pathlib import Path
import sys


def init_logging(
    log_level: str, log_file: Optional[Path] = None, log_console: bool = False
) -> None:
    log_level = getattr(logging, log_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if log_file:
        file_formatter = logging.Formatter(
            style="{", fmt="{asctime} {name:12} {levelname:8} {message}"
        )
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)

    if log_console:
        console_formatter = logging.Formatter(style="{", fmt="{message}")
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)

    logging.getLogger("PidFile").setLevel(logging.ERROR)
    logging.getLogger("sarge").setLevel(logging.ERROR)
