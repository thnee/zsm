Changelog
=========

0.3.0
^^^^^

Move library code from zsm-lib into zsm.

Remove dependency on sarge.

Update dependencies to newer versions.

Update project config files to more modern patterns.

0.2.1
^^^^^

Update requirements to newer versions.

Fix crash in _deserialize after upgrading to marshmallow 3.

0.2.0
^^^^^

Start including tests in source packages.

Snapshot config field ``name`` renamed to ``label``,
to avoid confusion with the actual ZFS snapshot name.
Also improved validation.

Snapshot config field ``delta`` renamed to ``frequency``,
because it makes more sense grammatically.
Also changed implementation from simple dict to complex string.
See :doc:`quickstart` and :doc:`config` for more information.

Fix bug where it would incorrectly find and manage snapshots
where the label was only a partial match.
Add regression test to detect this bug.

Start including tests in source packages.

Improve test coverage.

0.1.0
^^^^^

Initial release.

Add commands:

- ``cron``
- ``validate-config``
- ``version``
