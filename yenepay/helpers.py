"""
YenePay helpers
"""


class Validator:
    """Add attribute validation

    Validate attribute before value is assigned.
    """

    def __setattr__(self, attr, value):
        name = "_validate_{}".format(attr)
        if hasattr(self, name):
            getattr(self, name)(value)
        super().__setattr__(attr, value)
