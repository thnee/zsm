import textwrap
from pathlib import Path
from unittest import mock

import marshmallow
import pytest

import zsm.config
import zsm.zfs


datasets = [
    zsm.zfs.Dataset(name="tank/a"),
    zsm.zfs.Dataset(name="tank/b"),
    zsm.zfs.Dataset(name="tank/c"),
]


@mock.patch("platform.system", mock.MagicMock(return_value="FreeBSD"))
def test_get_platform_path_returns_correct_path_on_freebsd():
    path = zsm.config.get_platform_path()

    assert path == Path("/usr/local/etc")


@mock.patch("platform.system", mock.MagicMock(return_value="Linux"))
def test_get_platform_path_returns_correct_path_on_linux():
    path = zsm.config.get_platform_path()

    assert path == Path("/etc")


def test_get_path():
    path = zsm.config.get_path()
    assert path == zsm.config.get_platform_path() / "zsm.yaml"


@mock.patch("zsm.zfs.get_datasets", mock.MagicMock(return_value=datasets))
def test_schema_raises_validationerror_for_invalid_dataset_name():
    data = {"snapshots": [{"dataset": "invalid/invalid"}]}

    with pytest.raises(marshmallow.ValidationError) as e:
        data = zsm.config.ConfigSchema().load(data)

    assert "Dataset does not exist" in e.value.messages["snapshots"][0]["dataset"]


@mock.patch("zsm.zfs.get_datasets", mock.MagicMock(return_value=datasets))
def test_load_works_with_valid_data():
    data = """\
    snapshots:
      - dataset: "tank/a"
        label: "hourly"
        frequency: "1h"
        retention: 24
    """

    zsm.config.load(data=textwrap.dedent(data))


@mock.patch("zsm.zfs.get_datasets", mock.MagicMock(return_value=datasets))
def test_load_raises_validationerror_for_invalid_datas():
    datas = [
        # Invalid YAML.
        "!@#",
        # Missing fields.
        """\
        snapshots:
          - dataset: "tank/a"
        """,
        # Label contains invalid character.
        """\
        snapshots:
          - dataset: "tank/a"
            label: "_"
            frequency: "1h"
            retention: 1
        """,
        # Frequency contains invalid unit.
        """\
        snapshots:
          - dataset: "tank/a"
            label: "a"
            frequency: "1p"
            retention: 1
        """,
    ]

    for data in datas:
        with pytest.raises(zsm.config.ValidationError):
            zsm.config.load(data=textwrap.dedent(data))
