import asyncio
import fcntl
import os
import socket
import struct
from typing import Tuple

from aiofile import async_open
from cumulonimbus_models.network import NetworkInterface

from configuration import home_dir


ifc_dir_loc = f'/{home_dir}/host/sys/class/net/'


def get_ip_address(ifc_name: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifc_name[:15])
        )[20:24])



async def fetch_ifcs(ifc_name: str) -> NetworkInterface:
    async with async_open(f'{ifc_dir_loc}/{ifc_name}/address') as f:
        mac_address = (await f.read()).strip()
    ip_address = get_ip_address(ifc_name)
    return NetworkInterface(name=ifc_name, mac_address=mac_address, ip_address=ip_address)


async def get_ifcs() -> Tuple[NetworkInterface]:
    ifc_names = os.listdir(ifc_dir_loc)
    return await asyncio.gather(*[await fetch_ifcs(ifc_name) for ifc_name in ifc_names])
