import requests, re, os, argparse, sys, waybackpack, time, subprocess
from requests import Session
session = Session()
from tqdm import tqdm
import colorama
from colorama import  Fore, Back, Style
colorama.init(autoreset=True)
os.system('cls')

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
    time.sleep(2)

stuck = "(Don't worry, Twayback isn't stuck!"

print(f"Please wait. Twayback is searching far and wide for deleted tweets from {username}.\nDrink some delicious coffee while this gets done.\n\n{Back.MAGENTA + stuck + Fore.WHITE}\nDepending on the number of Tweets, this step might take several minutes.)\n")

print(f"Grabbing links for Tweets from the Wayback Machine...\n")

link = f"https://web.archive.org/cdx/search/cdx?url=twitter.com/{username}/status&matchType=prefix&filter=statuscode:200&from={fromdate}&to={todate}"
data2 = []

c = session.get(link).text
urls = re.findall(r'https?://(?:www\.)?(?:mobile\.)?twitter\.com/(?:#!/)?\w+/status(?:es)?/\d+', c)
blocklist = []
blocks = re.findall(r'Blocked', c)
for block in blocks:
    blocklist.append(f"{block}") 
    if any("Blocked" in s for s in blocklist):
        print(f"Sorry, no deleted Tweets can be retrieved for {username}.\nThis is because the Wayback Machine excludes Tweets for this handle.")
        exit()
    else:
        pass

username_character_count = len(username)
if username_character_count == 1:
    data2 = [g for g in data2 if len(str(g)) <= 48]
elif username_character_count == 2:
    data2 = [g for g in data2 if len(str(g)) <= 49]
elif username_character_count == 3:
    data2 = [g for g in data2 if len(str(g)) <= 50]
elif username_character_count == 4:
    data2 = [g for g in data2 if len(str(g)) <= 51]
elif username_character_count == 5:
    data2 = [g for g in data2 if len(str(g)) <= 52]
elif username_character_count == 6:
    data2 = [g for g in data2 if len(str(g)) <= 53]
elif username_character_count == 7:
    data2 = [g for g in data2 if len(str(g)) <= 54]
elif username_character_count == 8:
    data2 = [g for g in data2 if len(str(g)) <= 55]
elif username_character_count == 9:
    data2 = [g for g in data2 if len(str(g)) <= 56]
elif username_character_count == 10:
    data2 = [g for g in data2 if len(str(g)) <= 57]
elif username_character_count == 11:
    data2 = [g for g in data2 if len(str(g)) <= 58]
elif username_character_count == 12:
    data2 = [g for g in data2 if len(str(g)) <= 59]
elif username_character_count == 13:
    data2 = [g for g in data2 if len(str(g)) <= 60]
elif username_character_count == 14:
    data2 = [g for g in data2 if len(str(g)) <= 61]
elif username_character_count == 15:
    data2 = [g for g in data2 if len(str(g)) <= 62]
else:
    pass
 
for url in urls:
    data2.append(f"{url}")
    
# Remove duplicate URLs
data3 = list(set(data2))

number_of_elements = len(data3)
if number_of_elements >= 1000:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\nThat's a lot of Tweets! It's gonna take some time.\nTip: You can use -from and -to to narrow your search between two dates.")
else:
    print(f"Getting the status codes of {number_of_elements} archived Tweets...\n")

# Obtain status codes
results = []
headers = {'user-agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}

for url in tqdm(data3):
    response = session.get(url, headers=headers)
    status_code = response.status_code
    results.append((url, status_code))

# Append URL and status code
for url, status_code in results:
    data3.append(f"{url} {status_code}")

# Filter for only deleted Tweets
data4 = [g for g in data3 if " 404" in g]
data5 = [g.replace(' 404', '') for g in data4]

os.system('cls')

number_of_elements = len(data5)

if number_of_elements == 1:
    answer = input(f"\n{number_of_elements} deleted Tweet has been found.\nWould you like to download it? Type yes or no. Then press Enter. \n")
elif number_of_elements == 0:
    answer = f"No deleted Tweets have been found.\nTry expanding the date range to check for more Tweets.\n"
    exit()
else:
    answer = input(f"\n{number_of_elements} deleted Tweets have been found.\nWould you like to download them all? Type yes or no. Then press Enter. \n")
os.system('cls')
# Use waybackpack to download URLs
if answer.lower() == 'yes':
    for url in tqdm(data5, position=0, leave=True):
        subprocess.run(f"waybackpack -d {username}  --uniques-only --raw {url}", text=True, capture_output=True)
        with open(f'{username}/{username}.txt', 'w') as file:
            for row in data5:
                s = "".join(map(str, row))
                file.write(s+'\n')
    print(f"\nAll Tweets have been successfully downloaded!\nThey can be found as HTML files inside the folder {Back.MAGENTA + Fore.WHITE + username + Back.BLACK + Fore.WHITE}.\nAlso, a text file ({username}.txt) is saved, which lists all URLs for the deleted Tweets.")
    time.sleep(1)
    print(f"Have a great day! Thanks for using Twayback :)")
else:
    print("Goodbye!")
