# SPDX-License-Identifier: BSD-2-Clause
import setuptools


setuptools.setup(
    name="zsm",
    version="0.2.1",
    keywords="zfs snapshots freebsd linux",
    description="ZFS Snapshot Manager",
    long_description="Please see the project links.",
    project_urls={
        "Documentation": "https://zsm.readthedocs.io/",
        "Source": "https://gitlab.com/thnee/zsm",
    },
    license="BSD-2-Clause",
    author="Mattias Lindvall",
    author_email="mattias.lindvall@gmail.com",
    package_dir={"": "src"},
    packages=["zsm"],
    python_requires=">=3.6",
    install_requires=["click~=7.1.2", "pid~=3.0.4", "zsm-lib~=0.2.1"],
    entry_points={"console_scripts": ["zsm = zsm.cli:cli"]},
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Filesystems",
    ],
)
