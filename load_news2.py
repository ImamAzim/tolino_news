#!/usr/bin/env python3

import subprocess
import signal
import time
import os
import tempfile


MIN_DELAY = 10 # minimum time between two requests to fetch news. used to avoid multiple udev event
WAIT_TIME = 10
RECIPE_FOLDER = os.path.join(os.environ['HOME'], '.config', 'calibre', 'custom_recipes')
EPUB_FOLDER = os.path.join(os.environ['HOME'], '.config', 'calibre', 'to_transfer')
if not os.path.exists(EPUB_FOLDER):
    os.makedirs(EPUB_FOLDER)

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
    recipe_names = ['rts_info', 'reveil', 'comics' ]
    recipe_paths, epub_paths = get_paths(recipe_names)

    passwords = [None, None, None]
    usernames = [None, 'imam.usmani@sfr.fr', None]

    epub_names = [f'{i}.epub' for i in range(len(recipe_names))]
    for recipe_path, epub_path, username, password in zip(recipe_paths, epub_paths, usernames, passwords):
        fetch_news(recipe_path, epub_path)

def get_paths(epub_names):
    recipe_paths = [os.path.join(RECIPE_FOLDER, recipe_name) for recipe_name in recipe_names]
    epub_paths = [os.path.join(EPUB_FOLDER, epub_name) for epub_name in epub_names]
    return recipe_paths, epub_paths


def fetch_news(recipe_path, epub_path, username=None, password=None):
    cmd = ['ebook-convert', recipe_path, epub_path, '--output-profile=kobo']
    if username is not None:
        cmd += [f'--username={username}']
    if password is not None:
        cmd += [f'--password={password}']
    subprocess.run(cmd)


if __name__ == '__main__':
    fetch_all_news()
    # while True:
        # continue




# epub_folder=$(mktemp -d)/
# epub_path=$epub_folder$epub_name
# epub_path_2=$epub_folder$epub_name_2
# subprocess.run(['ebook-convert', $recipe_path $epub_path --username=$user --password=$pwd --output-profile=kobo
