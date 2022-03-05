import datetime
import platform
import re
from pathlib import Path

import marshmallow
import yaml
from marshmallow import Schema, fields

from . import zfs


class ValidationError(Exception):
    pass


class DatasetField(fields.String):
    def _deserialize(self, value, attr, obj, **kwargs):
        return zfs.Dataset(name=value)

    def _validate(self, value):
        datasets = zfs.get_datasets()

        for dataset in datasets:
            if dataset == value:
                return dataset

        raise marshmallow.ValidationError("Dataset does not exist")


class LabelField(fields.String):
    pattern = r"[^a-zA-Z0-9-]"

    def _validate(self, value):
        matches = re.findall(self.pattern, value)
        if matches:
            formatted_matches = ", ".join([f"'{m}'" for m in matches])
            raise marshmallow.ValidationError(
                f"Contains invalid characters: {formatted_matches}"
            )

        return value


class FrequencyField(fields.String):
    pattern = r"(?P<value>\d+)(?P<unit>[a-zA-Z]+)"

    units = {
        "seconds": ["s", "sec", "second", "secs", "seconds"],
        "minutes": ["m", "min", "minute", "minutes"],
        "hours": ["h", "hour", "hours"],
        "days": ["d", "day", "days"],
        "weeks": ["w", "week", "weeks"],
    }

    def _deserialize(self, value, attr, obj, **kwargs):
        result = {}

        pattern = re.compile(self.pattern)
        matches = pattern.finditer(value)
        for match in matches:
            group = match.groupdict()

            found_unit = None

            for unit, aliases in self.units.items():
                if group["unit"].lower() in aliases:
                    found_unit = unit

            if found_unit is not None:
                result[found_unit] = int(group["value"])
            else:
                raise marshmallow.ValidationError(
                    f"Unit not supported: {group['unit']}"
                )

        return datetime.timedelta(**result)


class SnapshotSchema(Schema):
    dataset = DatasetField(required=True)
    label = LabelField(required=True)
    frequency = FrequencyField(required=True)
    retention = fields.Integer(required=True)


class ConfigSchema(Schema):
    snapshots = fields.Nested(SnapshotSchema, many=True, required=True)


def get_platform_path() -> Path:
    paths = {"FreeBSD": "/usr/local/etc/", "Linux": "/etc/"}
    system = platform.system()
    return Path(paths[system])


def get_path() -> Path:
    return get_platform_path() / "zsm.yaml"


def load(data: str) -> dict:
    try:
        data = yaml.safe_load(data)

    except yaml.YAMLError as e:
        msg = "Invalid YAML"

        problem = getattr(e, "problem", None)
        if problem is not None:
            msg += f": {e.problem}"

        problem_mark = getattr(e, "problem_mark", None)
        if problem_mark is not None:
            msg += (
                f": line={e.problem_mark.line + 1} column={e.problem_mark.column + 1}"
            )

        raise ValidationError(msg)

    try:
        data = ConfigSchema().load(data)

    except marshmallow.ValidationError as e:
        raise ValidationError(e.messages)

    return data
