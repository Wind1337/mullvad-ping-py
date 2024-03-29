import signal
import sys
import requests
import argparse
from icmplib import ping, multiping, SocketPermissionError
from utilities import handler, split_into_parts, print_results, check_skip
from tqdm import tqdm

parser = argparse.ArgumentParser(description="A Mullvad relay ping script")
parser.add_argument(
    "--owned",
    dest="owned",
    default=None,
    action="store_true",
    help="Ping only servers owned by Mullvad",
)
parser.add_argument(
    "--country",
    dest="country",
    default=None,
    help="Ping servers from a certain country e.g.(us, gb, se). "
    "To ping multiple countries, concatenate with '+' e.g. us+gb",
)
parser.add_argument(
    "--server-type",
    dest="server_type",
    default=None,
    choices=["ram", "disk"],
    help="Select a server type to ping e.g.(ram, disk)",
)
parser.add_argument(
    "--protocol",
    dest="use_protocol",
    default="all",
    choices=["openvpn", "wireguard", "bridge"],
    help="Select a VPN protocol - Default: all",
)
parser.add_argument(
    "--exclude-protocol",
    dest="exclude_protocol",
    default=None,
    choices=["openvpn", "wireguard", "bridge"],
    help="Exclude a VPN protocol - Default: none",
)
parser.add_argument(
    "--exclude-provider",
    dest="exclude_provider",
    default=None,
    help="Exclude a provider. Case-Sensitive. To exclude multiple providers, concatenate with '+' "
    "e.g. M247+xtom",
)
parser.add_argument(
    "--count", dest="count", default=5, help="Number of times to ping each host"
)
parser.add_argument(
    "--interval",
    dest="interval",
    default=200,
    help="Interval time between each ping (ms)",
)
parser.add_argument(
    "--timeout", dest="timeout", default=3, help="Time to wait before timeout (s)"
)
parser.add_argument(
    "--concurrent", dest="concurrent", default=50, help="Concurrent multiping tasks"
)

args = parser.parse_args()

# Owned server
owned_flag = args.owned

# Ping country
if args.country:
    country = args.country.split("+")
else:
    country = None

# Server type
server_type = args.server_type

# Protocols: all, openvpn, wireguard, bridge
# Default: all
use_protocol = args.use_protocol

# Exclude Providers
if args.exclude_provider:
    exclude_provider = args.exclude_provider.split("+")
else:
    exclude_provider = None

# Exclude Protocol
exclude_protocol = args.exclude_protocol

count = int(args.count)
interval = float(args.interval) / 1000
timeout = int(args.timeout)
concurrent = int(args.concurrent)

results = []
errors = []

signal.signal(
    signal.SIGINT,
    lambda signum, frame: handler(signum, frame, lambda: print_results(results)),
)

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

print("Testing ping functionality...")
try:
    host = ping("8.8.8.8", count=1, timeout=timeout, privileged=False)
except SocketPermissionError:
    print("You require elevated privileges to run icmplib")
    print("Rerun with sudo or as administrator")
    sys.exit(1)

print(
    f"Initiating multiping operation with parameters: count={count}, interval={interval * 1000:.0f}ms, "
    f"timeout={timeout}s, concurrent_tasks={concurrent}"
)
ip_list = []
host_data = []

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

    if not check_skip(
        country_code,
        provider,
        protocol,
        stboot,
        owned,
        country,
        owned_flag,
        server_type,
        exclude_provider,
        exclude_protocol,
    ):
        ip_list.append(ip_addr)
        host_data.append(
            {
                "country_code": country_code,
                "ip_addr": ip_addr,
                "hostname": hostname,
                "stboot": stboot,
                "owned": owned,
                "protocol": protocol,
                "provider": provider,
            }
        )

batch_size = 1
if len(ip_list) > concurrent:
    parts = -(len(ip_list) // -concurrent)
    ip_list_batches = list(split_into_parts(ip_list, parts))
    host_data_batches = list(split_into_parts(host_data, parts))
    batch_size = len(ip_list_batches)
else:
    ip_list_batches = [ip_list]
    host_data_batches = [host_data]

print(f"Split target list into {batch_size} batches \n")

for ip_batch, host_batch in tqdm(
    zip(ip_list_batches, host_data_batches), total=batch_size, desc="Pinging"
):
    hosts = multiping(
        ip_batch,
        count=count,
        interval=interval,
        timeout=timeout,
        concurrent_tasks=concurrent,
        privileged=False,
    )
    for host in hosts:
        ip_addr = host.address
        matching_host_data = next(
            filter(lambda h: h["ip_addr"] == ip_addr, host_batch), None
        )

        if matching_host_data:
            hostname = matching_host_data["hostname"]
            protocol = matching_host_data["protocol"]
            provider = matching_host_data["provider"]
            stboot = matching_host_data["stboot"]
            owned = matching_host_data["owned"]
            if host.is_alive:
                avg_ping = str(round(host.avg_rtt, 2)) + "ms"
                result_dict = {
                    "hostname": hostname,
                    "latency": round(host.avg_rtt, 2),
                    "protocol": protocol,
                    "stboot": stboot,
                    "provider": provider,
                    "owned": owned,
                }
                results.append(result_dict)
                tqdm.write(
                    f"Pinged {hostname:15s}| latency={avg_ping:10s} protocol={protocol:10s} provider={provider:10s}"
                )
            else:
                result_dict = {"hostname": hostname, "latency": "timeout"}
                errors.append(result_dict)
                tqdm.write(f"Failed to ping {hostname} ({ip_addr})")

print_results(results)
