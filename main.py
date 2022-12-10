from icmplib import ping, SocketPermissionError
import signal
import sys
import requests
import argparse

parser = argparse.ArgumentParser(description="A Mullvad relay ping script")
parser.add_argument("--country", dest="country", default=None,
                    help="Ping servers from a certain country e.g.(us, uk, se)")
parser.add_argument("--owned", dest="owned", default=None, action='store_true',
                    help="Ping only servers owned by Mullvad")
parser.add_argument("--server-type", dest="server_type", default=None, choices=['ram', 'disk'],
                    help="Select a server type to ping e.g.(ram, disk)")
parser.add_argument("--protocol", dest="use_protocol", default="all", choices=['openvpn', 'wireguard', 'bridge'],
                    help="Select a VPN protocol - Default: all")
parser.add_argument("--exclude-protocol", dest="exclude_protocol", default=None,
                    choices=['openvpn', 'wireguard', 'bridge'],
                    help="Exclude a VPN protocol - Default: none")
parser.add_argument("--exclude-provider", dest="exclude_provider", default=None, help="Exclude a provider (M247)")

args = parser.parse_args()

# Ping country
country = args.country

# Owned server
owned_flag = args.owned

# Server type
server_type = args.server_type

# Protocols: all, openvpn, wireguard, bridge
# Default: all
use_protocol = args.use_protocol

# Exclude Providers
exclude_provider = args.exclude_provider

# Exclude Protocol
exclude_protocol = args.exclude_protocol


def handler(signum, frame):
    sys.exit(0)


def check_skip(country_code, provider, protocol, stboot, owned):
    if country:
        if country_code != country:
            return True
    if owned_flag:
        if owned is False:
            return True
    if server_type:
        if stboot:
            if server_type == "disk":
                return True
        else:
            if server_type == "ram":
                return True
    if provider == exclude_provider:
        return True
    if protocol == exclude_protocol:
        return True
    return False


signal.signal(signal.SIGINT, handler)

api_url = "https://api.mullvad.net/www/relays/"
api_url += use_protocol

print("Fetching relay list from Mullvad...")
try:
    response = requests.get(api_url)
except requests.exceptions.ConnectionError:
    print("An exception occurred while attempting to connect to Mullvad API")
    print("Mullvad API Fetch Failed")
    sys.exit(1)

if response.status_code != requests.codes.ok:
    print("Mullvad API Fetch Failed")
    sys.exit(1)

response_json = response.json()

count = 5
interval = 0.2
timeout = 3

print("Testing ping functionality...")
try:
    host = ping("8.8.8.8", count=1, timeout=timeout)
except SocketPermissionError:
    print("You require elevated privileges to run icmplib")
    print("Rerun with sudo or as administrator")

print("Initiating ping operation with parameters: count={count}, interval={interval:.0f}ms, timeout={timeout}s \n"
      .format(count=count, interval=interval * 1000, timeout=timeout))
for i in range(len(response_json)):
    country_code = response_json[i]["country_code"]
    ip_addr = response_json[i]["ipv4_addr_in"]
    hostname = response_json[i]["hostname"]
    stboot = response_json[i]["stboot"]
    owned = response_json[i]["owned"]
    if use_protocol == "all":
        protocol = response_json[i]["type"]
    else:
        protocol = use_protocol
    provider = response_json[i]["provider"]
    if check_skip(country_code, provider, protocol, stboot, owned):
        continue
    host = ping(ip_addr, count=count, interval=interval, timeout=timeout)
    if host.is_alive:
        avg_ping = str(round(host.avg_rtt, 2)) + "ms"
        print("Pinged {hostname:15s}| latency={avg_ping:10s} protocol={protocol:10s} provider={provider:10s}"
              .format(hostname=hostname, avg_ping=avg_ping, protocol=protocol, provider=provider))
    else:
        print("Failed to ping {hostname}".format(hostname=hostname))
