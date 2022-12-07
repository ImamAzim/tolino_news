#!/usr/bin/env python3

import subprocess
import signal
import time
import os
import tempfile


MIN_DELAY = 10 # minimum time between two requests to fetch news. used to avoid multiple udev event
WAIT_TIME = 10
# RECIPE_FOLDER = os.path.join(os.environ['HOME'], '.config', 'calibre', 'custom_recipes')
# EPUB_FOLDER = os.path.join(os.environ['HOME'], '.config', 'calibre', 'to_transfer')
APP_FOLDER = os.path.join(os.environ['HOME'], '.config', 'calibre', 'news_loader')
if not os.path.exists(APP_FOLDER):
    os.makedirs(APP_FOLDER)

global t1
t1 = time.time()

def run_script(signal, frame):
    global t1
    print('received usr1 signal')
    t2 = time.time()
    dt = t2 - t1
    t1 = time.time()

    if dt > MIN_DELAY:
        print('fetch news and copy to kobo')
        time.sleep(WAIT_TIME)
        subprocess.call('/root/bin/load_news.sh')
    else:
        print('delay to short. do nothing')

signal.signal(signal.SIGUSR1, run_script)



def fetch_all_news():
    recipe_paths, epub_paths, usernames, passwords = get_paths(folder)

    for recipe_path, epub_path, username, password in zip(recipe_paths, epub_paths, usernames, passwords):
        fetch_news(recipe_path, epub_path)

def get_paths(folder):
    files = os.listdir(folder)

    recipe_names = [filename for filename in files if filename.split('.')[-1]=='recipe']
    names = [''.join(name.split('.')[:-1]) for name in recipe_names]

    recipe_paths = [os.path.join(folder, recipe_name) for recipe_name in recipe_names]

    epub_names = [f'{name}.epub' for name in names]
    epub_paths = [os.path.join(folder, epub_name) for epub_name in epub_names]

    passwords = list()
    usernames = list()
    for name in names:
        filename = f'{name}.credentials'
        if filename in files:
            path = os.path.join(folder, filename)
            with open(path, 'r') as myfile:
                # text = myfile.read()
            # lines = text.split('\n')
                for line in myfile:
                    key, value = line.split('=')
                    if key == 'password':
                        passwords.append(value)
                    if key == 'username':
                        usernames.append(value)
        else:
            passwords.append(None)
            usernames.append(None)

    return recipe_paths, epub_paths, usernames, passwords


def fetch_news(recipe_path, epub_path, username=None, password=None):
    cmd = ['ebook-convert', recipe_path, epub_path, '--output-profile=kobo']
    if username is not None:
        cmd += [f'--username={username}']
    if password is not None:
        cmd += [f'--password={password}']
    subprocess.run(cmd)


if __name__ == '__main__':
    recipe_paths, epub_paths, usernames, passwords = get_paths(APP_FOLDER)
    print(recipe_paths)
    print(epub_paths)
    print(usernames)
    print(passwords)
    # fetch_all_news()
    # while True:
        # continue




# epub_folder=$(mktemp -d)/
# epub_path=$epub_folder$epub_name
# epub_path_2=$epub_folder$epub_name_2
# subprocess.run(['ebook-convert', $recipe_path $epub_path --username=$user --password=$pwd --output-profile=kobo
