import socket
import struct
from typing import AsyncIterator, Dict

from aiofile import async_open


def get_addr_from_hex(hex_addr: str) -> str:
    pack_data = struct.unpack('<I', struct.pack('>I', int(hex_addr, 16)))
    addr = socket.inet_ntoa(struct.pack('!L', pack_data[0]))
    return addr



def get_addr_data(gateway_hex: str, destination_hex: str, mask_hex: str) -> Dict[str, str]:
    gateway_addr = get_addr_from_hex(gateway_hex)
    gateway_hostname = 'default' if gateway_addr == '0.0.0.0' else socket.gethostbyaddr(gateway_addr)[0]
    subnet_addr = get_addr_from_hex(destination_hex)
    mask_addr = get_addr_from_hex(mask_hex)
    return {
        'gateway_hostname': gateway_hostname,
        'gateway_addr': gateway_addr,
        'subnet_addr': subnet_addr,
        'mask_addr': mask_addr
    }


def process_route_line(line: str) -> Dict[str, str]:
    fields = line.strip().split()
    ifc_name = fields[0]
    destination_hex = fields[1]
    gateway_hex = fields[2]
    flags = fields[3]
    refcnt = fields[4]
    use = fields[5]
    metric = fields[6]
    mask_hex = fields[7]
    mtu = fields[8]
    window = fields[9]
    irtt = fields[10]
    addr_data = get_addr_data(gateway_hex, destination_hex, mask_hex)
    return {
        **addr_data,
        'ifc_name': ifc_name,
        'destination_hex': destination_hex,
        'gateway_hex': gateway_hex,
        'flags': flags,
        'refcnt': refcnt,
        'use': use,
        'metric': metric,
        'mask_hex': mask_hex,
        'mtu': mtu,
        'window': window,
        'irtt': irtt
    }



async def async_read_proc_net_route() -> AsyncIterator[str]:
    async with async_open('/proc/net/route') as f:
        await f.readline()  # skip the header
        while line := (await f.readline()).strip():
            if isinstance(line, bytes):
                yield line.decode()
            else:
                yield line


async def get_routes() -> list[Dict[str, str]]:
    """Read the default gateway directly from /proc."""
    return [process_route_line(line) async for line in async_read_proc_net_route()]

