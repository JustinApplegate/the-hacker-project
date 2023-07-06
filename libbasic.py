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
#  - vote - gets HPD from voting
#  - get_unused_pvp - gets the amount of unused PvP points
#
################################################################


### IMPORTS ###
import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import urllib.parse
import time


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
def get_page(page, method="GET", data="", headers={}):
    cookies = dict(PHPSESSID=dotenv_values(".env")["PHPSESSID"])

    if 'User-Agent' not in headers:
        headers['User-Agent'] = USERAGENT

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


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     Amount of HPD gained
# Description:
#     Gets free PvP points for voting on servers, then turns this into HPD.
#     Note - still needs work! Need to test on new days looking for errors, 
#     and catching free AP.
# 
#####
def vote():
    for i in range(1,21):
        page = get_page("index.php?action=view&_a="+str(i))

        # if haven't voted, get script text
        try:
            URLencoded = page.find_all("script")[0].get_text().strip()[16:-4]
        except:
            print("Already voted for number "+str(i))
            continue

        decoded = urllib.parse.unquote(URLencoded)
        reward_path = decoded.split("location.href = '")[1].split("'")[0]
        print(reward_path)

        time.sleep(5)

        reward_page = get_page(reward_path)
        if 'You have gained <font color="#FFCC00">10 PvP points</font> bonus!' in reward_page:
            print("Voted successfully!")
        elif 'You have already voted' in reward_page:
            print("Already voted for number "+str(i))
        else:
            print("There was an error getting the reward for number "+str(i))


    # turn PvP points into HPD
    points = get_unused_pvp()

    if points == 0:
        print("No PvP points to convert.")
        return 0

    page = get_page("index.php?action=pvp_board&a2=rew_store&sac=convert", method="POST", data=f"points={points}&sel_type=HPD", headers={"Content-Type": "application/x-www-form-urlencoded"})

    if 'PvP point(s) successfully converted into' in str(page):
        HPD = int(str(page).split('successfully converted into <span class="p">')[1].split(' HPD')[0])
        return HPD
    else:
        print("There was an error converting PvP points into HPD.")
        return 0


#####
# 
# Parameter(s):
#     none
# Return value(s):
#     Number of unused PvP points.
# Description:
#     Returns the number of unused PvP points.
# 
#####
def get_unused_pvp():
    page = get_page('index.php?action=pvp_board&a2=rew_store')

    points = int(str(page).split('You have <span class="p">')[1].split('</span>')[0])

    return points



# used for testing functions above
if __name__ == "__main__":
    ""
