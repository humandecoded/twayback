# Twayback: Downloading deleted Tweets from the Wayback Machine, made easy

<div align="center">
  
![screenshot](https://i.imgur.com/oBeqt6V.png)

</div>

Finding and downloading deleted Tweets takes a lot of time. Thankfully, with this tool, it becomes a piece of cake! 🎂

Twayback is a portmanteau of *Twitter* and the *Wayback Machine*. Enter your desired Twitter username, and let Twayback do the rest!

## Features
 - Can download some or all of a user's archived deleted Tweets.
 - Lets you extract Tweets text to a text file (yes, even quote retweets!)
 - Has ability to screenshot deleted Tweets.
 - Allows custom time range to narrow search for deleted Tweets archived between two dates.
 - Differentiates between accounts that are active, suspended, or don't/no longer exist.
 - Lets you know if a target handle's archived Tweets have been excluded from the Wayback Machine.

## Usage
    twayback -u USERNAME [OPTIONS]
    
    -u, --username                                        Specify target user's Twitter handle
    
    -from, --fromdate                                     Narrow search for deleted Tweets *archived* on and after this date
                                                          (can be combined with -to)
                                                          (format YYYY-MM-DD or YYYY/MM/DD or YYYYMMDD, doesn't matter)
                                            
    -to, --todate                                         Narrow search for deleted Tweets *archived* on and before this date
                                                          (can be combined with -from)
                                                          (format YYYY-MM-DD or YYYY/MM/DD or YYYYMMDD, doesn't matter)
    Examples:
    twayback -u taylorswift13                             Downloads all of @taylorswift13's deleted Tweets
    
    twayback -u jack -from 2022-01-05                     Downloads all of @jack's deleted Tweets *archived* since January 5, 2022 until now
    
    twayback -u drake -to 2022/02/09                      Downloads all of @drake's deleted Tweets *archived* since the beginning until February 9, 2022
    
    twayback -u EA -from 2020-08-30 -to 2020-09-15        Downloads all of @EA's deleted Tweets *archived* between August 30, 2020 to September 15, 2020
    
## Twayback A vs Twayback B
Currently, there are two versions of Twayback:

  - Twayack A's pros: **faster**, no need to check status codes.
  - Twayback A's cons: **it does not work on Twitter accounts that currently have more than 3,200 Tweets.** [Known limitation.](https://twittercommunity.com/t/tweet-limit-at-3200/156391)
    - However, if account has fewer than 3,200 Tweets, Twayback A can download all their deleted archived Tweets.
<div align="center">
  
[![windows](https://img.shields.io/badge/Download-Twayback%20A%20for%20Windows-blue?style=for-the-badge&logo=Microsoft)](https://github.com/Mennaruuk/twayback/releases/download/02%2F14%2F2022/twayback.exe)
[![python](https://img.shields.io/badge/Download-Python%20script-red?style=for-the-badge&logo=python)](https://github.com/Mennaruuk/twayback/releases/download/02%2F14%2F2022/twayback.zip)
  
</div>

  - Twayback B's pros: no ~3,200 Tweets limit, so it can download all deleted archived Tweets **regardless of how many active Tweets the account has**.
  - Twayback B's cons: slower, requires status code checking.

<div align="center">

[![windows](https://img.shields.io/badge/Download-Twayback%20B%20for%20Windows-blue?style=for-the-badge&logo=Microsoft)](https://github.com/Mennaruuk/twayback/releases/download/02%2F14%2F2022/twayback_B.exe)
[![python](https://img.shields.io/badge/Download-Python%20script-red?style=for-the-badge&logo=python)](https://github.com/Mennaruuk/twayback/releases/download/02%2F14%2F2022/twayback_B.zip)
  
</div>

## Installation
### For Windows only
 1. Download the latest EXE file.
 2. Launch Command Prompt in the EXE file's directory.
 3. Run the command `twayback -u USERNAME` (Replace `USERNAME` with your target handle).

### For Windows, Linux, and macOS
 1. Download the latest Python script ZIP file.
 2. Extract ZIP file to a directory of your choice.
 3. Open terminal in that directory.
 4. Run the command `pip install -r requirements.txt`.
 5. Run the command `twayback.py -u USERNAME` (Replace `USERNAME` with your target handle).


For more information, check out the [Usage](#usage) section above.

## Screenshots
Screenshots are done using Selenium. To successfully take screenshots, please follow these steps:
 1. Make sure you have Chrome installed.
    - Firefox works, but you have to edit the script to replace Chrome with Firefox. Plus, Firefox isn't great with screenshots.
 2. Note your Chrome version.
 3. Go to [this page](https://chromedriver.chromium.org/downloads) and download the appropriate Chrome driver for your version of Chrome.
 4. Place the Chrome driver in your Python installation directory, or add it to PATH.
    - Add to PATH tutorials: [Windows](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/), [Linux](https://itsfoss.com/add-directory-to-path-linux/), [macOS](https://www.architectryan.com/2012/10/02/add-to-the-path-on-mac-os-x-mountain-lion/).



## Things to keep in mind
 - Quality of the HTML files depends on how the Wayback Machine saved them. Some are better than others.
 - This tool is best for text. You might have some luck with photos. You cannot download videos.
 - By definition, if an account is suspended or no longer exists, all their Tweets would be considered deleted.
 - Custom date range is not about when Tweets were made, but rather when they were _archived_. For example, a Tweet from 2011 may have been archived today.

## Call for help 🙏
I welcome, and encourage, contributions! They make my day.
What I can think of off the top of my head:
 - **Code simplification/improvement**: If you're a pro at Python and know better ways to do what's in the script, please feel free to do so! If it works well, if not better, I will most likely merge it 😃
 - **async/await**: This one is badly needed. I'm trying to create another version of the script that doesn't check the status code of every archived URL. Rather, it gets the list of archived URLs from the Wayback Machine, gets the list of online URLs from the Twitter profile, subtracts both, and splits the Twitter URLs to get their IDs to serve as filenames. All of this can be pretty slow without async/await. I tried implementing it, but I suck at it, and I don't know where to put what. Multithreading and multiprocessing are also good.
