import argparse
import logging
import socket
from time import sleep

from zeroconf import IPVersion, ServiceInfo, Zeroconf

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument('--v6', action='store_true')
    version_group.add_argument('--v6-only', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
    if args.v6:
        ip_version = IPVersion.All
    elif args.v6_only:
        ip_version = IPVersion.V6Only
    else:
        ip_version = IPVersion.V4Only

    switch_name = "Fake Orro Switch"
    service_type = "_edisonswitch._tcp.local."
    ip_address = get_ip_address()


    properties = {
        'aosp_version': 'release.22.37.5',
        'app_version': '6.10.1',
        'id': 'fba7ff34-ae7c-47cc-b49f-bfc03c802731',
        'home_id': 'd5d8ed98-e989-4863-9242-826fe24953cp',
        'ip_address': ip_address,
        'visibility': 'VISIBLE'
    }

    info = ServiceInfo(
        service_type,
        f"{switch_name}.{service_type}",
        addresses=[socket.inet_aton(ip_address)],
        port=8080,
        properties=properties,
        server="OrroOne-XXXXXX.local.",
    )

    zeroconf = Zeroconf(ip_version=ip_version)
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()