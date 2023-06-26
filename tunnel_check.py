import os
import socket
import time
from datetime import datetime
import subprocess
from colorama import Fore, Style

def is_tunnel_working(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', port))
        sock.close()
        return False
    except socket.error as e:
        if e.errno == 48:
            return True
        else:
            raise

def kill_tunnel(port):
    timestamp = datetime.now().strftime('%H:%M:%S')
    cmd = f"ps aux | grep 'ssh -D {port}' | grep -v grep | awk '{{print $2}}'"
    ssh_pid = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

    if ssh_pid:
        subprocess.run(f'kill {ssh_pid}', shell=True)
        print(f'\n{Fore.GREEN}[{timestamp}] Tunnel killed (pid: {ssh_pid}){Style.RESET_ALL}')

def create_tunnel(port, ssh_user, ssh_host):
    cmd = f'ssh -D {port} -f -C -q -N {ssh_user}@{ssh_host} -o ServerAliveInterval=10 -o ServerAliveCountMax=1 -o ExitOnForwardFailure=True'
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    try:
        last_ssid_check = False
        port = 8080
        ssh_user = 'ubuntu'
        ssh_host = '144.22.144.218'
        is_working = False
        interval = 3

        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            ssid_check = check_wifi()
            
            if not is_tunnel_working(port):
                is_working = False
                print(f'{Fore.YELLOW}[{timestamp}] Tunnel not working. Creating a new one...{Style.RESET_ALL}')
                if create_tunnel(port, ssh_user, ssh_host):
                    print(f'{Fore.YELLOW}[{timestamp}] Tunnel created on port {port} with {ssh_user}@{ssh_host}{Style.RESET_ALL}')
                    change_bb_location()
                else:
                    back_location = change_location('Automatic')
                    # if back_location:
                    #     print(f'[{timestamp}] Location set to Automatic')
                    print(f'{Fore.RED}[{timestamp}] Failed to create tunnel.{Style.RESET_ALL}')
            else:
                if ssid_check != last_ssid_check & ssid_check:
                    change_bb_location()
                print(f'{Fore.GREEN}{Style.BRIGHT}[{timestamp}] Tunnel is working.({interval}s){Style.RESET_ALL}', end='\r')
                is_working = True
            last_ssid_check = ssid_check

            time.sleep(interval)  # Wait for X seconds before checking again
    except KeyboardInterrupt:
        timestamp = datetime.now().strftime('%H:%M:%S')
        kill_tunnel(port)
        change_automatic_location()
        print(f'[{timestamp}] Bye!')

def check_wifi(ssid_target = "88200Wireless-d"):
    COMMAND = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep SSID | tail -1 | awk '{print $2}'"
    SSID = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (SSID == ssid_target):
    # if (SSID == "hNet"):
        return True
    else:
        return False

def get_location(param_location):
    COMMAND = "networksetup -getcurrentlocation"
    LOCATION = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (LOCATION == param_location):
        return True
    else: 
        return False

def change_location(param_location):
    COMMAND = f'networksetup -switchtolocation {param_location}'
    RESULT = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (RESULT == "found it!"):
        return True
    else:
        return False    

def change_bb_location():
    timestamp = datetime.now().strftime('%H:%M:%S')
    changed = change_location('BB')
    if changed:
        print(f'{Fore.GREEN}[{timestamp}] Location set to BB{Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}[{timestamp}] Failed to change to BB location{Style.RESET_ALL}')

def change_automatic_location():
    timestamp = datetime.now().strftime('%H:%M:%S')
    changed = change_location('Automatic')
    if changed:
        print(f'{Fore.GREEN}[{timestamp}] Location set to Automatic{Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}[{timestamp}] Failed to change to Automatic location{Style.RESET_ALL}')


if __name__ == '__main__':
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f'{Style.BRIGHT}[{timestamp}] Starting tunnel check. Press Ctrl+C to exit.{Style.RESET_ALL}')
    main()