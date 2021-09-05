.. SPDX-License-Identifier: BSD-2-Clause

Command Line Interface
======================

Commands
--------

* ``cron`` : The main command that performs all work.
* ``validate-config``: Validate the configuration file.
* ``version`` : Prints the version of the program.

Commands are passed as the first argument to ``zsm``.

For example:

.. code-block:: text

    zsm version

Options to ``cron`` command
------------------------------

All of these options are optional.

.. program:: zsm cron

.. option:: --config-file <filename>

Path to a config file.

Default: ``/usr/local/etc/zsm.yaml`` on FreeBSD and ``/etc/zsm.yaml`` on Linux.

.. option:: --log-file <filename>

Path to a log file.

Default: ``/var/log/zsm.log``.

.. option:: --log-level <level>

Minimum log level that will be outputted.

Must be one of ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``.

Default: ``INFO``.

.. option:: --log-console

Print log output to stdout.

Default: Off.

.. option:: --dry-run

Disable all operations that make modifications.

Default: Off.

Options to ``validate-config`` command
-----------------------------------------

All of these options are optional.

.. program:: zsm validate-config

.. option:: --config-file <filename>

Path to a config file.

Default: ``/usr/local/etc/zsm.yaml`` on FreeBSD and ``/etc/zsm.yaml`` on Linux.

.. option:: --log-level <level>

Minimum log level that will be outputted.

Must be one of ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``.

Default: ``INFO``.
