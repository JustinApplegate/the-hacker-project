################################################################
#
# Description
#
################################################################


### IMPORTS ###
from libbasic import get_page
from libgateway import attempt_crack_password, connect
from libdatabase import IPDB_to_localDB, get_IP_attributes


#####
# 
# Parameter(s):
#     IP - the IP address of the server to process
#     try_crack (optional) - whether or not the script to should try to crack the server
#     process_admin (optional) - whether or not the script should process as admin
# Return value(s):
#     List of all IP addresses scraped from server
# Description:
#     This script takes the given IP and connects to it, adds
#     it to the IP database, updates all the information in
#     the local database, and depending on the settings given,
#     will try to crack the password and process as admin.
# 
#####
def process_IP_basic(IP, try_crack=True, process_admin=True):
    # connect to the new IP
    return_code = connect(IP)

    # throw error if connection failed
    if return_code == -1:
        print("Could not connect to IP "+IP)
        return []
    
    # ignore if trying to connect to self
    elif return_code == -2:
        return []

    # add to IP DB
    get_page("index.php?action=gate&a2=connect&a3=add_ip")

    # update info for specific IP
    IPDB_to_localDB(IP)

    # try cracking
    if try_crack:
        attempt_crack_password(IP)
    
    # process as admin (which leaves a log)
    if process_admin and get_IP_attributes(IP, ["admin"])[0]:
        return process_IP_admin(IP)

    # if not processing as admin
    return []


#
def process_IP_admin(IP):
    ""


# 
def process_all_IPs(try_crack=True, process_admin=True):
    # update the entire database
    # get list of all IP addresses
    # process each IP
    ""

# used for testing functions above
if __name__ == "__main__":
    ""