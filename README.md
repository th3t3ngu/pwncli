# pwncli
Simple script in python3 to access [Have I been Pwnd](https://haveibeenpwned.com) via its [API](https://haveibeenpwned.com/api/v3) to check whether or not mail address(es) have occured in data breaches. Needs a valid API-key and an active subscription to work.

# Usage

    usage: pwncli.py [-h] [--manage-key] [--mail MAIL] [--list LIST]
    
    PwnCli – Checking mails via Have I Been Pwned API
    
    options:
      -h, --help    show this help message and exit
      --manage-key  show API-Key and/or configure
      --mail MAIL   Check a single mail adress
      --list LIST   Check a .txt with mail addresses (one address per line)

Getting started: run `./pwncli.py --manage-key` and insert your API-Key. Run this command again to show and/or manage your installed Key.
