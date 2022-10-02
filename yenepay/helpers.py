"""
YenePay helpers
"""
import re


class Validator:
    """Add attribute validation

    Validate attribute before value is assigned.
    """

    def __setattr__(self, attr, value):
        name = "_validate_{}".format(attr)
        if hasattr(self, name):
            getattr(self, name)(value)
        super().__setattr__(attr, value)


def to_python_attr(attr: str) -> str:
    """return a given attribute name into snake case.

    :param attr: attribute name need to be changed
    :type attr: :func:`str`

    :return: snake case of a given attibute.
    :rtype: :func:`str`
    """
    pattern = r"(?:[A-Z])[a-z0-9_]*"
    attr = attr.replace("ID", "Id")
    matches = re.findall(pattern, attr)

    return "_".join((match.lower() for match in matches))
