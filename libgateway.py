################################################################
#
# Description
#
################################################################


### IMPORTS ###
# global imports
import urllib.parse
import hashlib

# local imports
from libbasic import get_page


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
#     returned.
# 
#####
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
    else:
        return 0


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


# used for testing functions above
if __name__ == "__main__":
    connect("18.227.145.108")