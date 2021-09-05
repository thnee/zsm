# SPDX-License-Identifier: BSD-2-Clause
import setuptools


setuptools.setup(
    name="zsm",
    version="0.3.0",
    keywords="zfs snapshots freebsd linux",
    description="ZFS Snapshot Manager",
    long_description="Please see the project links.",
    project_urls={
        "Documentation": "https://zsm.readthedocs.io/",
        "Source": "https://github.com/thnee/zsm",
    },
    license="BSD-2-Clause",
    author="Mattias Lindvall",
    author_email="mattias.lindvall@gmail.com",
    package_dir={"": "src"},
    packages=["zsm"],
    python_requires=">=3.7",
    install_requires=[
        "click~=8.0.1",
        "pid~=3.0.4",
        "pyyaml~=5.4.1",
        "marshmallow~=3.13.0",
    ],
    extras_require={
        "test": [
            "pytest~=6.2.5",
            "pytest-cov~=2.12.1",
            "flake8~=3.9.2",
            "flake8-bugbear~=21.4.3",
            "black~=21.8b0",
            "isort~=5.9.3",
        ],
        "build": [
            "wheel~=0.37.0",
            "twine~=3.4.2",
        ],
    },
    entry_points={"console_scripts": ["zsm = zsm.cli:cli"]},
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
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
