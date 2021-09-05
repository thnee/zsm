# SPDX-License-Identifier: BSD-2-Clause
import datetime
import logging
import sys
from pathlib import Path
from typing import Optional

import click
import pid
import pkg_resources

from . import config, manage
from .logging import init_logging


log = logging.getLogger(__name__)


def load_config(config_file: Optional[Path] = None) -> Optional[dict]:
    if config_file is None:
        config_file = config.get_path()

    log.info(f"Loading config file from: {config_file}")

    try:
        with open(str(config_file), "r") as f:
            return config.load(data=f)

    except FileNotFoundError:
        log.error(f"Config file not found: {config_file}")

    except config.ValidationError as e:
        log.error(f"Config file invalid: {e}")


@click.group()
@click.pass_context
def program(ctx):
    ctx.obj["now"] = datetime.datetime.now()


@program.command("cron")
@click.option(
    "--config-file", type=click.Path(), default=None, help="Path to config file."
)
@click.option(
    "--log-file",
    type=click.Path(),
    default="/var/log/zsm.log",
    help="Path to log file.",
)
@click.option(
    "--log-level", type=str, default="INFO", help="Minimum log level to output."
)
@click.option("--log-console", is_flag=True, help="Write logs to console.")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Prevent all operations that perform modifications from running.",
)
@click.pass_context
def cron(
    ctx,
    config_file: str,
    log_file: str,
    log_level: str,
    log_console: bool,
    dry_run: bool,
):
    if config_file is not None:
        config_file = Path(config_file)

    if log_file is not None:
        log_file = Path(log_file)

    init_logging(log_level=log_level, log_file=log_file, log_console=log_console)

    config_data = load_config(config_file=config_file)

    if config_data is None:
        sys.exit(1)

    try:
        with pid.PidFile("zsm_cron"):
            manage.manage_snapshots(
                config=config_data, now=ctx.obj["now"], dry_run=dry_run
            )

    except pid.PidFileAlreadyLockedError:
        log.info("Found existing pidfile, aborting.")
        sys.exit(2)


@program.command("validate-config")
@click.option(
    "--config-file", type=click.Path(), default=None, help="Path to config file."
)
@click.option(
    "--log-level", type=str, default="INFO", help="Minimum log level to output."
)
def validate_config(config_file: str, log_level: str):
    if config_file is not None:
        config_file = Path(config_file)

    init_logging(log_level=log_level, log_console=True)

    config_data = load_config(config_file=config_file)

    if config_data is None:
        sys.exit(1)

    log.info("Config file is valid!")


@program.command("version")
def version():
    version = pkg_resources.get_distribution("zsm").version
    print(f"zsm {version}")


def cli():
    program(obj={})
