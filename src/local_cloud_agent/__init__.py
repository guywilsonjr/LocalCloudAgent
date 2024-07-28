from importlib.metadata import version, PackageNotFoundError
print(__name__)

def get_version():
    try:
        return version('local-cloud-agent')
    except PackageNotFoundError:
        return 'Unknown'

__version__ = get_version()


