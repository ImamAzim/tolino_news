#!/usr/bin/env python3

import shutil
import subprocess
import os
import logging
import sys
import json
from html.parser import HTMLParser
import datetime
import tempfile


import requests
import xdg
import owncloud
import feedparser
import tomli


logger = logging.getLogger('load news')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

CONFIG_FOLDER = os.path.join(xdg.XDG_CONFIG_HOME, 'news_loader')
if not os.path.exists(CONFIG_FOLDER):
    os.makedirs(CONFIG_FOLDER)
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER, 'config.toml')
# APP_FOLDER = os.path.join(xdg.XDG_CONFIG_HOME, 'calibre', 'news_loader_recipes') # must be the same as in install.sh !!
# if not os.path.exists(APP_FOLDER):
    # os.makedirs(APP_FOLDER)
CUSTOM_RECIPES_PATH = os.path.join(xdg.XDG_CONFIG_HOME, 'calibre', 'custom_recipes')


def fetch_daily_news():

    with open(CONFIG_FILE_PATH, 'rb') as myfile:
        toml_dict = tomli.load(myfile)
    webdav_link = toml_dict['webdav']['link']
    comics_rss_links = toml_dict['comics']['rss_links']


    folder = APP_FOLDER
    recipe_paths = list()
    epub_paths = []
    usernames = []
    passwords = []


    suffix = datetime.date.today().isoformat()
    comic_filepath = os.path.join(CONFIG_FOLDER,  f'comics_{suffix}.cbz')
    merged_epub_path = os.path.join(CONFIG_FOLDER, f'news_{suffix}.epub')

    logger.info('clean local folder...')
    clean_folder(CONFIG_FOLDER)
    logger.info('clean webdav folder...')
    clean_webdav_folder(webdav_link)

    logger.info('start to fetch daily news...')
    epub_to_merge = list()
    for recipe_path, epub_path, username, password in zip(recipe_paths, epub_paths, usernames, passwords):
        answer = fetch_news(recipe_path, epub_path, username, password)
        if answer:
            epub_to_merge.append(epub_path)
    if epub_to_merge:
        logger.info('merge epub...')
        merge_epub(epub_to_merge, merged_epub_path)
        logger.info('upload epub to webdav')
        upload_file(merged_epub_path)
    else:
        logger.info('fail to fetch for every news. I do not merge nor transfer')
    logger.info('create comics')
    create_comics(comics_rss_links, comic_filepath)
    logger.info('transfer comics')
    upload_file(comic_filepath, webdav_link)

    logger.info('all done')

def configure_daily_news():
    print('welcome. this script will configure the daily news daemon for this user.')
    print('TODO: create crontab job')
    dst = CONFIG_FILE_PATH
    src = os.path.join('/etc', 'news_loader', 'config.toml')
    shutil.copy(src, dst)
    print(f'the configuration file has been created in {dst}. you can now customize it.')

def clean_folder(folder):
    #remove old epub and cbz files
    filetypes_to_remove = ('cbz', 'epub')
    files = os.listdir(folder)
    filenames_to_remove = [fn for fn in files if fn.split('.')[-1] in filetypes_to_remove]
    filepaths_to_remove = [os.path.join(folder, filename) for filename in filenames_to_remove]
    for filepath in filepaths_to_remove:
        os.remove(filepath)

def clean_webdav_folder(link):
    oc = owncloud.Client.from_public_link(link)

    files = oc.list('/')
    for remote_file in files:
        filename = remote_file.path
        if 'comics_' in filename or 'news_' in filename:
            oc.delete(filename)

def upload_file(file_path, link):
    oc = owncloud.Client.from_public_link(link)
    oc.drop_file(file_path)


def merge_epub(epub_paths, output_file):
    title = os.path.basename(output_file)
    cmd = [
            'calibre-debug',
            '--run-plugin',
            'EpubMerge',
            '--',
            f'--title={title}',
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

def create_comics(rss_links, output_path):

    with tempfile.TemporaryDirectory() as comic_folder:

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
    with open(CONFIG_FILE_PATH, 'rb') as myfile:
        toml_dict = tomli.load(myfile)

