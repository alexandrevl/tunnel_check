import subprocess

def check_wifi():
    COMMAND = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep SSID | tail -1 | awk '{print $2}'"
    SSID = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (SSID == "88200Wireless-d"):
        return True
    else:
        return False

def bb_location():
    COMMAND = "networksetup -getcurrentlocation"
    LOCATION = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (LOCATION == "BB"):
        return True
    else: 
        return False

def change_location():
    COMMAND = "networksetup -switchtolocation BB"
    RESULT = subprocess.check_output(COMMAND,shell = True).decode("utf-8").strip()
    if (RESULT == "found it!"):
        return True
    else:
        return False    

def change_bb_location():
    bb_wireless = check_wifi()
    if bb_wireless:
        bb_location_settled = bb_location()
        if not bb_location_settled:
            changed = change_location()
            if changed:
                print("Changed to BB location")
            else:
                print("Failed to change to BB location")
        else:
            print("Already in BB location")
    else:
        print("Not connected to BB Wireless")
        
if __name__ == '__main__':
    change_bb_location()