from pysystemd import ServiceManager

from common import constants


def reload_systemd():
    service_manager = ServiceManager(constants.lower_keyword)
    service_manager.reload()
    service_manager.restart()
