import pyroute2
import logging
logging.basicConfig(level=logging.INFO)

ip = pyroute2.IPDB()
try:
    default_iface = ip.interfaces[ip.routes['default']['oif']]['ifname']
finally:
    if ip._stop:
        ip.release()

print(default_iface)
