################################################################
#
# Description
#
################################################################


### IMPORTS ###
# global imports
import sqlite3

# local imports
from libbasic import get_page


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     Sqlite3 connection object that can be used for SQL queries
# Description:
#     Creates a connection to the sqlite3 database, local.db
#     and returns a connection object to allow other functions
#     to execute queries. If the servers table does not exist,
#     then it will be automatically created.
# 
#####
def connect_to_db():
    # initialize database
    conn = sqlite3.connect('local.db', isolation_level=None)
    print("Connected to database")

    # create table if it doesn't exist
    conn.execute('CREATE TABLE if not exists servers (ipAddress TEXT PRIMARY KEY, name TEXT, type TEXT, connectParam TEXT, page INTEGER, admin BOOLEAN, minimum_protect TEXT, owned BOOLEAN, running TEXT, files TEXT, cpu TEXT, memory TEXT, bandwidth TEXT, lastlog TEXT)')

    return conn


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     none
# Description:
#     Extracts all the information from the local IP database and
#     inserts it into the local Sqlite3 file, local.db.
# 
#####
def IPDB_to_localDB():
    # connect to DB
    conn = connect_to_db()
    cursor = conn.cursor()

    # import information
    print("Importing information from IP DB to local DB...")

    # loops through Public, Private, and Secret servers to determine type
    exts = ['pub', 'priv', 'sec']
    for ext in exts:

        # determine type
        if ext == "pub":
            server_type = "Public"
        elif ext == "priv":
            server_type = "Private"
        else:
            server_type = "Secret"
        
        # loops through all pages
        counter = 0
        moreIPs = True

        while moreIPs:
            page = get_page("index.php?action=ip_db&a2="+ext+"&_o="+str(counter*20))

            # extra tables are added if connected
            if "Remote host web service" in page.text:
                trs = page.find_all("table")[16].find_all("tr")[::2][1:][:-1]
            else:
                trs = page.find_all("table")[9].find_all("table")[3].find_all("tr")[::2][1:][:-1]

            # no IPs on this page
            if len(trs) == 0:
                moreIPs = False

            # loop through elements and extract information
            for tr in trs:
                # get information
                connectParam = tr.find_all("td")[0].find_all("td")[0].find_all("a")[0]["href"].split("&")[3]
                ipAddress = tr.find_all("td")[0].find_all("td")[0].find_all("a")[0]["href"].split("&")[2][7:]
                name = ' '.join(tr.find_all("td")[5].get_text().split())
                admin = (tr.find_all("td")[6].get_text() == "Yes")
                owned = (tr.find_all("td")[7].get_text() == "Gateway")

                # if IP exists already...
                if len(cursor.execute("SELECT name FROM servers WHERE ipAddress = ?", (ipAddress,)).fetchall()) != 0:
                    # update information
                    cursor.execute("UPDATE servers SET name = ?, type = ?, connectParam = ?, page = ?, admin = ?, owned = ? WHERE ipAddress = ?", (name, server_type, connectParam, counter, admin, owned, ipAddress))
                else:
                    # add new row to database
                    cursor.execute("INSERT INTO servers VALUES (?, ?, ?, ?, ?, ?, '', ?, '', '', '', '', '', '')", (ipAddress, name, server_type, connectParam, counter, admin, owned))

            # increase counter to see if more logs on next page
            counter += 1

    print("Completed")
    conn.close()


# used for testing functions above
if __name__ == "__main__":
    IPDB_to_localDB()