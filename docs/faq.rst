.. SPDX-License-Identifier: BSD-2-Clause

FAQ
===

How does zsm store its meta data?
---------------------------------

All meta data is stored in the name of the snapshot.
Everything zsm does is calculated at run time,
based on the current configuration file and existing snapshots in ZFS.

- All meta data is immediately visible to the user in the snapshot name.
- There is no hidden meta data stored in properties or attributes.
- There is no database or other third party storage.

Will zsm interfere with other snapshots?
----------------------------------------

Nope.
Zsm will only manage snapshots that starts with ``zsm``.
As long as you avoid creating snapshots that starts with ``zsm``
using other tools than zsm itself, it will be fine.

What happens when removing a snapshot config?
---------------------------------------------

Zsm will only manage snapshots for the list of snapshot configs
that are in the configuration file at the moment when it starts.
Any existing snaphots created from an older configuration file
will simply remain in ZFS, and can safely be destroyed manually.

If you want to have zsm clean up existing snapshots before removing a snapshot config,
set ``retention`` to ``0`` and let zsm run once.
