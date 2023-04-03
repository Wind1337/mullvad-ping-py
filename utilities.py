import sys


def handler(signum, frame, print_func):
    print_func()
    sys.exit(0)


def print_results(results):
    results = sorted(results, key=lambda d: d['latency'])
    print("\nRESULTS\n")
    print("Servers with the lowest latency")
    if len(results) < 5:
        for j in range(len(results)):
            print("Hostname: {hostname:15s}| latency: {latency:10s} protocol: {protocol:10s} provider: {provider:10s}"
                  .format(hostname=results[j]["hostname"], latency=str(results[j]["latency"]) + "ms",
                          protocol=results[j]["protocol"], provider=results[j]["provider"]))
    else:
        for j in range(5):
            print("Hostname: {hostname:15s}| latency: {latency:10s} protocol: {protocol:10s} provider: {provider:10s}"
                  .format(hostname=results[j]["hostname"], latency=str(results[j]["latency"]) + "ms",
                          protocol=results[j]["protocol"], provider=results[j]["provider"]))


def check_skip(country_code, provider, protocol, stboot, owned, country, owned_flag, server_type,
               exclude_provider, exclude_protocol):
    return (
            (country and country_code not in country) or
            (owned_flag and not owned) or
            (server_type and ((stboot and server_type == "disk") or (not stboot and server_type == "ram"))) or
            (exclude_provider and provider in exclude_provider) or
            (protocol == exclude_protocol)
    )
