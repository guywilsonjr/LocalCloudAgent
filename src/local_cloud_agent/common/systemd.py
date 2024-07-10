from common.configuration import agent_config
from pystemd.systemd1 import Manager, Unit


def reload_systemd() -> None:
    unit: Manager = Unit(agent_config.installed_service_fp.encode())
    unit.load()
    unit.Unit.Restart(b'fail')




