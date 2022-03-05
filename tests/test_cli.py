from unittest import mock

import pid
import pkg_resources
from click.testing import CliRunner

import zsm
import zsm.config


@mock.patch("zsm.cli.open", mock.mock_open())
@mock.patch("zsm.config.load")
def test_load_config_calls_config_load(mock_config_load):
    zsm.cli.load_config()

    mock_config_load.assert_called()


@mock.patch("pid.PidFile", mock.MagicMock())
@mock.patch("zsm.cli.load_config", mock.MagicMock(return_value={}))
@mock.patch("zsm.manage.manage_snapshots", mock.MagicMock())
def test_cron_returns_0_on_success():
    runner = CliRunner()
    result = runner.invoke(
        zsm.cli.program,
        ["cron", "--log-file", "/dev/null", "--config-file", "/dev/null"],
        obj={},
    )

    assert result.exit_code == 0


@mock.patch("pid.PidFile", mock.MagicMock())
@mock.patch("zsm.cli.load_config", mock.MagicMock(return_value=None))
@mock.patch("zsm.manage.manage_snapshots", mock.MagicMock())
def test_cron_returns_1_on_failed_config_load():
    runner = CliRunner()
    result = runner.invoke(zsm.cli.program, ["cron", "--log-file", "/dev/null"], obj={})

    assert result.exit_code == 1


@mock.patch("pid.PidFile", mock.MagicMock(side_effect=pid.PidFileAlreadyLockedError))
@mock.patch("zsm.cli.load_config", mock.MagicMock(return_value={}))
@mock.patch("zsm.manage.manage_snapshots", mock.MagicMock())
def test_cron_returns_2_on_pidfilealreadylockederror():
    runner = CliRunner()
    result = runner.invoke(zsm.cli.program, ["cron", "--log-file", "/dev/null"], obj={})

    assert result.exit_code == 2


@mock.patch("zsm.cli.open", mock.mock_open())
@mock.patch("zsm.config.load", mock.MagicMock())
def test_validate_config_returns_0_on_success():
    runner = CliRunner()
    result = runner.invoke(
        zsm.cli.program, ["validate-config", "--config-file", "/fake/path"], obj={}
    )

    assert result.exit_code == 0


@mock.patch("zsm.cli.open", mock.mock_open())
@mock.patch("zsm.config.load", mock.MagicMock(side_effect=zsm.config.ValidationError))
def test_validate_config_returns_1_on_validationerror():
    runner = CliRunner()
    result = runner.invoke(zsm.cli.program, ["validate-config"], obj={})

    assert result.exit_code == 1


@mock.patch("zsm.cli.open", mock.MagicMock(side_effect=FileNotFoundError))
def test_validate_config_returns_1_on_filenotfounderror():
    runner = CliRunner()
    result = runner.invoke(zsm.cli.program, ["validate-config"], obj={})

    assert result.exit_code == 1


def test_version_prints_version():
    runner = CliRunner()
    result = runner.invoke(zsm.cli.program, ["version"], obj={})

    assert result.exit_code == 0

    version = pkg_resources.get_distribution("zsm").version
    assert result.output.strip() == f"zsm {version}"


@mock.patch("zsm.cli.program")
def test_cli_calls_program(mock_program):
    zsm.cli.cli()
    mock_program.assert_called()
