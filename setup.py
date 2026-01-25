from setuptools import setup, find_packages

setup(
    name="digitalchild-api",
    version="0.1.0",
    packages=find_packages(include=["api", "api.*"]),
    python_requires=">=3.12",
)
