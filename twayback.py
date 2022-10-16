import colorama
import requests
import platform
import argparse
from pathlib import Path
import asyncio
import sys
import re
import urllib3
from colorama import Fore, Back
from tqdm import tqdm
from time import sleep
from aiohttp import ClientSession
import asyncio
import random
import downloadTweets


# checks the status of a given url
async def checkStatus(url, session: ClientSession, sem: asyncio.Semaphore, proxy_server):
    
    async with sem:
        if proxy_server == '':
            async with session.get(url) as response:
                return url, response.status
        else:
            async with session.get(url, proxy = proxy_server) as response:
                return url, response.status
        
    
# controls our async event loop
async def asyncStarter(url_list, semaphore_size, proxy_list):
    
    status_list = []
    headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}
    proxy_server = chooseRandomProxy(proxy_list)
    
    # this will wrap our event loop and feed the the various urls to their async request function.
    async with ClientSession(headers=headers) as a_session:
        
        sem = asyncio.Semaphore(semaphore_size)

        # if aiohttp throws an error it will be caught and we'll try again up to 5 times
        for x in range(0,5):
            try:
                status_list = await asyncio.gather(*(checkStatus(u, a_session, sem, proxy_server) for u in url_list))
                break
            except:
                proxy_server = chooseRandomProxy(proxy_list)
                print(f"Error. Trying a differ proxy: {proxy_server}")
                status_list = []
                
    # return a list of the results 
    if status_list != []:   
        return status_list
    else:
        print("There was an error with aiohttp proxies. Please Try again")
        exit()

def chooseRandomProxy(proxy_list):
    if proxy_list != []:
        return "http://" + proxy_list[random.randint(0, len(proxy_list)-1)]
    else:
        return ''

colorama.init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Parse arguments passed in from command line
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, default='')
parser.add_argument('-from', '--fromdate', required=False, default='')
parser.add_argument('-to', '--todate', required=False, default='')
parser.add_argument('--batch-size', type=int, required=False, default=300, help="How many urls to examine at once.")
parser.add_argument('--semaphore-size', type=int, required=False, default=50, help="How many urls(from --batch-size) to query at once. Between 1 and 50")
parser.add_argument('--proxy-file', required=False, default='', help="A list of proxies the script will rotate through")
args = vars(parser.parse_args())

account_name = args['username']
from_date = args['fromdate']
to_date = args['todate']
batch_size = args['batch_size']
semaphore_size = args['semaphore_size']
proxy_file = args['proxy_file']

proxy_list = []
if proxy_file != '':
    with open(proxy_file, "r") as f:
        for x in f.readlines():
            proxy_list.append(x.split("\n")[0])


remove_list = ['-', '/']
from_date = from_date.translate({ord(x): None for x in remove_list})
to_date = to_date.translate({ord(x): None for x in remove_list})
account_url = f"https://twitter.com/{account_name}"
headers = {'User-Agent': 'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}


account_response = requests.get(account_url, headers=headers, allow_redirects=False)
status_code = account_response.status_code

if status_code == 200:
    print(Back.GREEN + Fore.WHITE + f"Account is ACTIVE")
elif status_code == 302:
    print(Back.RED + Fore.WHITE + f"Account is SUSPENDED. This means all of "
          f"{Back.WHITE + Fore.RED + account_name + Back.RED + Fore.WHITE}'s Tweets will be "
          f"downloaded.")
elif status_code ==429:
    print(Back.RED + Fore.WHITE + f"Respose Code 429: Too Many Requests. Your traffic to Twitter is being limited and results of this script will not be accurate")
    exit()
else:
    print(Back.RED + Fore.WHITE + f"No one currently has this handle. Twayback will search for a history of this "
          f"handle's Tweets.")
sleep(1)


wayback_cdx_url = f"https://web.archive.org/cdx/search/cdx?url=twitter.com/{account_name}/status" \
                  f"&matchType=prefix&filter=statuscode:200&mimetype:text/html&from={from_date}&to={to_date}"
cdx_page_text = requests.get(wayback_cdx_url).text

if len(re.findall(r'Blocked', cdx_page_text)) != 0:
    print(f"Sorry, no deleted Tweets can be retrieved for {account_name}.\n"
          f"This is because the Wayback Machine excludes Tweets for this handle.")
    sys.exit(-1)

# Capitalization does not matter for twitter links. Url parameters after '?' do not matter either.
# create a dict of {twitter_url: wayback_id}
tweet_id_and_url_dict = {line.split()[2].lower().split('?')[0]: line.split()[1] for line in cdx_page_text.splitlines()}

# create a list of just twitter urls
twitter_url_list = []
for url in tweet_id_and_url_dict:
    twitter_url_list.append(url)

number_of_elements = len(tweet_id_and_url_dict)
if number_of_elements >= 1000:
    print(f"Getting the status codes of {number_of_elements} unique archived Tweets...\nThat's a lot of Tweets! "
          f"It's gonna take some time.\nTip: You can use -from and -to to narrow your search between two dates.")
else:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\n")

# break out url list in to chunks and check asyncronously
results_list = []
counter = 0
for x in tqdm(range(0, len(twitter_url_list))):
    if counter==batch_size or x == len(twitter_url_list)-1 :
        results_list.extend(asyncio.run(asyncStarter(twitter_url_list[x-batch_size:x], semaphore_size, proxy_list)))
        counter = 0
    counter += 1
    
missed_tweet_count = 0
# list of just missing twitter url
missing_tweet_list = []
for result in results_list:
    if result[1] == 404:
        missing_tweet_list.append(str(result[0]))
    if result[1] == 429:
        missed_tweet_count += 1
if missed_tweet_count > 0:
    print(f"Skipped {missed_tweet_count} tweets due to 429 error. Recommend using rotating proxy servers")

# list of wayback ids for just missing tweets
wayback_id_list = []
for url in missing_tweet_list:
    wayback_id_list.append(tweet_id_and_url_dict[url])


wayback_url_dict = {}
for url, number in zip(missing_tweet_list, wayback_id_list):
    wayback_url_dict[number] = f"https://web.archive.org/web/{number}/{url}"

number_of_elements = len(wayback_url_dict)


# at the very least, create a csv with the info found
directory = Path(account_name)
directory.mkdir(exist_ok=True)
with open(f"{account_name}/{account_name}.csv", "w") as f:
    for x,y in zip (missing_tweet_list, wayback_url_dict.values()):
        f.write(f'{x},{y}\n')

if number_of_elements == 1:
    answer = input(f"\nOne deleted Tweet has been found.\nWould you like to download the Tweet,"
                   f"\nget its text only, both, or take a screenshot?\nType 'download' or 'text' or 'both' or "
                   f"'screenshot'. Then press Enter. \n")
elif number_of_elements == 0:
    print(f"No deleted Tweets have been found.\nTry expanding the date range to check for more Tweets.\n")
    sys.exit()
else:
    answer = input(f"\nAbout {number_of_elements} deleted Tweets have been found\nWould you like to download the "
                   f"Tweets, get their text only, both, or take screenshots?\nType 'download' or 'text' or 'both' "
                   f"or 'screenshot'. Then press Enter. \n").lower()

# Actual downloading occurs here

if answer =="text":
    downloadTweets.textOnly(account_name, wayback_url_dict)
elif answer =="download":
    downloadTweets.download(account_name, wayback_url_dict)
elif answer == "both":
    downloadTweets.textOnly(account_name, wayback_url_dict)
    downloadTweets.downloadOnly(account_name, wayback_url_dict)
elif answer == "screenshot":
    downloadTweets.screenshot(account_name, wayback_url_dict)