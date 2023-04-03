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


def check_skip(country_code, provider, protocol, stboot, owned, country, owned_flag, server_type, exclude_provider, exclude_protocol):
    if country:
        if country_code not in country:
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
    if exclude_provider:
        if provider in exclude_provider:
            return True
    if protocol == exclude_protocol:
        return True
    return False
