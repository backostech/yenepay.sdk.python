from setuptools import find_packages, setup


def get_discription():
    """
    Read full description from `README.md`
    """

    with open("README.md", "r") as long_description:
        return long_description.read()


def get_requirements():
    """
    Return all requirements from `requirements.txt`
    """

    with open("requirements.txt", "r") as requirements:
        return [line.strip() for line in requirements.readlines()]


setup(
    name="yenepay",
    version="0.2.0",
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
    install_requires=get_requirements(),
)
