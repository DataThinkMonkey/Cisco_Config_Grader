# Cisco_Config_Grader
Compares local Cisco config files with remote key config file on a web server.
Written in python using the diffios, requests and os modules. 

# Setup
I hope to automate this process soon. 
1. Install Web server
2. In root directory of web server create a directory called "compare"
3. Inside the compare directory create 4 directories name "1" "2" "3" and "4" to represent the 4 CCNA courses.
4. Insde each numbered directory (1-4) create a directory for each Lab number, for example 1.2.3.5 
5. Copy the answer key files to the corresponding lab number directory. 
6. Open compare.py and modify url to IP if using remote web server. Default is localhost. 

# Install python modules
diffios
beautifulsoup


