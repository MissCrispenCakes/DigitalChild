# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

from setuptools import find_packages, setup

setup(
    name="digitalchild-api",
    version="0.1.0",
    packages=find_packages(include=["api", "api.*"]),
    python_requires=">=3.12",
)
