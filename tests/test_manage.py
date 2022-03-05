import datetime
from unittest import mock

import freezegun

import zsm.manage
import zsm.zfs


def test_get_snapshots_finds_correct_items():
    label = "abc"
    valid_names = ["zsm_abc_11", "zsm_abc_22"]
    invalid_names = [
        "zsm_xyz_11",  # Wrong label.
        "zsm_abcc_11",  # Label is only partial match.
        "xyz_abc_11",  # Right pattern, but wrong prefix.
        "abc",  # Wrong prefix, and not enough parts.
        "zsm",  # Right prefix, but not enough parts.
        "zsm_abc_11_lol",  # Right prefix, and right label, but too many parts.
        "",  # Empty string should not even be possible to get.
    ]
    names = valid_names + invalid_names

    dataset = mock.MagicMock()

    with mock.patch(
        "zsm.zfs.get_snapshots",
        return_value=[zsm.zfs.Snapshot(dataset=dataset, name=name) for name in names],
    ):
        snapshots = zsm.manage.get_snapshots(dataset=dataset, label=label)

    # Assert that result only contains snapshots with valid names.
    assert snapshots == [
        zsm.zfs.Snapshot(dataset=dataset, name=name) for name in valid_names
    ]


def test_create_snaphot_calls_zfs_create_snapshot():
    dataset = mock.MagicMock()

    with mock.patch("zsm.zfs.create_snapshot") as mock_create_snapshot:
        zsm.manage.create_snapshot(dataset=dataset, label="asdf")

    assert mock_create_snapshot.called


def test_parse_snapshot_returns_correct_parts():
    expected_label = "daily"
    expected_timestamp = datetime.datetime.now()
    formatted_expected_timestamp = expected_timestamp.strftime(
        zsm.manage.SNAPSHOT_TIMESTAMP_FORMAT
    )

    label, timestamp = zsm.manage.parse_snapshot(
        snapshot=zsm.zfs.Snapshot(
            dataset=mock.MagicMock(),
            name=zsm.manage.SNAPSHOT_DELIMITER.join(
                [
                    zsm.manage.SNAPSHOT_PREFIX,
                    expected_label,
                    formatted_expected_timestamp,
                ]
            ),
        )
    )

    # Round down microseconds, because that is not stored in the snapshot name.
    expected_timestamp = expected_timestamp.replace(microsecond=0)

    assert label == expected_label
    assert timestamp == expected_timestamp


dataset = zsm.zfs.Dataset(name="tank/data")


@mock.patch("zsm.zfs.create_snapshot")
@mock.patch("zsm.zfs.destroy_snapshot")
@mock.patch(
    "zsm.zfs.get_snapshots",
    return_value=[
        zsm.zfs.Snapshot(dataset=dataset, name="zsm_often_2022-03-05T11:59:00"),
        zsm.zfs.Snapshot(dataset=dataset, name="zsm_often_2022-03-05T11:09:00"),
        zsm.zfs.Snapshot(dataset=dataset, name="zsm_often_2022-03-05T11:19:00"),
        zsm.zfs.Snapshot(dataset=dataset, name="zsm_often_2022-03-05T11:29:00"),
        zsm.zfs.Snapshot(dataset=dataset, name="zsm_often_2022-03-05T11:39:00"),
    ],
)
@freezegun.freeze_time("2022-03-05 11:45:00")
def test_manage_snapshots_calls_zfs_create_and_destroy(
    mocked_zfs_get_snapshots,
    mocked_zfs_destroy_snapshot,
    mocked_zfs_create_snapshot,
):
    config = dict(
        snapshots=[
            dict(
                dataset=dataset,
                label="often",
                frequency=datetime.timedelta(minutes=10),
                retention=5,
            )
        ]
    )

    zsm.manage.manage_snapshots(
        config=config,
        now=datetime.datetime(2022, 3, 5, 12, 11, 00),
        dry_run=False,
    )

    assert mocked_zfs_create_snapshot.call_args_list == [
        mock.call(
            dataset=dataset,
            name="zsm_often_2022-03-05T11:45:00",
        )
    ]
    assert mocked_zfs_destroy_snapshot.call_args_list == [
        mock.call(
            snapshot=zsm.zfs.Snapshot(
                dataset=dataset,
                name="zsm_often_2022-03-05T11:09:00",
            )
        ),
        mock.call(
            snapshot=zsm.zfs.Snapshot(
                dataset=dataset,
                name="zsm_often_2022-03-05T11:19:00",
            )
        ),
    ]
    assert mocked_zfs_get_snapshots.called
