import datetime
import logging
from typing import Dict, Iterable, Tuple

from . import zfs


log = logging.getLogger(__name__)

SNAPSHOT_DELIMITER = "_"
SNAPSHOT_PREFIX = "zsm"
SNAPSHOT_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_snapshots(dataset: zfs.Dataset, label: str) -> Iterable[zfs.Snapshot]:
    snapshots = zfs.get_snapshots(dataset=dataset)

    result = []

    for snapshot in snapshots:
        parts = snapshot.name.split(SNAPSHOT_DELIMITER)

        if len(parts) != 3:
            continue

        if parts[0] == SNAPSHOT_PREFIX and parts[1] == label:
            result.append(snapshot)

    return result


def create_snapshot(dataset: zfs.Dataset, label: str) -> None:
    timestamp = datetime.datetime.now().strftime(SNAPSHOT_TIMESTAMP_FORMAT)
    zfs.create_snapshot(
        dataset=dataset,
        name=SNAPSHOT_DELIMITER.join([SNAPSHOT_PREFIX, label, timestamp]),
    )


def parse_snapshot(snapshot: zfs.Snapshot) -> Tuple[str, datetime.datetime]:
    _, label, timestamp = snapshot.name.split(SNAPSHOT_DELIMITER)
    timestamp = datetime.datetime.strptime(timestamp, SNAPSHOT_TIMESTAMP_FORMAT)
    return label, timestamp


def manage_snapshots(config: Dict, now: datetime.datetime, dry_run: bool) -> None:
    for snapshot_config in config["snapshots"]:
        create_snapshots(
            now=now,
            dataset=snapshot_config["dataset"],
            label=snapshot_config["label"],
            frequency=snapshot_config["frequency"],
            dry_run=dry_run,
        )

    for snapshot_config in config["snapshots"]:
        destroy_snapshots(
            now=now,
            dataset=snapshot_config["dataset"],
            label=snapshot_config["label"],
            frequency=snapshot_config["frequency"],
            retention=snapshot_config["retention"],
            dry_run=dry_run,
        )


def create_snapshots(
    now: datetime.datetime,
    dataset: zfs.Dataset,
    label: str,
    frequency: datetime.timedelta,
    dry_run: bool,
) -> None:
    snapshots = get_snapshots(dataset=dataset, label=label)

    if len(snapshots) == 0:
        log.info(f"[{dataset.name}:{label}] No snapshots yet, creating the first one.")

        if not dry_run:
            create_snapshot(dataset=dataset, label=label)

    else:
        latest_snapshot = snapshots[0]
        _, latest_timestamp = parse_snapshot(snapshot=latest_snapshot)
        latest_age = now - latest_timestamp

        if latest_age > frequency:
            log.info(
                f"[{dataset.name}:{label}] "
                f"Latest snapshot ({latest_snapshot.name}) is {latest_age} old, "
                "creating new."
            )

            if not dry_run:
                create_snapshot(dataset=dataset, label=label)

        else:
            log.info(
                f"[{dataset.name}:{label}] "
                f"Latest snapshot ({latest_snapshot.name}) is only {latest_age} old, "
                "skipping."
            )


def destroy_snapshots(
    now: datetime.datetime,
    dataset: zfs.Dataset,
    label: str,
    frequency: datetime.timedelta,
    retention: int,
    dry_run: bool,
) -> None:
    snapshots = get_snapshots(dataset=dataset, label=label)

    any_old_found = False

    for snapshot in snapshots:
        label, timestamp = parse_snapshot(snapshot=snapshot)

        age = now - timestamp
        max_age = frequency * retention

        if age > max_age:
            log.info(
                f"[{dataset.name}:{label}] "
                f"Found old snapshot ({snapshot.name}), destroying it."
            )

            if not dry_run:
                zfs.destroy_snapshot(snapshot=snapshot)

            any_old_found = True

    if not any_old_found:
        log.info(f"[{dataset.name}:{label}] There are no old snapshots to destroy.")
