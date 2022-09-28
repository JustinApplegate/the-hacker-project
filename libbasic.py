################################################################
#
# All functions here are helpers that implement basic
# functionality for the game.
# 
# Functions:
#  - get_page - returns the HTML text of a page
#  - login - logs in to the game
#  - get_money - gets the amount of HPD owned
#  - get_AP - gets the number of available Action Points
#
################################################################


### IMPORTS ###
import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup


### CONSTANTS ###
BASEURL = "http://www.hacker-project.com/"
USERAGENT = "Legoclones"
FAKE_LOG = "admin logged in from [17.144.148.127]"


#####
# 
# Parameter(s):
#     page - local path for the URL [example: 'index.php?action=gate']
#     method (optional) - HTTP method, default value is 'GET'
#     data (optional) - values to be passed through the request, default value is {}
# Return value(s):
#     Soup object for BeautifulSoup parser
#     Status code (if error thrown)
# Description:
#     Given a specific page, this will use the BASEURL
#     constant and PHPSESSID local environmental variable
#     and return the HTML text to be parsed with BeautifulSoup.
#     The user is automatically logged in if logged out.
# 
#####
def get_page(page, method="GET", data="", headers={'User-Agent': USERAGENT}):
    cookies = dict(PHPSESSID=dotenv_values(".env")["PHPSESSID"])

    while True:
        # get response
        response = requests.request(method, BASEURL+str(page), cookies=cookies, data=data, headers=headers)

        # if error thrown
        if str(response.status_code)[:1] != "2":
            print("Non-OK status code returned - "+str(response.status_code))
            return -1

        # if not logged in
        elif ("login or create a new account" in response.text) or ("Accept terms and conditions?" in response.text):
            print("Logging in again...")
            login()

        # if OK
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     none
# Description:
#     This uses credentials stored .env to login again. A new
#     session cookie isn't required if an old session cookie
#     is sent in the request.
# 
#####
def login():
    username = dotenv_values(".env")["HP_USERNAME"]
    password = dotenv_values(".env")["HP_PASS"]

    get_page(
        "index.php",
        method="POST",
        data="user="+username+"&pwd="+password+"&submit=Login&action=login",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': USERAGENT,
        })


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     Amount of HPD owned as a string
# Description:
#     Retrieves the current amount of HPD owned.
# 
#####
def get_money():
    page = get_page("index.php")

    return page.find_all("table")[2].find_all("tr")[3].find_all("span")[0].get_text()[:-4]


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     Number of actions points as an integer
# Description:
#     Retrieves the current number of available
#     Actions Points.
# 
#####
def get_AP():
    page = get_page("index.php")

    return int(page.find_all("table")[2].find_all("tr")[4].find_all("span")[0].get_text()[:-3])


# used for testing functions above
if __name__ == "__main__":
    ""
