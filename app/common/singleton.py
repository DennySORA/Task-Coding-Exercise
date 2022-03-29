"""Singleton Pattern."""


class Singleton(object):
    """Singleton Pattern Class."""
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
