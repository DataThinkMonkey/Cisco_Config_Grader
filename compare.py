#!/usr/bin/env python3
# Compare baseline Cisco config with Student config
#
# Jared Bernard
#
## To-do
# Validate lab number 
# Compare with lab directories on server and if not there, return "Lab not found"
# Check for config files and name properly.

import diffios, requests, os, re, sys, urllib.request
from bs4 import BeautifulSoup 
from os import system, name
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
    print("\nYOUR REPORT FOR DEVICE: " + device )
    print("\n**** YOU ARE MISSING THE FOLLOWING FROM YOUR CONFIG ****\n")
    print(diff.pprint_missing())

#    print("\n~~~~~~~~~~~~~ COMPARISON ~~~~~~~~~~~~~~~~\n")
#    print("EXPLANATION:")
#    print("Lines beginning with a dash - Settings missing from your config.")
#    print("Lines beginning with a plus + Settings in your config, not found in the key.\n")
#    print(diff.delta())

def cleanup():
    # Delete downloaded files
    os.remove(baseline)
    os.remove(ignore)

clear()

######### BEGIN MENU CISCO LOOP ########
while True:
    print("""
    ************ Cisco Lab Auto Grader **************""")
    #time.sleep(1)
    print()
######## Get Cisco Class ##########
    cisco = input("""
       Which Cisco class you are taking?

       1. INFO 1200 - Cisco 1
       2. INFO 1201 - Cisco 2
       3. INFO 2220 - Cisco 3
       4. INFO 2230 - Cisco 4\n                        
       Enter the number of the Cisco class you are taking: """)
# Validate Cisco class choice.
    if cisco == "1" or cisco == "2" or cisco == "3" or cisco == "4":
# Build partial url with class         
       url_class = url + '/' + cisco
######## LAB #############
       clear() 
####### DISPLAY LABS AVAILABLE ##########
       # http get page
       r = requests.get(url_class)
       # parse the page
       soup = BeautifulSoup(r.content, 'html.parser')
       # Clean up unwanted <a href> links, mostly headers in the table
       header0 = soup.find(href='?C=S;O=A')
       header0.decompose()
       header1 = soup.find(href='?C=M;O=A')
       header1.decompose()
       header2 = soup.find(href='?C=D;O=A')
       header2.decompose()
       header3 = soup.find(href='?C=N;O=D')
       header3.decompose()
       header4 = soup.find(href='/compare/') # remove parent dir
       header4.decompose()
       header5 = soup.find(href='final/') # do not list dir with final key 
       header5.decompose()

       # find table, only a single table listing child directories
       tb = soup.find('table')
       # find only the <a> tags
       dir_links = tb.find_all('a')
       
       print("""
    ************ Available Labs for Cisco """ + cisco + """ ***********\n""" )
       # Loop through and list <a> tags with are the child dir
       for dirs in dir_links:
           #print(dirs.prettify()) # displays html in pretty format, for debugging
           folders = dirs.contents[0]
           # print and remove the trailing forward slash /
           print("""           """ + folders.replace('/', ''))
####### INPUT LAB ########
       lab = input("""
   Enter a lab number: """)
       url_lab = url_class + '/' + lab
       clear()
######## DEVICE ###########                
       while True:
           # http get page
           r_device = requests.get(url_lab)
           # parse the page
           soup = BeautifulSoup(r_device.content, 'html.parser') 

           # Clean up unwanted <a href> links, mostly headers in the table
           header0 = soup.find(href='?C=S;O=A')
           header0.decompose()
           header1 = soup.find(href='?C=M;O=A')
           header1.decompose()
           header2 = soup.find(href='?C=D;O=A')
           header2.decompose()
           header3 = soup.find(href='?C=N;O=D')
           header3.decompose()
           header4 = soup.find(href='/compare/' + cisco + '/') # remove parent dir
           header4.decompose()

           # find table, only a single table listing child directories
           tb_device = soup.find('table')
           # find only the <a> tags
           device_files = tb_device.find_all('a')
           print("""
    ************ Devices Used in Lab  """ + lab + """ ***********\n""" )

           # Loop through and list <a> tags with are the child dir
           for files in device_files:
               # print(dirs.prettify()) # displays html in pretty format, for debugging
               key_files = files.contents[0]
               # print and remove the trailing forward slash /
               print("""          """ + key_files.replace('-key', ''))

           device = input("""
Enter the device to compare (case sensitive) or quit: """)
#                   device_format = re.match('R|S\d\Z',device) #Need to work on only R or S with either 1, 2 or 3
           if device == "R1" or device == "R2" or device == "R3" or device == "S1" or device == "S2" or device == "S3":
             baseline = (device + "-key")
             compare = (device + "-confg")
             get_key()
             get_ignore()
             clear()
             report()
             cleanup()
             print()
           elif device == "quit":
              clear() 
              break
           else:
             print("\nTry Again. Make to enter a listed device using capital letters or 'quit' to return to the beginning.\n ")
           continue 
######## END CISCO CLASS IF ###########    
    else:
        clear()
        print("""
    You must select either 1,2,3 or 4. Please try again.""")
        print()


# ******Other print options****************************
#print("\n-----THIS IS PPRINT FORMAT-----\n" )
#pprint(diff.additional())
#print("\n-----WHAT IS DOES NOT MATCH (BASELINE)-----\n" )
#print(diff.pprint_additional())

