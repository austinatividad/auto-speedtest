# auto-speedtest
 automatic speedtest using speedtest-cli
 
 this will create a scheduled task that runs auto_speed_test.py based on a `wifi.py` file. This script will only work on SAVED NETWORKS (a network must have been connected successfully manually at least once).

 ## `wifi.py` format
 ```python
 wifi_list = [
    'SSID1',
    'SSID2',
    .
    .
    .
]
 ```

 records the datetime, download speed, upload speed, ping, and SSID to the .csv file `speedtest_logs.csv` in the `Logs` folder

# logs
Logs are saved in `C:\Users\[User]\Documents\AutoSpeedTest\Logs`

# setup
1. run `setup.bat`, or:
    - open cmd in the project directory
    - paste the code below:
    ``` bash
    setup.bat
    ```
    
2. copy-paste Python directory 

