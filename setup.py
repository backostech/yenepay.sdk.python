import pathlib
import re

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent


def get_discription():
    """
    Read full description from `README.md`
    """

    with open("README.md", "r") as long_description:
        return long_description.read()


def get_version():
    """
    Read version
    """
    txt = (WORK_DIR / "yenepay" / "__init__.py").read_text("utf-8")
    try:
        return re.findall(
            r"^__version__\s+=\s+['|\"]([^']+)['|\"]\r?$", txt, re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


setup(
    name="yenepay",
    version=get_version(),
    author="Backos Technologies",
    author_email="info@backostech.com",
    description=(
        "Unofficial Python SDK for YenePay (https://yenepay.com)"
        " payment integration"
    ),
    long_description=get_discription(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "tests.*", "examples.*", "docs")),
    url="https://github.com/backostech/yenepay.sdk.python",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[
        "requests==2.28.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
