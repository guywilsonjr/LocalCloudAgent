from importlib.metadata import version, PackageNotFoundError


def get_version() -> str:
    try:
        return version('local-cloud-agent')
    except PackageNotFoundError:
        return 'Unknown'


__version__ = get_version()

