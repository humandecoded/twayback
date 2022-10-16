from pathlib import Path
import requests
from requests_futures.sessions import FuturesSession
from tqdm import tqdm
import bs4
from colorama import Fore, Back
from time import sleep
from playwright.sync_api import sync_playwright
import re
from concurrent.futures import as_completed


def downloadOnly(account_name, wayback_url_dict):
    headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}
    directory = Path(account_name)
    directory.mkdir(exist_ok=True)
    dont_spam_user = False
    deleted_tweets_futures = {}
    deleted_tweets_futures_retry = {}

    with FuturesSession(max_workers=5) as session:
        for number, url in tqdm(wayback_url_dict.items(), position=0, leave=True):
            deleted_tweets_futures[number] = session.get(url, headers=headers, timeout=30)

    for completed_future_number, completed_future in tqdm(deleted_tweets_futures.items(), position=0, leave=True):
        result = None
        try:
            result = completed_future.result()
            with open(f"{account_name}/{completed_future_number}.html", 'wb') as f:
                f.write(result.content)
        except:
            if not dont_spam_user:
                print("\n\nThere is a problem with the connection.\n")
                sleep(0.5)
                print("Either the Wayback Machine is down or it's refusing the requests.\n"
                    "Your Wi-Fi connection may also be down.")
                sleep(1)
                print("Retrying...")
                # Make sure that cascading failures don't spam text on the terminal.
                dont_spam_user = True
            if result is not None:
                deleted_tweets_futures_retry[completed_future_number] = session.get(result.url,
                                                                                    headers=headers, timeout=30)
    for completed_future_number, completed_future in tqdm(deleted_tweets_futures_retry.items(),
                                                        position=0, leave=True):
        try:
            with open(f"{account_name}/{completed_future_number}.html", 'wb') as f:
                f.write(completed_future.result().content)
        except:
            # Give up if the 2nd time around doesn't work.
            continue

    print(f"\nAll Tweets have been successfully downloaded!\nThey can be found as HTML files inside the folder "
        f"{Back.MAGENTA + Fore.WHITE + account_name + Back.BLACK + Fore.WHITE}.")


def textOnly(account_name, wayback_url_dict ):
    headers = {'user-agent':'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'}
    directory = Path(account_name)
    directory.mkdir(exist_ok=True)
    futures_list = []
    regex = re.compile('.*TweetTextSize TweetTextSize--jumbo.*')

    with FuturesSession(max_workers=5) as session:
        for number, url in tqdm(wayback_url_dict.items(), position=0, leave=True):
            futures_list.append(session.get(url))
    for future in as_completed(futures_list):
        try:
            result = future.result()
            tweet = bs4.BeautifulSoup(result.content, "lxml").find("p", {"class": regex}).getText()
            with open(f"{account_name}/{account_name}_text.txt", 'a') as f:
                f.write(str(result.url.split('/', 5)[:-1]) + " " + tweet + "\n\n---\n\n")
        except AttributeError:
            pass
        except ConnectionError:
            print('Connection error occurred while fetching tweet text!')

    print(f"\nA text file ({account_name}_text.txt) is saved, which lists all URLs for the deleted Tweets and "
        f"their text, has been saved.\nYou can find it inside the folder "
        f"{Back.MAGENTA + Fore.WHITE + account_name + Back.BLACK + Fore.WHITE}.")


def screenshot(account_name, wayback_url_dict):
    wayback_screenshots = {}
    screenshot_futures = []

    directory = Path(account_name)
    directory.mkdir(exist_ok=True)
    for number, url in wayback_url_dict.items():
        # Gets the oldest version saved
        link = f"https://archive.org/wayback/available?url={url}&timestamp=19800101"
        response1 = requests.get(link)
        jsonResponse = response1.json()
        wayback_url_screenshot = jsonResponse['url']
        # Example:
        # https://web.archive.org/web/20211108191302/https://accentusoft.com/
        # We want it like this, to remove the Wayback snapshots header:
        # https://web.archive.org/web/20211108191302if_/https://accentusoft.com/
        wayback_url_screenshot_parts = wayback_url_screenshot.split('/')
        wayback_url_screenshot_parts[4] += 'if_'
        wayback_url_screenshot = '/'.join(wayback_url_screenshot_parts)
        wayback_screenshots[number] = wayback_url_screenshot
    print('Taking screenshots...')
    sleep(1)
    print("This might take a long time depending on your Internet speed\nand number of Tweets to screenshot.")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)'
        )
        page = context.new_page()
        for number, tweet_to_screenshot in tqdm(wayback_screenshots.items(), position=0):
            page.goto(tweet_to_screenshot, wait_until='domcontentloaded', timeout=0)
            page.locator('.TweetTextSize--jumbo').screenshot(
                path=f"{account_name}/{number}.png")

        context.close()
        browser.close()

    print("Screenshots have been successfully saved!")
    sleep(1)
    print(f"\nYou can find screenshots inside the folder "
        f"{Back.MAGENTA + Fore.WHITE + account_name + Back.BLACK + Fore.WHITE}.")
