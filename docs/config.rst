.. SPDX-License-Identifier: BSD-2-Clause

Configuration file
==================

The config file is a YAML file where the top level object is a mapping.

Fields
------

- ``snapshots`` (List of mappings) - Define what snapshots to take.

  - ``dataset`` (String) - Name of an existing dataset, including pool name. |br|
    Example: ``tank/data``.
  - ``label`` (String) - Descriptive short name, typically describing the frequency. |br|
    Examples: ``daily``, ``weekly``, ``every-2-minutes``.
  - ``frequency`` (String) - Define how often the snapshot should be taken. |br|
    Can contain multiple values consisting of a number and a unit. |br|
    Supported units are ``weeks``, ``days``, ``hours``, ``minutes``, ``seconds``,
    including various abbreviations like ``w``, ``d``, ``h``, ``min``, ``sec``. |br|
    Examples: ``2w``, ``3d 12h``, ``2Weeks3DAYS 5h,3mins,2secs``.
  - ``retention`` (Integer) - Number of old snapshots to keep. |br|
    Example: ``12``.

.. |br| raw:: html

   <br />
