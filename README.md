# Twayback: Downloading deleted Tweets from the Wayback Machine, made easy

<div align="center">
  

[![windows](https://img.shields.io/badge/Download-EXE%20FILE-blue?style=for-the-badge&logo=Microsoft)](https://github.com/Mennaruuk/twayback/releases/download/03%2F09%2F2022/twayback.exe)
[![python](https://img.shields.io/badge/Download-Python%20script-red?style=for-the-badge&logo=python)](https://github.com/Mennaruuk/twayback/releases/download/03%2F09%2F2022/twayback.zip)
  
[Lire en français](https://github.com/Mennaruuk/twayback/blob/88ceb554ac0d445172dd4f41197cbc4ca83d169c/fr_README.md)
  
![screenshot](https://i.imgur.com/oBeqt6V.png)

# Looking for new maintainer

**I know this repo has been needing some love. If anyone is interested in taking ownership of this repo, please contact me! Either [post a discussion](https://github.com/Mennaruuk/twayback/discussions/new) or email me at mennaruuk at protonmail dot com.**

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
 - Saves a log of the deleted tweet URLs in case you want to view on the Wayback Machine

## Usage
>    twayback -u USERNAME [OPTIONS]
    
    -u, --username                                        Specify target user's Twitter handle

    --batch-size                                          Specify how many URLs you would like to 
                                                          examine at a time. Expecting an integer between
                                                          1 and 100. A larger number will give you a speed
                                                          boost but at the risk of errors. Default = 100

    --semaphore-size                                      Specify how many urls from --batch-size you would 
                                                          like to query asyncronously at once. Expecting an integer
                                                          between 1 and 50. A larger number number will give you a speed
                                                          boost but at the risk of errors. Default = 50
    
    -from, --fromdate                                     Narrow search for deleted Tweets *archived*
                                                          on and after this date
                                                          (can be combined with -to)
                                                          (format YYYY-MM-DD or YYYY/MM/DD
                                                          or YYYYMMDD, doesn't matter)
                                            
    -to, --todate                                         Narrow search for deleted Tweets *archived*
                                                          on and before this date
                                                          (can be combined with -from)
                                                          (format YYYY-MM-DD or YYYY/MM/DD
                                                          or YYYYMMDD, doesn't matter)
    Examples:
    twayback -u taylorswift13                             Downloads all of @taylorswift13's
                                                          deleted Tweets
    
    twayback -u jack -from 2022-01-05                     Downloads all of @jack's
                                                          deleted Tweets
                                                          *archived* since January 5,
                                                          2022 until now
    
    twayback -u drake -to 2022/02/09                      Downloads all of @drake's
                                                          deleted Tweets *archived*
                                                          since the beginning until
                                                          February 9, 2022
    
    twayback -u EA -from 2020-08-30 -to 2020-09-15        Downloads all of @EA's
                                                          deleted Tweets *archived*
                                                          between August 30, 2020 to
                                                          September 15, 2020

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
 
 ### Additional information for macOS
 - You can also install Twayback in the following way:
 ```
 git clone https://github.com/Mennaruuk/twayback
 ``` 
 
 - You can also use Python Virtualenv (Virtual Environment) in order to avoid conflicting packages | libs
 
 ```
 cd twayback
 ```
 
 ```
 pip3 install -r requirements.txt
 ```
 depending on versions
 ```
 pip install -r requirements.txt
 ```
 
Run the command:
```
python3 twayback.py -u USERNAME

```
(Replace `USERNAME` with your target handle).


For more information, check out the [Usage](#usage) section above.

## Screenshots
**(I'm aware that screenshots for pre-2016 Tweets aren't working. I'm currently trying my best to fix it, but I've been running into errors. As soon as I fix it, I will ship a version that works for all Tweets. Thanks for your patience!)**

Screenshots are done using Playwright. To successfully take screenshots, please follow these steps:
 1. Open a terminal window.
 2. Run: `playwright install`.

## Troubleshooting
The larger the number of tweets your query has the higher your chances of encountering errors during execution. The default speed settings for `--semaphore-size` and `--batch-size` are set to the fastest possible execution. Reduce these numbers to slow down your execution and reduce the chance of errors. 

## Things to keep in mind
 - Quality of the HTML files depends on how the Wayback Machine saved them. Some are better than others.
 - This tool is best for text. You might have some luck with photos. You cannot download videos.
 - By definition, if an account is suspended or no longer exists, all their Tweets would be considered deleted.
 - Custom date range is not about when Tweets were made, but rather when they were _archived_. For example, a Tweet from 2011 may have been archived today.

## Call for help 🙏
I welcome, and encourage, contributions! They make my day.
What I can think of off the top of my head:
 - **Increasing download speed:** It'd be nice to increase the speed at which files are downloaded. `requests` takes me 5 seconds to download a file in kilobytes. There exist faster alternatives to requests, such as `pycURL`, `faster_than_requests`, and `urllib3`. I haven't gotten them to successfully work. I just want to use the faster library to download the HTML files and parse the text, it's okay if the rest is done with `requests`.
 -  **Code simplification/improvement**: If you're a pro at Python and know better ways to do what's in the script, please feel free to do so! If it works well, if not better, I will most likely merge it 😃
 - **Error Handling:** Set up error handling that would react to crashes. Potentially saving work as it goes and trying to restart from a certain point after a crash. For example: In a session if it crashed after checking the status of half of the URLs it would then restart itself and know to skip the URLs it has already checked this session.
 - **Use of Proxiese:** Build in ability for users to set up list of proxy IPs to rotate through if traffic is being blocked or limited
