#!/usr/bin/env python3

import shutil
import subprocess
import signal
import time
import os
import tempfile
import json


MIN_DELAY = 10 # minimum time between two requests to fetch news. used to avoid multiple udev event
WAIT_TIME = 10
APP_FOLDER = os.path.join('/root', '.config', 'calibre', 'news_loader_recipes') # must be the same as in install.sh !!
if not os.path.exists(APP_FOLDER):
    os.makedirs(APP_FOLDER)
EREADER_MOUNT_POINT = '/mnt/ereader'

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
        fetch_all_news()
    else:
        print('delay to short. do nothing')


def fetch_all_news():
    folder = APP_FOLDER
    recipe_paths, epub_paths, usernames, passwords = get_paths(folder)

    epub_to_merge = list()
    for recipe_path, epub_path, username, password in zip(recipe_paths, epub_paths, usernames, passwords):
        answer = fetch_news(recipe_path, epub_path, username, password)
        if answer:
            epub_to_merge.append(epub_path)
    if epub_to_merge:
        merged_epub_path = os.path.join(APP_FOLDER, 'daily_news.epub')
        print('merge epub...')
        merge_epub(epub_to_merge, merged_epub_path)
        print('epub merged.')
        print('transfer epub...')
        transfer_epub(merged_epub_path)
        print('transfer done')
        print('done!')
    else:
        print('fail to fetch for every news. I do not merge nor transfer')


def transfer_epub(epub_path):
    src = epub_path
    dst = EREADER_MOUNT_POINT
    shutil.copy(src, dst)


def eject_ereader():
    cmd = [
            'ebook-device',
            'eject',
            ]
    subprocess.run(cmd)


def merge_epub(epub_paths, output_file):
    cmd = [
            'calibre-debug',
            '--run-plugin',
            'EpubMerge',
            '--',
            '--title=daily_news',
            f'--output={output_file}',
            ]
    cmd += epub_paths
    subprocess.run(cmd)


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
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f'could not fetch news from {recipe_path} ')
        return False


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, run_script)
    fetch_all_news()
    # while True:
        # continue
