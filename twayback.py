from operator import contains
import requests, re, os, argparse, sys, bs4, lxml, pathlib, time, aiohttp, asyncio, platform
from pathlib import Path
import simplejson as json
from tqdm import tqdm as tqdm
# this import needs to be named different since we've used up tqdm above
# used for progress bar on our async operations
from tqdm.asyncio import tqdm as asyncProgress
import colorama
from colorama import  Fore, Back, Style
colorama.init(autoreset=True)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests import Session
session = Session()
# for async
from aiohttp import ClientSession, TCPConnector
import asyncio

# checks the status of a given url
async def checkStatus(url, session: ClientSession, sem: asyncio.Semaphore):
    
    async with sem:
        async with session.get(url) as response:
            return response.real_url, response.status
        
    
# controls our async event loop
async def asyncStarter(url_list):
    # this will wrap our event loop and feed the the various urls to their async request function.
    status_list = []
    headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}
    
    # using a with statement seems to be working out better
    async with ClientSession(headers=headers) as session:
        # limit to 50 concurrent jobs
        sem = asyncio.Semaphore(50)
        # launch all the url checks concurrently as coroutines 
        status_list = await asyncProgress.gather(*(checkStatus(u, session, sem) for u in url_list))
    # return a list of the results    
    return status_list

# framework for future functions
def downloadHTML():
    pass

def takeScreenshots():
    pass

def downloadText():
    pass

def getStatuses():
    # will call one of the download functions above
    pass


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# parse out args passed in from command line
parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', required=True, default='')
parser.add_argument('-from','--fromdate', required=False, default='')
parser.add_argument('-to','--todate', required=False, default='')
args = vars(parser.parse_args())
username = args['username']
fromdate = args['fromdate']
todate = args['todate']
remove_list = ['-', '/']
fromdate = fromdate.translate({ord(x): None for x in remove_list})
todate = todate.translate({ord(x): None for x in remove_list})
account_url =f"https://twitter.com/{username}"
results = []
headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}

# Active, suspended, or doesn't exist?
account_response = requests.get(account_url, headers=headers, allow_redirects=False)
status_code = account_response.status_code
if status_code == 200:
    print(Back.GREEN + Fore.WHITE + f"Account is ACTIVE\n")
    time.sleep(1)
elif status_code == 302:
    print(Back.RED + Fore.WHITE + f"Account is SUSPENDED. This means all of {Back.WHITE + Fore.RED + username + Back.RED + Fore.WHITE}'s Tweets will be downloaded.\n")
    time.sleep(3)
else:
    print(Back.RED + Fore.WHITE + f"No one currently has this handle. Twayback will search for a history of this handle's Tweets.\n")
    time.sleep(4)

stuck = "(Don't worry, Twayback isn't stuck!"

print(f"Please wait. Twayback is searching far and wide for deleted tweets from {username}.\nDrink some delicious coffee while this gets done.\n\n{Back.MAGENTA + stuck + Fore.WHITE}\nDepending on the number of Tweets, this step might take several minutes.)\n")

print(f"Grabbing links for Tweets from the Wayback Machine...\n")

# list of deleted tweet urls
missing_tweet_list=[]
wayback_screenshot = []
# list of deleted tweet wayback machine urls
wayback_url_list = []

# build a url to take advantage of wayback machine cdx api
wayback_cdx_url = f"https://web.archive.org/cdx/search/cdx?url=twitter.com/{username}/status&matchType=prefix&filter=statuscode:200&mimetype:text/html&from={fromdate}&to={todate}"

# grab results of cdx query
cdx_page_text = requests.get(wayback_cdx_url).text

# Is Twitter handle excluded by the Wayback Machine?
blocklist = []
blocks = re.findall(r'Blocked', cdx_page_text)
for block in blocks:
    blocklist.append(f"{block}") 
    if any("Blocked" in s for s in blocklist):
        print(f"Sorry, no deleted Tweets can be retrieved for {username}.\nThis is because the Wayback Machine excludes Tweets for this handle.")
        exit()


r = re.compile(r"\b[0-9]{14}\b")
# pull out wayback id number cdx query results
wayback_id_list = r.findall(cdx_page_text)
# extract the twitter url from api call above
twitter_url_list = re.findall(r'https?://(?:www\.)?(?:mobile\.)?twitter\.com/(?:#!/)?\w+/status(?:es)?/\d+', cdx_page_text)


number_of_elements = len(wayback_id_list)
if number_of_elements >= 1000:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\nThat's a lot of Tweets! It's gonna take some time.\nTip: You can use -from and -to to narrow your search between two dates.")
else:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\n")

###############################################################################
# check twitter urls asyncronously and add the results to a list
# broken out in to functions
results_list = asyncio.run(asyncStarter(twitter_url_list))
 
#####################################################################################################

# extract just the urls that gave a 404 upon checking
for result in results_list:
    if result[1] == 404:
        missing_tweet_list.append(str(result[0]))

twitter_id_list = [] 
# extract just the numeric portion of twitter urls that gave a 404 above
for url in missing_tweet_list:
    regex = re.search(r"\b(\d{12,19})\b", url)
    if regex:
        twitter_id_list.append(regex.group())

# generate a tuple containing the wayback id and twitter url for just our missing tweets
wayback_id_twitter_url = [(x, y) for x, y in zip(wayback_id_list, twitter_url_list) if y in missing_tweet_list]
# generate list of full urls for use with wayback machine
for number, url in wayback_id_twitter_url:
    wayback_url_list.append(f"https://web.archive.org/web/{number}/{url}")

# create a dictionary with wayback url as key and the numeric portion of twitter url as value
fusion = dict(zip(wayback_url_list, twitter_id_list))

number_of_elements = len(fusion.keys())

if number_of_elements == 1:
    answer = input(f"\n{number_of_elements} deleted Tweet has been found.\nWould you like to download the Tweet,\nget its text only, both, or take a screenshot?\nType 'download' or 'text' or 'both' or 'screenshot'. Then press Enter. \n")
elif number_of_elements == 0:
    print(f"No deleted Tweets have been found.\nTry expanding the date range to check for more Tweets.\n")
    sys.exit()
else:
    answer = input(f"\nAbout {number_of_elements} deleted Tweets have been found\nWould you like to download the Tweets, get their text only, both, or take screenshots?\nType 'download' or 'text' or 'both' or 'screenshot'. Then press Enter. \n")

# Actual downloading occurs here
if answer.lower() == 'download':
    for url, number in tqdm(fusion.items(), position=0, leave=True):
        while True:
            try:
                r = session.get(url, allow_redirects=False)
                directory = pathlib.Path(username)
                directory.mkdir(exist_ok=True)
                with open(f"{username}/{number}.html", 'wb') as file:
                    file.write(r.content)
            except:
                print("\n\nThere is a problem with the connection.\n")
                time.sleep(0.5)
                print("Either the Wayback Machine is down or it's refusing the requests.\nYour Wi-Fi connection may also be down.")
                time.sleep(1)
                print("Retrying after 30 seconds...")
                time.sleep(30)
                continue
            break
    print(f"\nAll Tweets have been successfully downloaded!\nThey can be found as HTML files inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
    time.sleep(1)
    print(f"Have a great day! Thanks for using Twayback :)")
elif answer.lower() == 'text':
    textlist = []
    textonly = []
    for url in tqdm(wayback_url_list, position=0, leave=True):
        response2 = session.get(url, allow_redirects=False).text
        regex = re.compile('.*TweetTextSize TweetTextSize--jumbo.*')
        try:
            tweet = bs4.BeautifulSoup(response2, "lxml").find("p", {"class": regex}).getText()
            textonly.append(tweet + "\n\n---")
        except AttributeError:
            pass
    textlist = zip(missing_tweet_list, textonly)
    directory = pathlib.Path(username)
    directory.mkdir(exist_ok=True)
    with open(f"{username}/{username}_text.txt", 'w', encoding='utf-8') as file:
        for text in textlist:
            file.writelines(str(text[0]) + " " + text[1] +"\n" + "\n")
    print(f"\nA text file ({username}_text.txt) is saved, which lists all URLs for the deleted Tweets and their text, has been saved.\nYou can find it inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
    time.sleep(1)
    print(f"Have a great day! Thanks for using Twayback :)")
elif answer.lower() == 'both':
    textlist = []
    textonly = []
    for url in tqdm(wayback_url_list, position=0, leave=True, desc="Parsing text..."):
        response2 = session.get(url, allow_redirects=False).text
        regex = re.compile('.*TweetTextSize TweetTextSize--jumbo.*')
        try:
            tweet = bs4.BeautifulSoup(response2, "lxml").find("p", {"class": regex}).getText()
            textonly.append(tweet + "\n\n---")
        except AttributeError:
            pass
    textlist = zip(missing_tweet_list, textonly)
    directory = pathlib.Path(username)
    directory.mkdir(exist_ok=True)
    with open(f"{username}/{username}_text.txt", 'w', encoding='utf-8') as file:
        for text in textlist:
            file.writelines(str(text[0]) + " " + text[1] +"\n" + "\n")
    print("Text file has been successfully saved!\nNow downloading pages.")
    time.sleep(1)
    for url, number in tqdm(fusion.items(), position=0, leave=True, desc="Downloading HTML pages..."):
        while True:
            try:
                r = session.get(url, allow_redirects=False)
                directory = pathlib.Path(username)
                directory.mkdir(exist_ok=True)
                with open(f"{username}/{number}.html", 'wb') as file:
                    file.write(r.content)
            except:
                print("\n\nThere is a problem with the connection.\n")
                time.sleep(0.5)
                print("Either the Wayback Machine is down or it's refusing the requests.\nYour Wi-Fi connection may also be down.")
                time.sleep(1)
                print("Retrying after 30 seconds...")
                time.sleep(30)
                continue
            break
    print("HTML pages have been successfully saved!")
    time.sleep(2)
    print(f"\nA text file ({username}_text.txt) is saved, which lists all URLs for the deleted Tweets and their text, has been saved.\nHTML pages have also been downloaded.\nYou can find everything inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
    time.sleep(1)
    print(f"Have a great day! Thanks for using Twayback :)")
elif answer.lower() == "screenshot":
    for url in missing_tweet_list:
        link = f"https://archive.org/wayback/available?url={url}&timestamp=19800101"
        response1 = requests.get(link, allow_redirects=False)
        jsonResponse = response1.json()
        wayback_url_screenshot = (jsonResponse['archived_snapshots']['closest']['url'])
        wayback_screenshot.append(wayback_url_screenshot)
        wayback_screenshot= [g[:41] + 'if_' + g[41:] for g in wayback_screenshot]
    print('Taking screenshots...')
    time.sleep(1)
    print("This might take a long time depending on your Internet speed\nand number of Tweets to screenshot.")
    for url, number in zip(wayback_screenshot, twitter_id_list):
        directory = pathlib.Path(username)
        directory.mkdir(exist_ok=True)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=1')
        chrome = webdriver.Chrome(options=options)
        chrome.get(url)
        image = chrome.find_element(By.XPATH, "//*[@id='permalink-overlay-dialog']/div[3]/div/div/div[1]")
        for numbers in twitter_id_list:
            image.screenshot(f"{username}/{number}.png")
    print("Screenshots have been successfully saved!")
    time.sleep(2)
    print(f"\nYou can find screenshots inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
    time.sleep(1)
    print(f"Have a great day! Thanks for using Twayback :)")
else:
    sys.exit()
