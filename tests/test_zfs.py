# SPDX-License-Identifier: BSD-2-Clause
from unittest import mock

import pytest

import zsm.zfs


def get_mocked_subprocess_run_pipeline(returncode=0, stdout="", stderr=""):
    def get_out_err(value):
        if isinstance(value, list):
            return "\n".join(value)
        return value

    mocked_pipeline = mock.MagicMock()
    mocked_pipeline.returncode = returncode
    mocked_pipeline.stdout = get_out_err(stdout)
    mocked_pipeline.stderr = get_out_err(stderr)

    return mocked_pipeline


@mock.patch(
    "subprocess.run",
    return_value=get_mocked_subprocess_run_pipeline(
        returncode=0,
    ),
)
def test_run_with_success(mocked_subprocess_run):
    zsm.zfs.run("asdf")
    mocked_subprocess_run.assert_called()


@mock.patch(
    "subprocess.run",
    return_value=get_mocked_subprocess_run_pipeline(returncode=1, stderr="a problem?"),
)
def test_run_with_failure(mocked_subprocess_run):
    with pytest.raises(zsm.zfs.ZfsOperationFailed) as e:
        zsm.zfs.run("asdf")

    mocked_subprocess_run.assert_called()
    assert str(e.value) == "a problem?"


@mock.patch(
    "subprocess.run",
    return_value=get_mocked_subprocess_run_pipeline(
        stdout=["tank/a", "tank/b"],
    ),
)
def test_get_datasets(mocked_subprocess_run):
    datasets = zsm.zfs.get_datasets()

    mocked_subprocess_run.assert_called()
    assert datasets[0].name == "tank/a"
    assert datasets[1].name == "tank/b"


@mock.patch(
    "subprocess.run",
    return_value=get_mocked_subprocess_run_pipeline(
        stdout=["tank/a@abc", "tank/a@xyz"],
    ),
)
def test_get_snapshots(mocked_subprocess_run):
    snapshots = zsm.zfs.get_snapshots(dataset=zsm.zfs.Dataset(name="tank/a"))

    mocked_subprocess_run.assert_called()
    assert snapshots[0].name == "abc"
    assert snapshots[1].name == "xyz"


@mock.patch(
    "subprocess.run",
    return_value=get_mocked_subprocess_run_pipeline(),
)
def test_create_snapshot(mocked_subprocess_run):
    zsm.zfs.create_snapshot(dataset=zsm.zfs.Dataset(name="tank/a"), name="asdf")
    mocked_subprocess_run.assert_called()


@mock.patch(
    "subprocess.run",
    return_value=get_mocked_subprocess_run_pipeline(),
)
def test_destroy_snapshot(mocked_subprocess_run):
    zsm.zfs.destroy_snapshot(
        snapshot=zsm.zfs.Snapshot(dataset=zsm.zfs.Dataset(name="tank/a"), name="asdf")
    )
    mocked_subprocess_run.assert_called()
