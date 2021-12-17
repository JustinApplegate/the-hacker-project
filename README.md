# The Hacker Project Automation
This project was started to automate [The Hacker Project](http://www.hacker-project.com). In an attempt to decrease boring, manual, and repetitive actions, I have written Python scripts that will perform these actions simply by calling a function. As of this moment, these scripts only perform basic reconnaissance and cracking. It only has the ability to connect to IPs, read logs, crack newly found IPs, and scour them for logs. This will continue until all IPs have been scraped or cannot be cracked.

## Layout
Each of the files that start with `lib` are custom library files meant to be imported in other files. `main.py` is the main script that utilizes the functions defined in the libraries to perform the desired operation.

### `libbasic.py`
This Python library defines constants used across the libraries and core functions, such as retrieving pages and logging in. 

**Constants**
- `BASEURL` - the base url for The Hacker Project
- `USERAGENT` - the custom User Agent injected into all HTTP requests
- `FAKE_LOG` - whenever a log is created on any remote host, it is replaced with this log entry instead

**Functions**
- `get_page` - returns a BeautifulSoup object with the request page and parameters
- `login` - logs a user in
- `get_money` - retrieves current HPD
- `get_AP` - retrieves current Action Points

### `libdatabase.py`
This Python library is used to interface with the `local.db` SQLite file that stores all the information necessary. SQLite was chosen because it's easy to interface with and is stored in a file instead of a running service.

**Functions**
- `connect_to_db` - connects to the `local.db` database file
- `IPDB_to_localDB` - extracts information from the local IP database and updates the `local.db` file with it
- `get_IP_attributes` - returns information about a specific IP from the `local.db` file for other functions to use
- `get_IP_list` - returns a list of all the IPs in `local.db`

### `libgateway.py`
This Python library performs all gateway-related activities, such as retrieving logs and connecting to IPs.

**Functions**
- `get_logs` - gets all the logs from a remote or local IP address
- `get_current_connection` - returns the remote IP address currently connected to
- `get_my_IP` - returns the IP address of local server
- `connect` - connects to a specified remote address

### `libactions.py`
This Python library contains many of the higher-level operations. Instead of performing simple tasks like connecting or retrieving logs, these functions combine many of those in a desired way to perform log harvesting, cracking, and more.

**Functions**
- `process_new_IP` - when a new IP address is discovered, basic information is retrieved and stored in `local.db`
- `process_IP_as_admin` - when a new IP address has been cracked and admin access is obtained, extensive information is retrieved and stored in `local.db`
- `process_all_IPs` - goes through all the IPs in the local database, updates information, and looks for new IPs

### `main.py`
This Python script has been created to implement the functions in `libactions.py` (or other imported libraries).