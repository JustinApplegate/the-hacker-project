################################################################
#
# Description
#
################################################################


### IMPORTS ###
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
#     remote addresses.
# 
#####
def get_logs(IP="localhost"):
    logs = []
    counter = 0

    # loops through all pages of logs
    while True:
        # local logs or logs for a remote address
        URL = "index.php?action=gate&a2=logs&_o="+str(counter*10)

        # connect to remote host if not already
        if IP != "localhost":
            if IP != get_current_connection():
                "connect here"
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


# needs to contact IP db each time
def connect(IP):
    URL = "index.php?action=gate&a2=connect&con_ip="+IP+"&OcIGLyvrNk=0a84518ad58669999e83e657184fce82"
    resp = get_page(URL)


# used for testing functions above
if __name__ == "__main__":
    print(get_logs("176.126.190.21"))