#!/usr/bin/env python3
# Compare baseline Cisco config with Student config
#
# Jared Bernard
#
## To-do
# Loop prompt for device within the same lab.
# Check for config files and name properly.

import diffios
import requests
from os import system, name
import os 
from pprint import pprint
# import sleep to show output for some time period
from time import sleep

ignore = "ignore.txt"
url = 'http://localhost/compare/'

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(os.name is 'posix')
    else:
        _ = system('clear')

def get_key():
    # download the key file
    url_key = url_lab + '/' + baseline 
    get_key = requests.get(url_key)
    save_key = open(baseline, 'wb').write(get_key.content)

def get_ignore():
    # download the ignore file
    url_ignore = url_lab + '/' +  ignore
    get_ignore = requests.get(url_ignore)
    save_ignore = open(ignore, 'wb').write(get_ignore.content)

def report():
    # Compare
    diff = diffios.Compare(baseline, compare, ignore)
    # Print
    print("\n**** YOU ARE MISSING THE FOLLOWING FROM YOUR CONFIG ****\n")
    print(diff.pprint_missing())

    print("\n~~~~~~~~~~~~~ COMPARISON ~~~~~~~~~~~~~~~~\n")
    print("EXPLANATION:")
    print("Lines beginning with a dash - Settings missing from your config.")
    print("Lines beginning with a plus + Settings in your config, not found in the key.\n")
    print(diff.delta())

def cleanup():
    # Delete downloaded files
    os.remove(baseline)
    os.remove(ignore)

clear()
print("""
************ Cisco Lab Auto Grader **************""")
#time.sleep(1)
print()

cisco = input("""
   Which Cisco class you are taking?

   1. INFO 1200 - Cisco 1
   2. INFO 1201 - Cisco 2
   3. INFO 2220 - Cisco 3
   4. INFO 2230 - Cisco 4
                    
   Enter the number of the Cisco class you are taking: """)

if cisco == "1" or cisco == "2" or cisco == "3" or cisco == "4":
   url_class = url + '/' + cisco 
else:
    # clear the screen 
    clear() 
    print("""
You must select either 1,2,3 or 4. Please try again.""")
    print()

lab = input("""
  Enter the lab number (i.e. 2.3.1.5 or final): """)
url_lab = url_class + '/' + lab 

device = input("""
  Enter the device you would like to compare (i.e R1, R2, S1, etc): """)
baseline = (device + "-key")
compare = (device + "-confg")


get_key()
get_ignore()
clear()
report()
cleanup()
print()


# ******Other print options****************************
#print("\n-----THIS IS PPRINT FORMAT-----\n" )
#pprint(diff.additional())
#print("\n-----WHAT IS DOES NOT MATCH (BASELINE)-----\n" )
#print(diff.pprint_additional())

