# The Hacker Project Automation
This project was started to provide APIs that can interface with the game through the Python `requests` library, lending itself to automation. In addition, a Flask webserver was designed to provide the customer with a nice graphical interface so all the automation can be programmed, then deployed with the click of a button. 


*Note - It only has the ability to connect to IPs, read logs, crack newly found IPs, and scour them for logs. This will continue until all IPs have been scraped or cannot be cracked.*

# Layout
## `libbasic.py`
This Python library defines constants and core functions for the game, such as retrieving pages and logging in. 

**Constants**
- `BASEURL` - the base url for The Hacker Project
- `USERAGENT` - the custom User Agent injected into all HTTP requests
- `FAKE_LOG` - whenever a log is created on any remote host, it is replaced with this log entry instead

**Functions**
- `get_page(page, method="GET", data="", headers={}) -> BeautifulSoup`
    - Description
        - Given a specific page, this function will use the `BASEURL` constant and `PHPSESSID` local environmental variable to request the endpoint, and returns the HTML text to be parsed with BeautifulSoup. The user is automatically logged in if logged out.
    - Parameters
        - `page` [str] - path and query string for the URL to request, without the leading slash (`/`)
            - Example - `'index.php?param1=param2'`
        - `method` [str] (optional) - HTTP method, default value is `'GET'`
            - Example - `'POST'`
        - `data` [str] (optional) - data to provided in the request body, default is `''`
            - Example - `'ip=1.1.1.1&con=rem'`
        - `headers` [dict] (optional) - dict of HTTP headers to include in the request. Note that the `User-Agent` header will be added if not specified. Default value is `{}`
            - Example - `{"Content-Type": "application/json"}`
    - Return value
        - `BeautifulSoup`



- `get_page` - returns a BeautifulSoup object with the request page and parameters
- `login` - logs a user in
- `get_money` - retrieves current HPD
- `get_AP` - retrieves current Action Points
- `vote` - gains free PvP points then transforms into HPD
- `get_unused_pvp` - retrieves unused PvP points

### `libdatabase.py`
This Python library is used to interface with the `local.db` SQLite file that stores all the information necessary. SQLite was chosen because it's easy to interface with and is stored in a file instead of a running service.

**Functions**
- `connect_to_db` - connects to the `local.db` database file
- `IPDB_to_localDB` - extracts information from the local IP database and updates the `local.db` file with it
- `get_IP_attributes` - returns information about a specific IP from the `local.db` file for other functions to use
- `set_IP_attributes` - sets columns to desired values for a specific IP, updating information
- `get_IP_list` - returns a list of all the IPs in `local.db`

### `libgateway.py`
This Python library performs all gateway-related activities, such as retrieving logs and connecting to IPs.

**Functions**
- `get_logs` - gets all the logs from a remote or local IP address
- `get_current_connection` - returns the remote IP address currently connected to
- `get_my_IP` - returns the IP address of local server
- `connect` - connects to a specified remote address and updates internal information both locally and remotely
- `attempt_crack_password` - attempts to crack the password of a remote server
- `get_running_software` - returns an array of objects containing information about each software running on a machine
- `update_internal_info` - updates information only available when connected to a machine, such as CPU, memory, running processes, and more

### `libactions.py`
This Python library contains many of the higher-level operations. Instead of performing simple tasks like connecting or retrieving logs, these functions combine many of those in a desired way to perform log harvesting, cracking, and more.

**Functions**
- `process_IP_basic` - basic, unprivileged information about an IP is retrieved and stored in `local.db`
- `process_IP_as_admin` - when admin access is obtained, extensive information is retrieved and stored in `local.db`
- `process_all_IPs` - goes through all the IPs in the local database, updates information, and looks for new IPs

## Flask Web Server
The Python script `server.py` contains a Flask webserver that is used as the main interface with the Python automation. It's split into 2 main parts - views, and API endpoints. 

Views are meant for a consumer to access, and use Jinja + Bootstrap to present a beautiful interface with buttons that do all the work. 

The API endpoints are meant to be accessed using `fetch()` from within the views, and communicate to the server to perform actions that interact with the game.

### Views
* `/`
* `/logs`
* `/static/<path>` - static support files

### API Endpoints
* `/api/sync_db` - syncs the local SQLite database with the game site, updating information stored in the IP database. This only includes basic information such as server type, name, and whether admin access is obtained.
* `/api/vote` - "votes" on all 20 sites to get 200 free PvP points, and then converts this to HPD.
* `/api/update` - updates server information that can only be obtained when connected to an IP. It updates both localhost and the remote connection