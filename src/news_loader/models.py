import os
import subprocess
import logging
import datetime
from html.parser import HTMLParser
from urllib.parse import urlparse


import xdg_base_dirs
import tomli_w
import tomli
import feedparser
import requests


CUSTOM_RECIPES_PATH = os.path.join(
        xdg_base_dirs.xdg_config_home(),
        'calibre',
        'custom_recipes',
        )


class RSSParser(HTMLParser):
    """a small rss parser to obtain image link"""
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.image_link=dict(attrs).get('src')


class NewsCreator(object):

    """contains tools to fetch news, merge to an epub and upload it"""

    def __init__(self, config_dict):
        """ store config dict
        :config_dict: from toml config file
        """
        self._config_dict = config_dict
        self._data_path = os.path.join(
                xdg_base_dirs.xdg_data_home(),
                'news_loader'
                )
        if not os.path.exists(self._data_path):
            os.makedirs(self._data_path)

        self._to_delete = list()

    def download_all_news(self):
        """download news for all the recipes and create epub for each
        :returns: list of path to epub just created

        """
        epubs = list()
        for recipe_name, credentials in self._config_dict['recipes'].items():
            recipe_path = os.path.join(
                    CUSTOM_RECIPES_PATH,
                    f'{recipe_name}.recipe',
                    )
            username = credentials.get('username')
            password = credentials.get('password')
            epub_path = self.download_news(
                    recipe_path,
                    recipe_name,
                    username=username,
                    password=password,
                    )
            epubs.append(epub_path)
        return epubs

    def download_news(
            self,
            recipe_path,
            recipe_name,
            username=None,
            password=None,
            supress_output=True):
        """convert a recipe into an epub (fetch news)

        :recipe_path: path to calibre recipe
        :recipe name: name for futur epub
        :username: if required by recipe
        :password: if required by recipe
        :returns: path to epub just created

        """

        epub_path = os.path.join(self._data_path, f'{recipe_name}.epub')

        cmd = [
                'ebook-convert',
                recipe_path, epub_path,
                '--output-profile=kobo',
                ]
        if username is not None:
            cmd += [f'--username={username}']
        if password is not None:
            cmd += [f'--password={password}']
        stdout = open(os.devnull, 'w') if supress_output else None
        subprocess.run(cmd, check=True, stdout=stdout)

        self._to_delete.append(epub_path)

        return epub_path

    def merge_epubs(self, epubs, epub_name=None):
        """merge a list of epubs into one with mergedepub calibre pluginj

        :epubs: list of path to epubs
        :epub_name: str. if None news_DATE will be taken
        :returns: path to newly created merged epub

        """
        if epub_name is None:
            suffix = datetime.date.today().isoformat()
            epub_name = f'news_{suffix}'
        merged_epub = os.path.join(self._data_path, f'{epub_name}.epub')

        cmd = [
                'calibre-debug',
                '--run-plugin',
                'EpubMerge',
                '--',
                f'--title={epub_name}',
                f'--output={merged_epub}',
                ]
        cmd += epubs
        subprocess.run(cmd)
        self._to_delete.append(merged_epub)
        return merged_epub

    def download_all_comics(self):
        """download all comics from the rss feeds in the config file

        :returns: list of image files

        """
        pass

    def download_comics(self, rss_feed: str):
        """
        get image from webcomic rss feeds. it has to parse to find the image link
        :rss_feed: from any webcomics rss with an image
        :returns: path to image file just created

        """
        feed = feedparser.parse(rss_feed)
        comic_summary = feed.entries[0].summary
        parser = RSSParser()
        parser.feed(comic_summary)
        image_link = parser.image_link

        rsp = requests.get(image_link)
        filename = urlparse(rss_feed).netloc
        path = os.path.join(self._data_path, f'{filename}.png')

        with open(path, 'wb') as myfile:
            myfile.write(rsp.content)
        self._to_delete.append(path)

        return path

    def create_cbz_file(self, images):
        """create an archive with images and a cbz extension

        :images: list of path to image files
        :returns: path to cbz file

        """
        pass

    def clean_webdav(self, arg1):
        """TODO: Docstring for clean_webdav.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def upload_files(self, arg1):
        """TODO: Docstring for upload_files.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def clean_data_folder(self):
        """delete all the previous book downloaded or created

        """
        for path in self._to_delete:
            try:
                os.remove(path)
            except FileNotFoundError:
                logging.warning('file to delete has not been found')
        self._to_delete = list()
        pass


class NewsLoaderConfiguration(object):

    """class to set configuration of the news loader app"""

    def __init__(self):
        """initiate and create dict config and path to file"""
        self._config_dict = dict(
                recipes=dict(),
                comics_rss_feeds=list(),
                )

        directory = os.path.join(
                xdg_base_dirs.xdg_config_home(),
                'news_loader',
                )
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.config_fp = os.path.join(directory, 'config.toml')

    def get_recipes_names(self):
        """find present custom recipes in calibre config folder
        :returns: list of recipes names, path to custom_recipe

        """
        folder_path = CUSTOM_RECIPES_PATH
        if not os.path.exists(folder_path):
            return [], folder_path
        else:
            files = os.listdir(folder_path)
            recipes = [
                    filename[0:-len('.recipe')]
                    for filename in files
                    if filename.split('.')[-1] == 'recipe'
                    ]
            return recipes, folder_path

    def add_recipe(self, recipe_name, username=None, password=None):
        """add a recipe to the config dict

        :recipe_name: name that match a custom recipe
        :username: str if required
        :password: str if required

        """
        self._config_dict['recipes'][recipe_name] = dict()
        if username:
            self._config_dict['recipes'][recipe_name]['username'] = username
        if password:
            self._config_dict['recipes'][recipe_name]['password'] = password

    def add_comics_rss(self, rss_link: str):
        """add a rss feed of a comics

        :rss_link: valid url of a feed

        """
        self._config_dict['comics_rss_feeds'].append(rss_link)

    def empty_comics_rss(self):
        self._config_dict['comics_rss_feeds'] = []

    def add_nextcloud_config(self, webdav_link: str):
        """add nextcloud toconfig

        :webdav_link: must be public link

        """
        self._config_dict['webdav_link'] = webdav_link

    def save_config(self, overwrite=False, test=False):
        """save the current config in a toml file

        :overwrite: True if you want to replace previous file
        :test: in test mode return a strin and does not create file
        :returns: None or toml_str if test is True

        """
        if test:
            toml_str = tomli_w.dumps(self._config_dict)
            return toml_str
        else:
            if os.path.exists(self.config_fp) and not overwrite:
                raise FileExistsError
            else:
                with open(self.config_fp, 'wb') as f:
                    tomli_w.dump(self._config_dict, f)

    def delete_config(self):
        """delete toml file

        """
        if os.path.exists(self.config_fp):
            os.remove(self.config_fp)

    def add_crontab(self, arg1):
        """TODO: Docstring for add_crontab.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def del_crontab(self, arg1):
        """TODO: Docstring for del_crontab.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def load_config(self):
        """load toml file present in config user directory
        :returns: tomli_dict from config file

        """
        with open(self.config_fp, 'rb') as f:
            toml_dict = tomli.load(f)
        return toml_dict


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    pass
