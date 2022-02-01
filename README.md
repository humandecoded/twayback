# Twayback: Download deleted Tweets from the Wayback Machine

Finding and downloading deleted Tweets takes a lot of time. Thankfully, with this tool, it becomes a piece of cake! 🎂

Twayback is a portmanteau of *Twitter* and the *Wayback Machine*. It's just a .bat file that runs two Python scripts. Enter your desired Twitter username, and let Twayback do the rest!

For now, it's Windows only. However, I'm finding ways to turn the code into Python entirely so that it can run on Linux and Mac.

## Requirements:

 1. Install [Python](https://www.python.org/downloads/)
 2. Install [Ruby](https://rubyinstaller.org/downloads/)
 3. After installing Ruby, install wayback_machine_downloader by launching Command Prompt and entering the following:
`gem install wayback_machine_downloader`

## Problems I'm aware of

 - Yes. The code is pretty messy. It's everywhere. But I don't even know Python. I just had an idea and a logic behind it, and scoured Stack Overflow and Reddit to get help.
 - I know about the limit mismatch. That is, if you tell the script "Download six tweets only", it will give you like three or four, not six. I'd love help on how I can have the script get as many deleted Tweets as the limit specified by the user. But it's too complex for me.
## Future plans
 - Batch is ugly. I'd like to have the whole code in Python. But I need to find equivalents for things like ECHO, GOTO, etc. Deleting and creating new files within Python shell might run into permission problems. So it'll take a while until everything is ported over.
 - GUI. This is a biggie. I don't know shit about Python, let alone GUI. But I'm hoping I can design one using Tkinter Designer. But I don't know how I can link actions to buttons and shit like that, so any help is appreciated, it would mean so much.

I hope you enjoy my little script. Please use it for good. Whatever you are, be a good one.

