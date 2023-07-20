################################################################
#
# All functions here relate to actions that can be performed
# with the gateway. 
# 
# Functions:
#  - get_logs - gets all the logs for an IP
#  - get_current_connection - gets the IP of the current
#      connection
#  - get_my_IP - gets the IP of the current server
#  - connect - connects to an IP
#  - get_connection_param - helper function for connect
#  - attempt_crack_password - attempts to crack the password
#  - get_running_software - gets the software running on an IP
#  - update_internal_info - updates the internal info of an IP
#
################################################################


### IMPORTS ###
# global imports
import urllib.parse
import hashlib
import json
import datetime

# local imports
from libbasic import get_page
from libdatabase import get_IP_attributes, set_IP_attributes


#####
# 
# Parameter(s):
#     IP (optional) - IP address to get logs of, default value is 'localhost'
# Return value(s):
#     Array of log objects in the format:
#     {
#        'id': 000000,
#        'text': 'This is the log',
#        'time': '01-Jan-2021 00:00:00'
#     }
# Description:
#     Returns the log IDs, text, and timestamps for local or
#     remote addresses. If the server isn't already connected
#     to the remote host, a blank array is returned. This must
#     be done before requesting logs.
# 
#####
def get_logs(IP="localhost"):
    logs = []
    counter = 0

    # loops through all pages of logs
    while True:
        # local logs or logs for a remote address
        URL = "index.php?action=gate&a2=logs&_o="+str(counter*10)

        # change settings for remote host
        if IP != "localhost":
            if IP != get_current_connection():
                print("Not connected to remote host")
                return []
            URL += "&rem=1"

        # get the page and start parsing
        page = get_page(URL)

        trs = page.find_all("fieldset")[0].find_all("table")[1].find_all("tr")

        # if there are no logs on the page, finish and return log list
        if len(trs) == 4:
            break
        
        # loop through all logs and append to array
        for i in range(len(trs)):
            if (i % 3 == 0) and (i != 0) and (i != len(trs)-1):
                tr = trs[i]
                form = tr.find_all("form")[0]
                
                obj = {
                    'id': int(form.find_all("input")[0]['value']),
                    'text': form.find_all("textarea")[0].get_text(),
                    'time': tr.find_all(class_="dbg")[1].get_text()
                }
                logs.append(obj)

        # increase counter to see new page of logs
        counter += 1

    return logs


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     IP address of remote machine currently connected to, or 'N/C'
# Description:
#     Returns the IP address of connected remote machine
# 
#####
def get_current_connection():
    URL = "index.php?action=gate"

    # get the page and start parsing
    page = get_page(URL)

    IP = page.find_all(class_="def")[3].find(class_="green").get_text()

    return IP


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     IP address of current user server
# Description:
#     Returns the IP address of the server that the user
#     is currently logged into.
# 
#####
def get_my_IP():
    URL = "index.php?action=gate"

    # get the page and start parsing
    page = get_page(URL)

    IP = page.find_all(class_="def")[1].find(class_="green").get_text()

    return IP


#####
# 
# Parameter(s):
#     IP - IP address of server to connect to
# Return value(s):
#     -2 if attempting to connect to self
#     -1 if connection was unsuccessful
#     0 if connection was successful
# Description:
#     Connects to the IP address specified in the parameter. If an
#     attempt was made to connect to oneself, an error code is
#     returned. If the connection was successful, then the local 
#     database is updated with internal information.
# 
#####

# wipe logs & update info on previously-connected IP before actually connecting
def connect(IP):
    # ensure not trying to connect to self
    if IP == get_my_IP():
        print("Cannot connect to self")
        return -2

    # get connect parameter
    connectParam = get_connection_param(IP)

    # connect
    URL = "index.php?action=gate&a2=connect&con_ip="+IP+"&"+connectParam
    get_page(URL)

    # ensure connection was successful
    if get_current_connection() != IP:
        print("Could not connect to IP")
        return -1
    
    # update remote & local information in local db
    update_internal_info(IP)
    update_internal_info()


#####
# 
# Parameter(s):
#     IP - IP address of server to connect to
# Return value(s):
#     URL-encoded GET parameter needed to connect to an IP
# Description:
#     This extracts the URL-encoded JavaScript from the connect
#     page, parses it, extracts the randomly-generated beginning
#     and end values, and calculates the MD5 hash of beginning+IP+end.
#     This MD5 hash is returned in the form 'beginning=md5_hash' to
#     be used to connect to an IP.
# 
#####
def get_connection_param(IP):
    URL = "index.php?action=gate&a2=connect"
    
    # get page
    page = get_page(URL)

    # extract beginning and end
    URLencoded = page.find_all("script")[1].get_text().strip()[16:-4]
    beginning = urllib.parse.unquote(URLencoded[777:810])
    end = urllib.parse.unquote(URLencoded[894:933])

    # hash value
    string_to_hash = beginning+IP+end
    hash_value = hashlib.md5(string_to_hash.encode()).hexdigest()

    # return param
    return beginning+"="+hash_value


# check if admin and already connected
def attempt_crack_password(IP):
    if not get_IP_attributes(IP, ['admin']):
        print("Already admin")
        return -1
    
    if get_current_connection() != IP:
        print("Not connected to IP")
        return -2
    
    # need to know running software before crack


#####
# 
# Parameter(s):
#     IP (optional) - the IP address of the server to extract software info
# Return value(s):
#     Returns an array of objects in the format:
#     {
#         'id': 000000,
#         'type': 'Log UnDeleter',
#         'name': 'Basic Log UnDeleter',
#         'version': '0.1',
#         'CPU': 50,
#         'memory': 3000,
#         'bandwidth': 0
#     }
# Description:
#     Returns a list of all software running on the 
#     given IP address.
# 
#####
def get_running_software(IP="localhost"):
    path = "index.php?action=gate&a2=run"

    # connect to remote host if not already connected
    if IP != "localhost":
        if IP != get_current_connection():
            connect(IP)
        path += "&rem=1"

    page = get_page(path)

    # get script tags
    software = []
    scripts = page.findAll("script")
    for script in scripts:
        if str(script.text)[:14] == 'document.write':
            # decode tags with software info
            new_text = urllib.parse.unquote(script.text[25:-4])

            id = int(new_text.split('snl">')[1].split("<")[0])
            type = new_text.split('p1">')[1].split("<")[0]
            name = new_text.split('sm">')[1].split("<")[0]
            version = new_text.split('sm2">')[1].split("<")[0]
            cpu = int(float(new_text.split('sm">')[2].split("<")[0]))
            memory = int(float(new_text.split('sm">')[3].split("<")[0]))
            bandwidth = int(float(new_text.split('sm">')[4].split("<")[0]))

            software.append({
                'id': id,
                'type': type,
                'name': name,
                'version': version,
                'CPU': cpu,
                'memory': memory,
                'bandwidth': bandwidth
            })

    return software


#####
# 
# Parameter(s):
#     IP (optional) - the IP address of the server to update internal info
# Return value(s):
#     None
# Description:
#     The IP specified will have information only available 
#     when connected (such as running software, files, etc.) 
#     updated in the local database.
# 
#####
def get_hardware(IP="localhost"):
    path = "index.php?action=gate&a2=run"

    # connect to remote host if not already connected
    if IP != "localhost":
        if IP != get_current_connection():
            connect(IP)
        path += "&rem=1"

    page = get_page(path)


#####
# 
# Parameter(s):
#     IP (optional) - the IP address of the server to update internal info
# Return value(s):
#     None
# Description:
#     The IP specified will have information only available 
#     when connected (such as running software, files, etc.) 
#     updated in the local database.
# 
#####
def update_internal_info(IP="localhost"):
    # CPU

    # memory

    # bandwidth

    # logs

    # running processes
    running = json.dumps(get_running_software(IP))

    # files

    # last update
    last_update = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # update
    if IP == "localhost":
        IP = get_my_IP()
        
    set_IP_attributes(IP, 
        ['running', 'lastupdated'], 
        [running, last_update]
    )

    return


# used for testing functions above
if __name__ == "__main__":
    ""