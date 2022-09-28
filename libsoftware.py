################################################################
#
# All functions here relate to software (specifically malware)
# that is or can be installed on servers.
# 
# Functions:
#  - 
#
################################################################


### IMPORTS ###
import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup


#####
# 
# Parameter(s):
#     None
# Return value(s):
#     Returns an array of objects in the format:
#     {
#         'id': 000000,
#         'ip': '123.123.123.123',
#         'type': 'Adware Spam Daemon',
#         'version': '0.1',
#         'runhours': 12.34
#     }
# Description:
#     Returns a list of all malware installed on 
#     servers in the games, along with relevant metadata.
# 
#####
def get_activated_software():
    return ""


#####
# 
# Parameter(s):
#     id - software id to collect
# Return value(s):
#     Returns the amount of HPD collected from the software
# Description:
#     Money is collected from the software specified and the amount is returned. 
# 
#####
def collect(id):
    return ""

"""
Destroy
Leech IP
Install software
"""