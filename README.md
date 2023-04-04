# mullvad-ping-py
Python-based script to ping Mullvad relays

## Running from source

### Prerequisites
1. Python 3 (3.7+ recommended, tested with 3.8 - 3.11)
2. PIP

### Steps
1\. Clone the repository

```git clone https://github.com/Wind1337/mullvad-ping-py```

2\. Install requirements

Windows

```pip install -r requirements.txt```

Mac/Linux

```pip3 install -r requirements.txt```

3\. Run the script (Arguments are optional)

Windows

```python main.py <args>```

Mac/Linux

```python3 main.py <args>```

## Running prebuilt executable

### Windows (Command Prompt)
```
mullvad-ping-py <args>
```

### Windows (Powershell)
```
.\mullvad-ping-py <args>
```

### Linux
```
chmod +x mullvad-ping-py
./mullvad-ping-py <args>
```
(Root required)
If you get the error ```You require elevated privileges to run icmplib``` run with
```
chmod +x mullvad-ping-py
sudo ./mullvad-ping-py <args>
```

## Arguments
```
usage: mullvad-ping-py.exe [-h] [--owned] [--country COUNTRY] [--server-type {ram,disk}] [--protocol {openvpn,wireguard,bridge}] [--exclude-protocol {openvpn,wireguard,bridge}] [--exclude-provider EXCLUDE_PROVIDER] [--count COUNT]
                           [--interval INTERVAL] [--timeout TIMEOUT]

A Mullvad relay ping script

options:
  -h, --help            show this help message and exit
  --owned               Ping only servers owned by Mullvad
  --country COUNTRY     Ping servers from a certain country e.g.(us, gb, se). To ping multiple countries, concatenate with '+' e.g. us+gb
  --server-type {ram,disk}
                        Select a server type to ping e.g.(ram, disk)
  --protocol {openvpn,wireguard,bridge}
                        Select a VPN protocol - Default: all
  --exclude-protocol {openvpn,wireguard,bridge}
                        Exclude a VPN protocol - Default: none
  --exclude-provider EXCLUDE_PROVIDER
                        Exclude a provider. Case-Sensitive. To exclude multiple providers, concatenate with '+' e.g. M247+xtom
  --count COUNT         Number of times to ping each host
  --interval INTERVAL   Interval time between each ping (ms)
  --timeout TIMEOUT     Time to wait before timeout (s)
  --concurrent CONCURRENT
                        Concurrent multiping tasks
```

## Argument examples
All arguments can be used concurrently at the same time in no particular order

### Ping only servers owned by Mullvad
```
mullvad-ping-py --owned
```

### Ping only USA servers
```
mullvad-ping-py --country us
```

### Ping only USA and UK servers
```
mullvad-ping-py --country us+gb
```

### Ping only servers running from RAM (stboot)
```
mullvad-ping-py --server-type ram
```

### Ping only wireguard servers
```
mullvad-ping-py --protocol wireguard
```

### Don't ping bridge servers
```
mullvad-ping-py --exclude-protocol bridge
```

### Don't ping M247 servers
```
mullvad-ping-py --exclude-provider M247
```

### Don't ping M247 and xtom servers
```
mullvad-ping-py --exclude-provider M247+xtom
```

### Ping each server 3 times to get the average latency
```
mullvad-ping-py --count 3
```

### Wait 100ms between each ping
⚠ Not recommended to set this value to 50 or lower
```
mullvad-ping-py --interval 100
```

### Wait 1 second before timing out the ping request
```
mullvad-ping-py --timeout 1
```

### Ping 100 servers concurrently
⚠ You may experience system-wide instability with a value higher than 1000
```
mullvad-ping-py --concurrent 100
```

## To-do:
- [x] Display servers with lowest ping at the end of the script (or script termination)
- [x] Customizable ping numbers, intervals and timeout
- [ ] Optionally save results to a CSV file (?)
- [ ] Additional arguments (?)