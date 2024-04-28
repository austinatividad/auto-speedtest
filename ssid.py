import subprocess

def get_ssid():
    wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
    wifi = wifi.decode('utf-8')
    wifi = wifi.split('\n')
    for line in wifi:
        if "SSID" in line:
            return line.split(":")[1].strip()
    return False