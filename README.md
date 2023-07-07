# Twayback: Downloading deleted Tweets from the Wayback Machine, made easy

# Sad News July 2023 - Due to recent changes to the Twitter platform, this tool is unable to work as intended. Login is required to even view tweets not to mention the rate limiting. I'll leave this repo up in case anyone wants to learn from it but I likely will not be updating the tool. Thank you to everyone that contributed and found some utility in this project.

Finding and downloading deleted Tweets takes a lot of time. Thankfully, with this tool, it becomes a piece of cake! 🎂

Twayback is a portmanteau of *Twitter* and the *Wayback Machine*. Enter your desired Twitter username, and let Twayback do the rest!

## Features
 - Can download some or all of a user's archived deleted Tweets.
 - Lets you extract Tweets text to a text file (yes, even quote retweets!)
 - Has ability to screenshot deleted Tweets.
 - Allows custom time range to narrow search for deleted Tweets archived between two dates.
 - Differentiates between accounts that are active, suspended, or don't/no longer exist.
 - Lets you know if a target handle's archived Tweets have been excluded from the Wayback Machine.
 - Saves a log of the deleted tweet URLs in case you want to view on the Wayback Machine.
 - Ability to rotate through a list of proxy servers to avoid 429 errors. **You will need to do this for data sets larger than about 800 tweets.**

## Usage
>    twayback -u USERNAME [OPTIONS]
    
    -u, --username                                        Specify target user's Twitter handle

    --batch-size                                          Specify how many URLs you would like to 
                                                          examine at a time. Expecting an integer between
                                                          1 and 100. A larger number will give you a speed
                                                          boost but at the risk of errors. Default = 100

    --semaphore-size                                      Specify how many urls from --batch-size you would 
                                                          like to query asyncronously at once. Expecting an integer
                                                          between 1 and 50. A larger number will give you a speed
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


    --proxy-file                                          Provide a list of proxies to use. You'll need this for checking large groups of tweets
                                                          Each line should contain one url:port to use
                                                          The script will pick a new proxy from the list at random after each --batch-size       

    
    Logs                                                  After checking a user's tweets but before you
                                                          make a download selection, a folder will be created
                                                          with that username. That folder will contain a log of:
                                                          <deleted-twitter-url>:<deleted-wayback-url> in case you needed them

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

    

#### Installation
 ```
 git clone https://github.com/Mennaruuk/twayback
 ``` 
 
 ```
 cd twayback
 ```
 
 ```
 pip3 install -r requirements.txt
 ```
 or possibly
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

Screenshots are done using Playwright. To successfully take screenshots, please follow these steps:
 1. Open a terminal window.
 2. Run: `playwright install`.

## Troubleshooting
The default speed settings for `--semaphore-size` and `--batch-size` are set to the fastest possible execution. Reduce these numbers to slow down your execution and reduce the chance of errors. 
For checking large numbers of tweets (> than 800) you'll need to use web proxies and `--proxy-file` flag

## Things to keep in mind
 - Quality of the HTML files depends on how the Wayback Machine saved them. Some are better than others.
 - This tool is best for text. You might have some luck with photos. You cannot download videos.
 - By definition, if an account is suspended or no longer exists, all their Tweets would be considered deleted.
 - Custom date range is not about when Tweets were made, but rather when they were _archived_. For example, a Tweet from 2011 may have been archived today.


