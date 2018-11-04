# SPDX-License-Identifier: BSD-2-Clause
import sys
from unittest import mock
import pkg_resources

import pytest
from click.testing import CliRunner
import pid

import zsm


@pytest.fixture
def mock_zsm_lib():
    mock_zsm_lib = mock.MagicMock()

    mock_zsm_lib_config = mock.MagicMock()
    mock_zsm_lib_manage = mock.MagicMock()
    mock_zsm_lib_zfs = mock.MagicMock()

    mock_zsm_lib.config = mock_zsm_lib_config
    mock_zsm_lib.manage = mock_zsm_lib_manage
    mock_zsm_lib.zfs = mock_zsm_lib_zfs

    sys.modules["zsm_lib"] = mock_zsm_lib
    sys.modules["zsm_lib.config"] = mock_zsm_lib_config
    sys.modules["zsm_lib.manage"] = mock_zsm_lib_manage
    sys.modules["zsm_lib.zfs"] = mock_zsm_lib_zfs

    return mock_zsm_lib


def test_load_config_calls_zsm_lib_config_load(mock_zsm_lib):
    with mock.patch("zsm.cli.open", mock.mock_open()):
        zsm.cli.load_config()

    mock_zsm_lib.config.load.assert_called()


def test_cron_returns_0_on_success(mock_zsm_lib):
    with mock.patch("pid.PidFile"):
        with mock.patch("zsm.cli.load_config", return_value={}):
            runner = CliRunner()
            result = runner.invoke(
                zsm.cli.program,
                ["cron", "--log-file", "/dev/null", "--config-file", "/dev/null"],
                obj={},
            )

    assert result.exit_code == 0


def test_cron_returns_1_on_failed_config_load(mock_zsm_lib):
    with mock.patch("pid.PidFile"):
        with mock.patch("zsm.cli.load_config", return_value=None):
            runner = CliRunner()
            result = runner.invoke(
                zsm.cli.program, ["cron", "--log-file", "/dev/null"], obj={}
            )

    assert result.exit_code == 1


def test_cron_returns_2_on_pidfilealreadylockederror(mock_zsm_lib):
    with mock.patch("pid.PidFile", side_effect=pid.PidFileAlreadyLockedError):
        with mock.patch("zsm.cli.load_config", return_value={}):
            runner = CliRunner()
            result = runner.invoke(
                zsm.cli.program, ["cron", "--log-file", "/dev/null"], obj={}
            )

    assert result.exit_code == 2


def test_validate_config_returns_0_on_success(mock_zsm_lib):
    with mock.patch("zsm.cli.open", mock.mock_open()):
        runner = CliRunner()
        result = runner.invoke(
            zsm.cli.program, ["validate-config", "--config-file", "/fake/path"], obj={}
        )

    assert result.exit_code == 0


def test_validate_config_returns_1_on_validationerror(mock_zsm_lib):
    class MockValidationError(Exception):
        pass

    def mocked_load(data):
        raise MockValidationError()

    mock_zsm_lib.config.ValidationError = MockValidationError
    mock_zsm_lib.config.load = mock.MagicMock(side_effect=mocked_load)

    with mock.patch("zsm.cli.open", mock.mock_open()):
        runner = CliRunner()
        result = runner.invoke(zsm.cli.program, ["validate-config"], obj={})

    assert result.exit_code == 1


def test_validate_config_returns_1_on_filenotfounderror(mock_zsm_lib):
    with mock.patch("zsm.cli.open", mock.mock_open()) as mock_open:
        mock_open.side_effect = FileNotFoundError

        runner = CliRunner()
        result = runner.invoke(zsm.cli.program, ["validate-config"], obj={})

    assert result.exit_code == 1


def test_version_prints_version():
    runner = CliRunner()
    result = runner.invoke(zsm.cli.program, ["version"], obj={})

    assert result.exit_code == 0

    version = pkg_resources.get_distribution("zsm").version
    assert result.output.strip() == f"zsm {version}"


def test_cli_calls_program():
    with mock.patch("zsm.cli.program") as mock_program:
        zsm.cli.cli()
        mock_program.assert_called()
