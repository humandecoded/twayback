# This is Twayback B.
# This version is recommended if you want to download all deleted Tweets. It requires status checking of archive links.

import requests, re, os, argparse, sys, time, bs4, lxml, pathlib, time, threading
from pathlib import Path
from requests import Session
session = Session()
import simplejson as json
from tqdm import tqdm as tqdm
import colorama
from colorama import  Fore, Back, Style
colorama.init(autoreset=True)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests.exceptions import ConnectionError

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
    time.sleep(4)

stuck = "(Don't worry, Twayback isn't stuck!"

print(f"Please wait. Twayback is searching far and wide for deleted tweets from {username}.\nDrink some delicious coffee while this gets done.\n\n{Back.MAGENTA + stuck + Fore.WHITE}\nDepending on the number of Tweets, this step might take several minutes.)\n")

print(f"Grabbing links for Tweets from the Wayback Machine...\n")

link = f"https://web.archive.org/cdx/search/cdx?url=twitter.com/{username}/status&matchType=prefix&filter=statuscode:200&mimetype:text/html&from={fromdate}&to={todate}"

data2 = []
data4 = []
data5=[]
twitter_id = []
wayback_screenshot = []
wayback = []

c = session.get(link).text
urls = re.findall(r'https?://(?:www\.)?(?:mobile\.)?twitter\.com/(?:#!/)?\w+/status(?:es)?/\d+', c)
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

# Attach all archived Tweet links to data2
class FetchingArchiveURLs:
    def faurl(self):
        global urls
        for url in urls:
            data2.append(f"{url}")
    def __init__(self):
        t = threading.Thread(target=self.faurl)
        t.start()

FetchingArchiveURLs()

# Remove duplicate links
data3 = list(set(data2))

number_of_elements = len(data3)
if number_of_elements >= 1000:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\nThat's a lot of Tweets! It's gonna take some time.\nTip: You can use -from and -to to narrow your search between two dates.")
else:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\n")

# Obtain status codes

results = []
headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}

for url in tqdm(data3):
    response = session.get(url, headers=headers)
    status_code = response.status_code
    results.append((url, status_code))

for url, status_code in results:
    data3.append(f"{url} {status_code}")

class DeletedTweetsOnly:
    def dto(self):
        global data3
        global data4
        global data5
        data4 = [g for g in data3 if " 404" in g]
        data5 = [g.replace(' 404', '') for g in data4]
    def __init__(self):
        t = threading.Thread(target=self.dto)
        t.start()

class SplitTwitterID:
    def sti(self):
        global data5
        global twitter_id
        for url in data5:
            regex = re.search(r"\b(\d{12,19})\b", url)
            if regex:
                twitter_id.append(regex.group())
    def __init__(self):
        t = threading.Thread(target=self.sti)
        t.start()

class ScreenshotURLs:
    def surls(self):
        global data5
        global wayback_screenshot
        for url in data5:
            link = f"http://archive.org/wayback/available?url={url}&timestamp=19800101"
            response1 = session.get(link)
            jsonResponse = response1.json()
            wayback_url_screenshot = (jsonResponse['archived_snapshots']['closest']['url'])
            wayback_screenshot.append(wayback_url_screenshot)
            wayback_screenshot= [g[:41] + 'if_' + g[41:] for g in wayback_screenshot]
    def __init__(self):
        t = threading.Thread(target=self.surls)
        t.start()

class NonScreenshotURLs:
    def nsurls(self):
        global data5
        global wayback
        for url in data5:
            link = f"http://archive.org/wayback/available?url={url}&timestamp=19800101"
            response1 = session.get(link)
            jsonResponse = response1.json()
            wayback_url = (jsonResponse['archived_snapshots']['closest']['url'])
            wayback.append(wayback_url)
    def __init__(self):
        t = threading.Thread(target=self.nsurls)
        t.start()
        
DeletedTweetsOnly()
SplitTwitterID()
NonScreenshotURLs()

class Download:
    def download(self):
        for url in tqdm(wayback, position=0, leave=True):
            while True:
                try:
                    r = requests.get(url)
                    directory = pathlib.Path(username)
                    directory.mkdir(exist_ok=True)
                    for number in twitter_id:
                        with open(f"{username}/{number}.html", 'wb') as file:
                            file.write(r.content)
                except ConnectionError as CE:
                    print("There is a problem with the connection.\n")
                    time.sleep(0.5)
                    print("Either the Wayback Machine is down or it's refusing the requests.\nYour Wi-Fi connection may also be down.")
                    time.sleep(1)
                    print("Retrying...")
                    continue
                break
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
        textlist = zip(data5, textonly)
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
        textlist = zip(data5, textonly)
        directory = pathlib.Path(username)
        directory.mkdir(exist_ok=True)
        with open(f"{username}/{username}_text.txt", 'w', encoding='utf-8') as file:
            for text in textlist:
                file.writelines(str(text[0]) + " " + text[1] +"\n" + "\n")
        print("Text file has been successfully saved!\nNow downloading pages.")
        time.sleep(1)
        for url in tqdm(wayback, position=0, leave=True, desc="Downloading HTML pages..."):
            while True:
                try:
                    r = requests.get(url)
                    directory = pathlib.Path(username)
                    directory.mkdir(exist_ok=True)
                    for number in twitter_id:
                        with open(f"{username}/{number}.html", 'wb') as file:
                            file.write(r.content)
                except ConnectionError as CE:
                    print("There is a problem with the connection.\n")
                    time.sleep(0.5)
                    print("Either the Wayback Machine is down or it's refusing the requests.\nYour Wi-Fi connection may also be down.")
                    time.sleep(1)
                    print("Retrying...")
                    continue
                break
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

number_of_elements = len(data5)

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
elif answer.lower() == 'text':
    Text()
elif answer.lower() == 'both':
    Both()
elif answer.lower() == "screenshot":
    ScreenshotURLs()
    Screenshot()
else:
    sys.exit()
