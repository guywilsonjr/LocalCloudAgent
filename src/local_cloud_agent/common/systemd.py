from pysystemd import ServiceManager

from local_cloud_agent.common import constants


def reload_systemd():
    service_manager = ServiceManager(constants.lower_keyword)
    service_manager.reload()
    service_manager.restart()
