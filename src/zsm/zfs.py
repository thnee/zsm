import logging
import subprocess
from dataclasses import dataclass
from typing import Iterable


log = logging.getLogger(__name__)


@dataclass
class Dataset:
    name: str


@dataclass
class Snapshot:
    dataset: Dataset
    name: str


class ZfsOperationFailed(Exception):
    pass


def run(cmd: str) -> Iterable[str]:
    log.debug(f"Run: {cmd}")
    p = subprocess.run(args=cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        raise ZfsOperationFailed(p.stderr.split("\n")[0])
    return p.stdout.rstrip("\n").split("\n")


def get_datasets():
    lines = run("zfs list -H -t filesystem -o name")
    return [Dataset(name=line) for line in lines]


def get_snapshots(dataset: Dataset):
    lines = run(f"zfs list -H -r -t snapshot -o name -S creation {dataset.name}")

    snapshots = []
    for line in lines:
        _, name = line.split("@")
        snapshots.append(Snapshot(dataset=dataset, name=name))
    return snapshots


def create_snapshot(dataset: Dataset, name: str):
    run(f"zfs snapshot {dataset.name}@{name}")


def destroy_snapshot(snapshot: Snapshot):
    run(f"zfs destroy {snapshot.dataset.name}@{snapshot.name}")
