VERSION = (0, 3, 0, 'alpha', 0)


def get_version(*args, **kwargs):
    from django.utils.version import get_version
    return get_version(VERSION)
