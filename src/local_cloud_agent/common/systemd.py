from pysystemd import ServiceManager
from common import constants
from pystemd.systemd1 import Unit


def reload_systemd():
    #unit = Unit(bytes(constants.service_fn))
    service_manager = ServiceManager(constants.lower_keyword)
    service_manager.reload()
    service_manager.restart()


