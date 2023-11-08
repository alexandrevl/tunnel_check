#!python3

import os
import socks
import socket
import requests
import time
from datetime import datetime
import subprocess
from colorama import Fore, Style
import platform

def is_tunnel_working(port=8080):
    try:
        socks.set_default_proxy(socks.SOCKS5, "localhost", port)
        socket.socket = socks.socksocket
        response = requests.get("http://144.22.144.218:8005/", timeout=2)
        if response.status_code == 200:
            return True
        else:
            print(f"Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        return False

def kill_tunnel(port):
    timestamp = datetime.now().strftime('%H:%M:%S')
    cmd = f"ps aux | grep 'ssh -D {port}' | grep -v grep | awk '{{print $2}}'"
    ssh_pid = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

    if ssh_pid:
        subprocess.run(f'kill {ssh_pid}', shell=True)
        print(f'{Fore.YELLOW}[{timestamp}] Tunnel killed (pid: {ssh_pid}){Style.RESET_ALL}')

def create_tunnel(port, ssh_user, ssh_host):
    cmd = f'ssh -D {port} -f -C -q -N {ssh_user}@{ssh_host} -o ServerAliveInterval=30 -o ServerAliveCountMax=2 -o ExitOnForwardFailure=True'
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def change_location(param_location):
    COMMAND = f'networksetup -switchtolocation {param_location}'
    RESULT = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (RESULT == "found it!"):
        return True
    else:
        return False    

def change_network_location(location):
    timestamp = datetime.now().strftime('%H:%M:%S')
    changed = change_location(location)
    if changed:
        print(f'{Fore.GREEN}[{timestamp}] Location set to {location}{Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}[{timestamp}] Failed to change to {location} location{Style.RESET_ALL}')

def main():
    try:
        port = 8080
        ssh_user = 'ubuntu'
        ssh_host = '144.22.144.218'
        interval = 3  # Seconds

        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            if not is_tunnel_working(port):
                kill_tunnel(port)
                print(f'{Fore.YELLOW}[{timestamp}] Tunnel not working. Creating a new one...{Style.RESET_ALL}')
                if create_tunnel(port, ssh_user, ssh_host):
                    change_network_location('Proxy')
                    print(f'{Fore.YELLOW}[{timestamp}] Tunnel created on port {port} with {ssh_user}@{ssh_host}{Style.RESET_ALL}')
                    print(f'{Fore.YELLOW}[{timestamp}] Tunnel setting up. Wait...{Style.RESET_ALL}', end='\r')
                else:
                    print(f'{Fore.RED}[{timestamp}] Failed to create tunnel.{Style.RESET_ALL}')
            else:
                print(f'{Fore.GREEN}[{timestamp}] {Style.BRIGHT}Tunnel is working.({interval}s){Style.RESET_ALL}                   ', end='\r')

            time.sleep(interval)  # Wait for X seconds before checking again
    except KeyboardInterrupt:
        timestamp = datetime.now().strftime('%H:%M:%S')
        print('')
        kill_tunnel(port)
        change_network_location('Automatic')
        print(f'[{timestamp}] {Style.BRIGHT}Bye!{Style.RESET_ALL}')

if __name__ == '__main__':
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] {Style.BRIGHT}Starting tunnel check. Press Ctrl+C to exit.{Style.RESET_ALL}')
    main()