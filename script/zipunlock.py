from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm

wordlist_path = Path(input('Enter path to the wordlist file > '))
zip_path = Path(input('Enter path to zipped file > '))

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