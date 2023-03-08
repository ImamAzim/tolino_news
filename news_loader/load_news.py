#!/usr/bin/env python3

import shutil
import subprocess
import os
import logging
import sys
import json
from html.parser import HTMLParser


import requests
import xdg
import owncloud
import feedparser


logger = logging.getLogger('load news')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


APP_FOLDER = os.path.join(xdg.XDG_CONFIG_HOME, 'calibre', 'news_loader_recipes') # must be the same as in install.sh !!
if not os.path.exists(APP_FOLDER):
    os.makedirs(APP_FOLDER)
WEBDAV_FILE_PATH = os.path.join(APP_FOLDER, 'webdav.json')


def fetch_daily_news():

    logger.info('start to fetch daily news...')
    folder = APP_FOLDER
    recipe_paths, epub_paths, usernames, passwords = get_paths(folder)
    comic_filepath = os.path.join(folder, 'daily_comics.cbz')
    merged_epub_path = os.path.join(folder, 'daily_news.epub')
    clean_folder(folder)

    epub_to_merge = list()
    for recipe_path, epub_path, username, password in zip(recipe_paths, epub_paths, usernames, passwords):
        answer = fetch_news(recipe_path, epub_path, username, password)
        if answer:
            epub_to_merge.append(epub_path)
    if epub_to_merge:
        logger.info('merge epub...')
        merge_epub(epub_to_merge, merged_epub_path)
        logger.info('epub merged.')
        logger.info('upload epub to webdav')
        upload_file(merged_epub_path)
        logger.info('file dropped')
    else:
        logger.info('fail to fetch for every news. I do not merge nor transfer')
    logger.info('create comics')
    create_comics(comic_filepath)
    logger.info('transfer comics')
    upload_file(comic_filepath)

    logger.info('all done')

def clean_folder(folder):
    #remove old epub and cbz files
    filetypes_to_remove = ('cbz', 'epub')
    files = os.listdir(folder)
    filenames_to_remove = [fn for fn in files if fn.split('.')[-1] in filetypes_to_remove]
    filepaths_to_remove = [os.path.join(folder, filename) for filename in filenames_to_remove]
    for filepath in filepaths_to_remove:
        os.remove(filepath)

def upload_file(file_path):
    with open(WEBDAV_FILE_PATH, 'r') as myfile:
        webdav = json.load(myfile)
    username = webdav['username']
    link = webdav['link']
    password = webdav['password']

    oc = owncloud.Client.from_public_link(link)
    oc.drop_file(file_path)


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
        logger.info(f'could not fetch news from {recipe_path} ')
        return False

class RSSParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.image_link=dict(attrs).get('src')

def create_comics(output_path):

    rss_links = dict(
            xkcd='https://xkcd.com/rss.xml',
            smbc='https://www.smbc-comics.com/comic/rss',
            )

    comic_folder = os.path.join(APP_FOLDER, 'comics')
    if not os.path.exists(comic_folder):
        os.makedirs(comic_folder)

    for name, rss_link in rss_links.items():
        feed = feedparser.parse(rss_link)
        comic_summary = feed.entries[0].summary
        parser = RSSParser()
        parser.feed(comic_summary)
        image_link = parser.image_link
        rsp = requests.get(image_link)
        path = os.path.join(comic_folder, f'{name}.png')
        with open(path, 'wb') as myfile:
            myfile.write(rsp.content)
    shutil.make_archive(output_path, 'zip', comic_folder)
    shutil.move(f'{output_path}.zip', output_path)


if __name__ == '__main__':
    pass

