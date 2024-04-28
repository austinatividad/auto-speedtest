# -- Internet Speed Test -- 
import speedtest 
import time
import csv
import os
from plyer import notification
from ssid import get_ssid
from wifi import wifi_list
import subprocess

# Obtain initial SSID
init_ssid = get_ssid()
if init_ssid == False:
    notification.notify(
    title = "Internet Speed Test",
    message = f"Please Connect to a Network",
    timeout = 2
    )
    exit()

for x in range(len(wifi_list)):
    ssid = wifi_list[x]
    # Connect to SSID
    try:
        print(f"Connecting to {ssid}...")
        subprocess.run(['netsh', 'wlan', 'disconnect'])
        # wait for connection
        timeout = 10
        while get_ssid() != ssid and timeout > 0:
            subprocess.run(['netsh', 'wlan', 'connect', ssid])
            print(f'Connecting... ({timeout})\r', end='')
            time.sleep(1)
            timeout -= 1
            
        if timeout == 0:
            raise Exception("Connection Timeout")
    except Exception as e:
        # Failure Notification
        notification.notify(
            title = "Internet Speed Test",
            message = f"Failed to Connect to {ssid}. Please check your wifi credentials.\n Error: {e}",
            timeout = 2
        )
        continue
    
    # Start Notification
    notification.notify(
        title = "Internet Speed Test",
        message = f"Starting Scheduled Speed Test on {ssid}...",
        timeout = 2
    )
    
    # Speedtest module
    try:
        print("Running Speed Test...")
        st = speedtest.Speedtest()
        download_speed = st.download()
        upload_speed = st.upload()
        servernames =[]   
        st.get_servers(servernames)
        print(f"Download Speed: {download_speed / 1024 / 1024:.2f} Mbps")   
    except Exception as e:
        # Failure Notification
        
        notification.notify(
            title = "Internet Speed Test",
            message = f"Speed Test Failed. Please check your internet connection.\n Error: {e}",
            timeout = 2
        )
        continue
    
    # Write to CSV file in /Logs/ directory
    
    try:
        directory = f"C:/Users/{os.getlogin()}/Documents/AutoSpeedTest/Logs/speedtest_logs.csv"
        
        #tests first if the directory exists, if not create the directory and the file
        if not os.path.exists(f"C:/Users/{os.getlogin()}/Documents/AutoSpeedTest/Logs"):
            os.makedirs(f"C:/Users/{os.getlogin()}/Documents/AutoSpeedTest/Logs")
            with open(directory, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Download Speed", "Upload Speed", "Ping", "SSID"])

        with open(directory, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), f"{download_speed / 1024 / 1024:.2f} Mbps", f"{upload_speed / 1024 / 1024:.2f} Mbps", f"{st.results.ping} ms", ssid])
    except Exception as e:
        # Failure Notification
        
        notification.notify(
            title = "Internet Speed Test",
            message = f"Failed to save results.\nError: {e}",
            timeout = 2
        )
        continue
    
    # Success Notification 
    
    notification.notify(
        title = "Internet Speed Test",
        message = f"Speed Test Results: \nDownload Speed: {download_speed / 1024 / 1024:.2f} Mbps \nUpload Speed: {upload_speed / 1024 / 1024:.2f} Mbps \nPing: {st.results.ping} ms\n Results saved to Logs/speedtest_logs.csv",
        timeout = 2
    )

# Revert to initial SSID
try:
    print(f"Reverting to {init_ssid}...")
    subprocess.run(['netsh', 'wlan', 'disconnect'])
    subprocess.run(['netsh', 'wlan', 'connect', init_ssid])
    while get_ssid() != init_ssid:
        time.sleep(1)
except:
    # Failure Notification
    notification.notify(
        title = "Internet Speed Test",
        message = f"Failed to Revert to {init_ssid}. Please check your wifi credentials.",
        timeout = 2
    )
    exit()