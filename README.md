# mullvad-ping-py
Python-based script to ping Mullvad relays

## Prerequisites
1. Python 3
2. PIP

## Steps
1. Clone the repository

```git clone https://github.com/Wind1337/mullvad-ping-py```

2. Install requirements

```pip install -r requirements.txt```

3. Run the script (Arguments are optional)

```python main.py <args>```

## Arguments
```
usage: main [-h] [--country COUNTRY] [--owned] [--server-type {ram,disk}] [--protocol {openvpn,wireguard,bridge}]
            [--exclude-protocol {openvpn,wireguard,bridge}] [--exclude-provider EXCLUDE_PROVIDER]

A Mullvad relay ping script

options:
  -h, --help            show this help message and exit
  --country COUNTRY     Ping servers from a certain country e.g.(us, uk, se)
  --owned               Ping only servers owned by Mullvad
  --server-type {ram,disk}
                        Select a server type to ping e.g.(ram, disk)
  --protocol {openvpn,wireguard,bridge}
                        Select a VPN protocol - Default: all
  --exclude-protocol {openvpn,wireguard,bridge}
                        Exclude a VPN protocol - Default: none
  --exclude-provider EXCLUDE_PROVIDER
                        Exclude a provider (M247)
```

## To-do:
1. Display servers with lowest ping at the end of the script (or script termination)
2. Customizable ping numbers, intervals and timeout
3. Optionally save results to a CSV file (?)
4. Additional arguments (?)