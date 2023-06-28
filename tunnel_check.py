import os
import socks
import time
from datetime import datetime
import subprocess
from colorama import Fore, Style

def is_tunnel_working(port=8080):
    s = socks.socksocket() # Same API as socket.socket in the standard lib
    try: 
        s.set_proxy(socks.SOCKS5, "localhost",port)
        s.settimeout(2.0)

        s.connect(("google.com", 80))

        request = """GET / HTTP/1.1
        Host: google.com
        User-Agent: MyClient/1.0

        """
        # convert to bytes for sending over network
        request_encoded = request.encode()

        s.sendall(request_encoded)

        # now receive the response
        buffer_size = 4096
        response = s.recv(buffer_size)

        s.close()
        return True
    except Exception as e:
        # print(e)
        return False

def kill_tunnel(port):
    timestamp = datetime.now().strftime('%H:%M:%S')
    cmd = f"ps aux | grep 'ssh -D {port}' | grep -v grep | awk '{{print $2}}'"
    ssh_pid = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

    if ssh_pid:
        subprocess.run(f'kill {ssh_pid}', shell=True)
        print(f'{Fore.YELLOW}[{timestamp}] Tunnel killed (pid: {ssh_pid}){Style.RESET_ALL}')

def create_tunnel(port, ssh_user, ssh_host):
    cmd = f'ssh -D {port} -f -C -q -N {ssh_user}@{ssh_host} -o ServerAliveInterval=30 -o ServerAliveCountMax=1 -o ExitOnForwardFailure=True'
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    try:
        last_ssid_check = False
        port = 8080
        ssh_user = 'ubuntu'
        ssh_host = '144.22.144.218'
        is_working = False
        interval = 5  # Seconds

        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            if not is_tunnel_working(port):
                is_working = False
                kill_tunnel(port)
                print(f'{Fore.YELLOW}[{timestamp}] Tunnel not working. Creating a new one...{Style.RESET_ALL}')
                if create_tunnel(port, ssh_user, ssh_host):
                    print(f'{Fore.GREEN}[{timestamp}] Tunnel created on port {port} with {ssh_user}@{ssh_host}{Style.RESET_ALL}')
                    change_proxy_location()
                    print(f'{Fore.GREEN}[{timestamp}] {Style.BRIGHT}Tunnel is working.({interval}s){Style.RESET_ALL}', end='\r')
                else:
                    #change_location('Automatic')
                    print(f'{Fore.RED}[{timestamp}] Failed to create tunnel.{Style.RESET_ALL}')
            else:
                print(f'{Fore.GREEN}[{timestamp}] {Style.BRIGHT}Tunnel is working.({interval}s){Style.RESET_ALL}', end='\r')
                is_working = True

            time.sleep(interval)  # Wait for X seconds before checking again
    except KeyboardInterrupt:
        timestamp = datetime.now().strftime('%H:%M:%S')
        print('')
        kill_tunnel(port)
        change_automatic_location()
        print(f'[{timestamp}] {Style.BRIGHT}Bye!{Style.RESET_ALL}')

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

def change_proxy_location():
    timestamp = datetime.now().strftime('%H:%M:%S')
    changed = change_location('Proxy')
    if changed:
        print(f'{Fore.GREEN}[{timestamp}] Location set to Proxy{Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}[{timestamp}] Failed to change to Proxy location{Style.RESET_ALL}')

def change_automatic_location():
    timestamp = datetime.now().strftime('%H:%M:%S')
    changed = change_location('Automatic')
    if changed:
        print(f'{Fore.GREEN}[{timestamp}] Location set to Automatic{Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}[{timestamp}] Failed to change to Automatic location{Style.RESET_ALL}')

if __name__ == '__main__':
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] {Style.BRIGHT}Starting tunnel check. Press Ctrl+C to exit.{Style.RESET_ALL}')
    main()