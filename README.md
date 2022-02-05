# Twayback: Downloading deleted Tweets from the Wayback Machine, made easy

<div align="center">
  
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
  
[![windows](https://img.shields.io/badge/Download-Windows-blue?style=for-the-badge&logo=Microsoft)](https://github.com/Mennaruuk/twayback/releases/download/02%2F04%2F2022/twayback.exe)
[![python](https://img.shields.io/badge/Download-Python-red?style=for-the-badge&logo=python)](https://github.com/Mennaruuk/twayback/releases/download/02%2F04%2F2022/twayback.zip)

![screenshot](https://i.imgur.com/oBeqt6V.png)

</div>

Finding and downloading deleted Tweets takes a lot of time. Thankfully, with this tool, it becomes a piece of cake! 🎂

Twayback is a portmanteau of *Twitter* and the *Wayback Machine*. Enter your desired Twitter username, and let Twayback do the rest!

## Features
 - Can download some or all of a user's archived deleted Tweets.
 - Allows custom time range to narrow search for deleted Tweets archived between two dates.
 - Differentiates between accounts that are active, suspended, or don't/no longer exist.

## Usage
    twayback -u USERNAME [OPTIONS]
    
    -u, --username        Specify target user's Twitter handle
    -from, --fromdate     Narrow search for deleted Tweets *archived* on and after this date
                          (can be combined with -to)
    -to, --todate         Narrow search for deleted Tweets *archived* on and before this date
                          (can be combined with -from)

## Installation
### For Windows only
 1. [Download the EXE file.](https://github.com/Mennaruuk/twayback/releases/download/02%2F04%2F2022/twayback.exe)
 2. Launch Command Prompt in the EXE file's directory.
 3. Run the command `twayback -u USERNAME` (Replace `USERNAME` with your target handle).

### For Windows, Linux, and macOS
 1. [Download the ZIP file.](https://github.com/Mennaruuk/twayback/releases/download/02%2F04%2F2022/twayback.zip)
 2. Extract ZIP file to a directory of your choice.
 3. Open terminal in that directory.
 4. Run the command `pip install -r requirements.txt`.
 5. Run the command `twayback -u USERNAME` (Replace `USERNAME` with your target handle).


For more information, check out the [Usage](#usage) section above.

## Things to keep in mind
 - Quality of the HTML files depends on how the Wayback Machine saved them. Some are better than others.
 - This tool is best for text. You might have some luck with photos. You cannot download videos.
 - By definition, if an account is suspended or no longer exists, all their Tweets would be considered deleted.
 - Custom date range is not about when Tweets were made, but rather when they were _archived_. For example, a Tweet from 2011 may have been archived today.

## Future plans
 - GUI. This is a biggie. I don't know shit about Python, let alone GUI. But I'm hoping I can design one using [Tkinter Designer](https://github.com/ParthJadhav/Tkinter-Designer). But I don't know how I can link actions to buttons and shit like that, that stuff is super foreign to me, so any help is appreciated, it would mean so much.

Plenty of thanks to jsvine for his amazing work on [waybackpack](https://github.com/jsvine/waybackpack). Without it, this tool cannot work nearly as well.

I hope you enjoy my little script. Please use it for good. Whatever you are, be a good one.
