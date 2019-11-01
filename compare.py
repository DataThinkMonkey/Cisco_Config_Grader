#!/usr/bin/env python3
# Compare baseline Cisco config with Student config

import diffios
import requests
import os
from pprint import pprint

cisco = input("Which Cisco class you are taking?\n\n1. INFO 1200 - Cisco 1\n2. INFO 1201 - Cisco 2\n3. INFO 2220 - Cisco 3\n4. INFO 2230 - Cisco 4\nEnter the number of the Cisco class you are taking: ")
lab = input("Enter the lab number (i.e. 2.3.1.5 or final): ")
device = input("Enter the device you would like to compare (i.e R1, R2, S1, etc): ")


baseline = (device + "-key")
compare = (device + "-confg")
ignore = "ignore.txt"

# download the key file
url_key = 'http://192.168.1.10/compare/' + cisco + '/' + lab + '/' + baseline 
get_key = requests.get(url_key)
save_key = open(baseline, 'wb').write(get_key.content)

# download the ignore file
url_ignore = 'http://localhost/compare/' + cisco + '/' + lab + '/' +  ignore
get_ignore = requests.get(url_ignore)
save_ignore = open(ignore, 'wb').write(get_ignore.content)


# Compare
diff = diffios.Compare(baseline, compare, ignore)
# Print
#print("BELOW IS A COMPARISON OF YOUR CONFIG FILE.")
#print("")
print("\n**** YOU ARE MISSING THE FOLLOWING FROM YOUR CONFIG ****\n")
print(diff.pprint_missing())

# ******Other print options****************************
#print(diff.delta())
#print("\n-----THIS IS PPRINT FORMAT-----\n" )
#pprint(diff.additional())
#print("\n-----WHAT IS DOES NOT MATCH (BASELINE)-----\n" )
#print(diff.pprint_additional())

# Delete downloaded files
os.remove(baseline)
os.remove(ignore)
