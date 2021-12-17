################################################################
#
# Description
#
################################################################


### IMPORTS ###
from libbasic import get_page
from libdatabase import get_IP_attributes, IPDB_to_localDB


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
#     -3 if the connection was unsuccessful after database refresh
#     -2 if attempting to connect to self
#     -1 if connectParam couldn't be retrieved from database
#     0 if connection was successful
# Description:
#     Connects to the IP address specified in the parameter. If
#     the connection threw no errors but was unsuccessful, the
#     database is refreshed for that IP address (most likely bad
#     connectParam) and it is attempted again.
# 
#####
def connect(IP):
    # ensure not trying to connect to self
    if IP == get_my_IP():
        print("Cannot connect to self")
        return -2

    # try connecting
    return_code = connect_help(IP)

    # if page was requested but no connection made, database needs to be updated
    if return_code == -2:
        print("Refreshing connectParam and connecting again...")
        IPDB_to_localDB(IP)
        
        # try connecting again
        if connect_help(IP) == -2:
            print("Connection unsuccessful")
            return -3
    
    # if error was thrown while connecting
    elif return_code == -1:
        print("ConnectParam could not be retrieved from database")
        return -1

    # all good
    else:
        return 0


#####
# 
# Parameter(s):
#     IP - IP address of server to connect to
# Return value(s):
#     -2 if the connection was unsuccessful
#     -1 if connectParam couldn't be retrieved from database
#     0 if connection was successful
# Description:
#     Helper function for the connect() function. Retrieves the
#     connectParam from the database, sends the HTTP request, and
#     checks to see if the connection succeeded.
# 
#####
def connect_help(IP):
    # get connect parameter
    connectParam = get_IP_attributes(IP, ["connectParam"])

    # check for error
    if connectParam == -1:
        print("Connect failed - connectParam not received")
        return -1

    # connect
    URL = "index.php?action=gate&a2=connect&con_ip="+IP+"&"+connectParam[0]
    page = get_page(URL)

    # ensure connection was successful
    if get_current_connection() != IP:
        return -2
    else:
        return 0


# used for testing functions above
if __name__ == "__main__":
    ""