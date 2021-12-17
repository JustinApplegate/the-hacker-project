################################################################
#
# Description
#
################################################################


### IMPORTS ###
from libbasic import get_page
from libgateway import connect
from libdatabase import IPDB_to_localDB


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     List of all IP addresses in local.db
# Description:
#     Retrieves a list of all the IP addresses in the
#     database for mass scanning and reconnaissance.
# 
#####
def process_new_IP(IP):
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
    # extract IPs from logs
    ""


#
def process_IP_as_admin():
    ""


# 
def process_all_IPs():
    ""

# used for testing functions above
if __name__ == "__main__":
    process_new_IP("40.247.61.25")