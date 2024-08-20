import importlib.metadata


def get_version() -> str:
    try:
        return importlib.metadata.version('local-cloud-agent')
    except importlib.metadata.PackageNotFoundError:
        return 'Unknown'


__version__ = get_version()

