# Twayback: Downloading deleted Tweets from the Wayback Machine, made easy

<p align="center">
  <a href="https://github.com/Mennaruuk/twayback/releases/download/v1.0.0/twayback.zip"><img alt="undefined" src="https://img.shields.io/badge/Download-Here-orange?style=for-the-badge&logo=github"></a>
</p>

Finding and downloading deleted Tweets takes a lot of time. Thankfully, with this tool, it becomes a piece of cake! 🎂

Twayback is a portmanteau of *Twitter* and the *Wayback Machine*. It's just a .bat file that runs two Python scripts. Enter your desired Twitter username, and let Twayback do the rest!

For now, it's Windows only. However, I'm finding ways to turn the code into Python entirely so that it can run on Linux and Mac.

## Requirements:

 1. Install [Python](https://www.python.org/downloads/)
 2. Install [Ruby](https://rubyinstaller.org/downloads/)
 3. After installing Ruby, install [wayback_machine_downloader](https://github.com/hartator/wayback-machine-downloader) by launching Command Prompt and entering the following:


`gem install wayback_machine_downloader`

## How to run:

 1. [Download](https://github.com/Mennaruuk/twayback/releases/download/v1.0.0/twayback.zip)
 2. Extract to a folder
 3. Open that folder
 4. Double click **run.bat**
 5. Enter username
 6. (Optional) Enter from date (earliest date you'd like to search), to date (latest date you'd like to search), and limit (how many Tweets?).
 7. Program will search for deleted Tweets. Depending on your Internet connection, computer performance, and number of Tweets, this might take a while.
 8. Once done, program will tell you how many deleted Tweets found, and if you'd like to download them. Type **y** to download.
 9. Program will then start downloading the Tweets.
 10. Once done, deleted Tweets should be found as HTML files in the folder _websites_. Also, a list of all deleted Tweets can be found in the text file username_deleted_tweets.txt.

## Problems I'm aware of

 - Yes. The code is pretty messy. It's everywhere. But I don't even know Python. I just had an idea and a logic behind it, and scoured Stack Overflow and Reddit to get help. I promise that I will clean it up and make it look nicer.
 - I know about the limit mismatch. That is, if you tell the script "Download six tweets only", it will give you like three or four, not six. That is because the tool doesn't set out to find six deleted Tweets. Rather, it sets out to find six Tweets, then checks if any of them are deleted. So I need to find a way to have the program recognize when there is a mismatch, then go back and scour for more Tweets until it reaches the right number. I'd appreciate any help. Once I have some time, I'll think about it and find a way, I'm sure some if/then statements can do the job.
 - When the script finishes, there are two things I want to happen that aren't happening even after I wrote them in the batch script. One is to delete the file temp6.txt. The other is to rename the file username_deleted_tweets1.txt to username_deleted_tweets.txt then go through the file and deleted the string **wayback_machine_downloader ** wherever it's found. If anyone can help me with these, I'd appreciate it so much!
## Future plans
 - Batch is ugly. I'd like to have the whole code in Python. But I need to find equivalents for things like ECHO, GOTO, etc. Deleting and creating new files within Python shell might run into permission problems. So it'll take a while until everything is ported over.
 - GUI. This is a biggie. I don't know shit about Python, let alone GUI. But I'm hoping I can design one using [Tkinter Designer](https://github.com/ParthJadhav/Tkinter-Designer). But I don't know how I can link actions to buttons and shit like that, so any help is appreciated, it would mean so much.
 - Similar to GUI: Make an ELI5 README.md. I don't just want coders and nerds using this; I want laypeople to use it. Hope I can make an easy-to-understand no-frills version.
 - Not sure if it's possible, but make an EXE version. Does anyone know if I can compile this with Ruby and Python all in one, and maybe even wayback_machine_downloader installed, so that it becomes a one-step process to download? Thanks.

## Things to keep in mind
 - Quality of the HTML files depends on how the Wayback Machine saved them. Some are better than others.
 - This tool is best for text. You might have some luck with photos. You won't find luck getting videos though.


## Logic
Program gets the username and inputs it into the [Wayback CDX server API](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md). It searches for all Tweets that have the 200 status code, since 302s most likely retweets. After that, the program sends GET requests to each URL with headers specifying the BingBot. This is so that it can accurately tell you if the Tweets in question are still up or down. It throws away all the Tweets that are online, and only keeps the ones that have a 404 status code (thus deleted). Then, it uses [wayback_machine_downloader](https://github.com/hartator/wayback-machine-downloader) by hartator to download the HTML files.

I hope you enjoy my little script. Please use it for good. Whatever you are, be a good one.

