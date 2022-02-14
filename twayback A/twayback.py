# This is Twayback A.
# This version is recommended for speed. It does not require status checking of archive links.
# Use Twayback B if the Twitter handle currently has more than 3,200 active Tweets.

import requests, re, os, argparse, sys, time, bs4, lxml, pathlib, time, threading
from pathlib import Path
from requests import Session
session = Session()
import simplejson as json
from tqdm import tqdm
import colorama
from colorama import  Fore, Back, Style
colorama.init(autoreset=True)
from bs4 import BeautifulSoup
import snscrape.modules.twitter as twitter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', required=True, default='')
parser.add_argument('-from','--fromdate', required=False, default='')
parser.add_argument('-to','--todate', required=False, default='')
args = vars(parser.parse_args())
username = args['username']
fromdate = args['fromdate']
todate = args['todate']

# Active, suspended, or doesn't exist?
data1 =f"https://twitter.com/{username}"
results = []
headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}

response = session.get(data1, headers=headers, allow_redirects=False)
status_code = response.status_code
if status_code == 200:
    print(Back.GREEN + Fore.WHITE + f"Account is ACTIVE\n")
    time.sleep(1)
elif status_code == 302:
    print(Back.RED + Fore.WHITE + f"Account is SUSPENDED. This means all of {Back.WHITE + Fore.RED + username + Back.RED + Fore.WHITE}'s Tweets will be downloaded.\n")
    time.sleep(3)
else:
    print(Back.RED + Fore.WHITE + f"No one currently has this handle. Twayback will search for a history of this handle's Tweets.\n")
    time.sleep(5)

stuck = "(Don't worry, Twayback isn't stuck!"

print(f"Please wait. Twayback is searching far and wide for deleted tweets from {username}.\nDrink some delicious coffee while this gets done.\n\n{Back.MAGENTA + stuck + Fore.WHITE}\nDepending on the number of Tweets, this step might take several minutes.)\n")

print(f"Grabbing links for Tweets from the Wayback Machine...\n")

link = f"https://web.archive.org/cdx/search/cdx?url=twitter.com/{username}/status&matchType=prefix&filter=statuscode:200&mimetype:text/html&from={fromdate}&to={todate}"
c = session.get(link).text

# Is Twitter handle excluded by the Wayback Machine?
blocklist = []
blocks = re.findall(r'Blocked', c)
for block in blocks:
    blocklist.append(f"{block}") 
    if any("Blocked" in s for s in blocklist):
        print(f"Sorry, no deleted Tweets can be retrieved for {username}.\nThis is because the Wayback Machine excludes Tweets for this handle.")
        exit()
    else:
        pass

# Get list of active (non-deleted) Tweets.
active_tweets = []

def userTweets(user=''):
    for i, tweet in enumerate(twitter.TwitterSearchScraper('from:' +user+ ' lang:"en" ').get_items()):
        active_tweets.append(tweet.url)

userTweets(username)


long_url = []
twitter_id = []

wayback_screenshot = []

c = session.get(link).text
r = re.compile(r"\b[0-9]{14}\b")
numbers = r.findall(c)
tweeties = re.findall(r'https?://(?:www\.)?(?:mobile\.)?twitter\.com/(?:#!/)?\w+/status(?:es)?/\d+', c)
class WaybackIDAppending:
    def wida(self):
        global wayback_id
        wayback_id = []
        for number in numbers:
            wayback_id.append(number)
    def __init__(self):
        t = threading.Thread(target=self.wida)
        t.start()

class TweetGettingAndIDSplitting:
    def tgaids(self):
        global twitter_url
        twitter_url = []
        for tweety in tweeties:
            twitter_url.append(tweety)
    def __init__(self):
        t = threading.Thread(target=self.tgaids)
        t.start()

class ZippingAndUnzipping:
    def zau(self):
        global wayback_id
        global twitter_url
        wayback_id_twitter_url = [(x, y) for x, y in zip(wayback_id, twitter_url) if y not in active_tweets]
        wayback_id = [x[0] for x in wayback_id_twitter_url]
        twitter_url = [x[1] for x in wayback_id_twitter_url]
    def __init__(self):
        t = threading.Thread(target=self.zau)
        t.start()

class CreateWaybackURL:
    def cwu(self):
        for number, tweety in zip(wayback_id, twitter_url):
            long_url.append(f"https://web.archive.org/web/{number}/{tweety}")
    def __init__(self):
        t = threading.Thread(target=self.cwu)
        t.start()

class SplitTwitterID:
    def sti(self):
        for url in twitter_url:
            regex = re.search(r"\b(\d{12,19})\b", url)
            if regex:
                twitter_id.append(regex.group())
    def __init__(self):
        t = threading.Thread(target=self.sti)
        t.start()

class Download:
    def download(self):
        for url in tqdm(wayback, position=0, leave=True):
            r = requests.get(url)
            directory = pathlib.Path(username)
            directory.mkdir(exist_ok=True)
            for number in twitter_id:
                with open(f"{username}/{number}.html", 'wb') as file:
                    file.write(r.content)
        print(f"\nAll Tweets have been successfully downloaded!\nThey can be found as HTML files inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
        time.sleep(1)
        print(f"Have a great day! Thanks for using Twayback :)")
    def __init__(self):
        t = threading.Thread(target=self.download)
        t.start()

class Text:
    def text(self):
        textlist = []
        textonly = []
        for url in tqdm(wayback, position=0, leave=True):
            response2 = session.get(url).text
            regex = re.compile('.*TweetTextSize TweetTextSize--jumbo.*')
            try:
                tweet = bs4.BeautifulSoup(response2, "lxml").find("p", {"class": regex}).getText()
                textonly.append(tweet + "\n\n---")
            except AttributeError:
                pass
        textlist = zip(twitter_url, textonly)
        directory = pathlib.Path(username)
        directory.mkdir(exist_ok=True)
        with open(f"{username}/{username}_text.txt", 'w', encoding='utf-8') as file:
            for text in textlist:
                file.writelines(str(text[0]) + " " + text[1] +"\n" + "\n")
        print(f"\nA text file ({username}_text.txt) is saved, which lists all URLs for the deleted Tweets and their text, has been saved.\nYou can find it inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
        time.sleep(1)
        print(f"Have a great day! Thanks for using Twayback :)")
    def __init__(self):
        t = threading.Thread(target=self.text)
        t.start()

class Both:
    def both(self):
        textlist = []
        textonly = []
        for url in tqdm(wayback, position=0, leave=True, desc="Parsing text..."):
            response2 = session.get(url).text
            regex = re.compile('.*TweetTextSize TweetTextSize--jumbo.*')
            try:
                tweet = bs4.BeautifulSoup(response2, "lxml").find("p", {"class": regex}).getText()
                textonly.append(tweet + "\n\n---")
            except AttributeError:
                pass
        textlist = zip(twitter_url, textonly)
        directory = pathlib.Path(username)
        directory.mkdir(exist_ok=True)
        with open(f"{username}/{username}_text.txt", 'w', encoding='utf-8') as file:
            for text in textlist:
                file.writelines(str(text[0]) + " " + text[1] +"\n" + "\n")
        print("Text file has been successfully saved!\nNow downloading pages.")
        time.sleep(1)
        for url in tqdm(wayback, position=0, leave=True, desc="Downloading HTML pages..."):
            r = requests.get(url)
            directory = pathlib.Path(username)
            directory.mkdir(exist_ok=True)
            for number in twitter_id:
                with open(f"{username}/{number}.html", 'wb') as file:
                    file.write(r.content)
        print("HTML pages have been successfully saved!")
        time.sleep(2)
        print(f"\nA text file ({username}_text.txt) is saved, which lists all URLs for the deleted Tweets and their text, has been saved.\nHTML pages have also been downloaded.\nYou can find everything inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
        time.sleep(1)
        print(f"Have a great day! Thanks for using Twayback :)")
    def __init__(self):
        t = threading.Thread(target=self.both)
        t.start()

class Screenshot:
    def screenshot(self):
        print('Taking screenshots...')
        time.sleep(2)
        print("This might take a long time depending on your Internet speed\nand number of Tweets to screenshot.")
        for url, number in zip(wayback_screenshot, twitter_id):
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
            for numbers in twitter_id:
                image.screenshot(f"{username}/{number}.png")
        print("Screenshots have been successfully saved!")
        time.sleep(2)
        print(f"\nYou can find screenshots inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\n")
        time.sleep(1)
        print(f"Have a great day! Thanks for using Twayback :)")
    def __init__(self):
        t = threading.Thread(target=self.screenshot)
        t.start()

WaybackIDAppending()
TweetGettingAndIDSplitting()
ZippingAndUnzipping()
CreateWaybackURL()
SplitTwitterID()

# List of Wayback Machine URLs to use for 'screenshot' ONLY.
wayback_screenshot = [a[:42] + 'if_' + a[42:] for a in long_url]
# List of Wayback Machine URLs to use for 'download', 'text', and 'both'. NOT 'screenshot'.
long_url = list(set(long_url))
wayback = long_url

number_of_elements = len(twitter_url)

if number_of_elements == 1:
    answer = input(f"\n{number_of_elements} deleted Tweet has been found.\nWould you like to download the Tweet,\nget its text only, both, or take a screenshot?\nType 'download' or 'text' or 'both' or 'screenshot'. Then press Enter. \n")
elif number_of_elements == 0:
    print(f"No deleted Tweets have been found.\nTry expanding the date range to check for more Tweets.\n")
    sys.exit()
else:
    answer = input(f"\nAbout {number_of_elements} deleted Tweets have been found\nWould you like to download the Tweets, get their text only, both, or take screenshots?\nType 'download' or 'text' or 'both' or 'screenshot'. Then press Enter. \n")

# Actual downloading occurs here
if answer.lower() == 'download':
    Download()
if answer.lower() == 'downlaod':
    Download()
elif answer.lower() == 'text':
    Text()
elif answer.lower() == 'txt':
    Text()
elif answer.lower() == 'both':
    Both()
elif answer.lower() == "screenshot":
    Screenshot()
elif answer.lower() == "screnshot":
    Screenshot()
else:
    print("Goodbye!")
