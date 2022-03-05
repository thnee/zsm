Quickstart
==========

Step 1: Create config file
--------------------------

The default location is
``/usr/local/etc/zsm.yaml`` on FreeBSD and ``/etc/zsm.yaml`` on Linux.

.. code-block:: yaml

    snapshots:
      - dataset: "tank/data"
        label: "daily"
        frequency: "1d"
        retention: 30

      - dataset: "tank/data"
        label: "hourly"
        frequency: "1h"
        retention: 24

Step 2: Verify configuration
----------------------------

Not required, but a good sanity check.

Validate the config file
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    sudo zsm validate-config

Perform a dry run
^^^^^^^^^^^^^^^^^

.. code-block:: text

    sudo zsm cron --dry-run --log-console


Step 3: Add to crontab
----------------------

Add a line to crontab as the root user, passing the ``cron`` command to zsm.

.. code-block:: text

    */1 * * * * zsm cron

The log file is by default located at ``/var/log/zsm.log``,
and the default log level is ``INFO``.

If you need help creating a crontab line, check out `crontab guru`_.

.. _crontab guru: https://crontab.guru/
