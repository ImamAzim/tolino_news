import os
import subprocess
import logging
import datetime
from html.parser import HTMLParser
from urllib.parse import urlparse
import tempfile
import shutil
import getpass


import xdg
import tomli_w
import tomli
import feedparser
import requests
from varboxes import VarBox
from crontab import CronTab
from pytolino.tolino_cloud import Client, PytolinoException


CUSTOM_RECIPES_PATH = os.path.join(
        xdg.xdg_config_home(),
        'calibre',
        'custom_recipes',
        )

EXEC_PATH = "/usr/local/bin/tolino_news_run" # must be created on install
COLLECTION_NAME = 'news'


class RSSParser(HTMLParser):
    """a small rss parser to obtain image link"""
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.image_link = dict(attrs).get('src')


class NewsCreator(object):

    """contains tools to fetch news, merge to an epub and upload it"""

    def __init__(self, config_dict):
        """ store config dict
        :config_dict: from toml config file
        """
        self._config_dict = config_dict
        self._data_path = os.path.join(
                xdg.xdg_data_home(),
                'tolino_news'
                )
        if not os.path.exists(self._data_path):
            os.makedirs(self._data_path)

        self._to_delete = list()

        self._varbox = VarBox('tolino_news')
        if not hasattr(self._varbox, 'files_online'):
            self._varbox.files_online = list()

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
            if epub_path:
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
        try:
            subprocess.run(cmd, check=True, stdout=stdout)
        except subprocess.CalledProcessError as e:
            print(e)
            return None
        else:
            self._to_delete.append(epub_path)
            return epub_path

    def merge_epubs(self, epubs):
        """merge a list of epubs into one with mergedepub calibre pluginj

        :epubs: list of path to epubs
        :returns: path to newly created merged epub

        """
        epub_name = self._config_dict['tolino_cloud_config']['epub_name']
        suffix = datetime.date.today().isoformat()
        epub_title = f'{epub_name}_{suffix}'
        merged_epub = os.path.join(self._data_path, f'{epub_title}.epub')

        cmd = [
                'calibre-debug',
                '--run-plugin',
                'EpubMerge',
                '--',
                f'--title={epub_title}',
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
        images = list()
        for rss_feed in self._config_dict['comics_rss_feeds']:
            image = self.download_comics(rss_feed)
            images.append(image)
        return images

    def download_comics(self, rss_feed: str):
        """
        get image from webcomic rss feeds. it has to parse to find the
        image link
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

    def create_cbz_file(self, images, cbz_filename=None):
        """create an archive with images and a cbz extension

        :images: list of path to image files
        :returns: path to cbz file

        """
        if cbz_filename is None:
            suffix = datetime.date.today().isoformat()
            cbz_filename = f'comics_{suffix}'
        cbz_path = os.path.join(self._data_path, cbz_filename)

        with tempfile.TemporaryDirectory() as comic_folder:
            for image in images:
                shutil.copy(image, comic_folder)
            shutil.make_archive(cbz_path, 'zip', comic_folder)
        cbz_path_with_ext = f'{cbz_path}.cbz'
        shutil.move(f'{cbz_path}.zip', cbz_path_with_ext)
        self._to_delete.append(cbz_path_with_ext)

        return cbz_path_with_ext

    def clean_cloud(self):
        """remove all files previousely uploaded

        """
        server_name =self._config_dict['tolino_cloud_config']['server_name']
        username =self._config_dict['tolino_cloud_config']['username']
        password =self._config_dict['tolino_cloud_config']['password']
        client = Client(server_name)
        try:
            client.login(username, password)
        except PytolinoException:
            logging.warning('failed to login before file deletion')
        else:
            for ebook_id in self._varbox.files_online:
                try:
                    client.delete_ebook(ebook_id)
                except PytolinoException:
                    logging.warning('failed to delete some files because of a pytolino exception')
            try:
                client.logout()
            except PytolinoException:
                logging.warning('failed to logout')
            finally:
                self._varbox.files_online = list()

    def upload_file(self, file_path):
        """upload a file to the cloud

        :file_path: str

        """

        server_name =self._config_dict['tolino_cloud_config']['server_name']
        username =self._config_dict['tolino_cloud_config']['username']
        password =self._config_dict['tolino_cloud_config']['password']
        try:
            client = Client(server_name)
            client.login(username, password)
            ebook_id = client.upload(file_path)
            client.add_to_collection(ebook_id, COLLECTION_NAME)
            client.logout()
        except PytolinoException:
            logging.warning('failed to upload file because of a pytolino exception')
        else:
            files_online = self._varbox.files_online
            files_online.append(ebook_id)
            self._varbox.files_online = files_online

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

    def register_device(self):
        """register device on server
        :return: msg of success or failure

        """
        server_name =self._config_dict['tolino_cloud_config']['server_name']
        username =self._config_dict['tolino_cloud_config']['username']
        password =self._config_dict['tolino_cloud_config']['password']
        try:
            client = Client(server_name)
            client.login(username, password)
            client.register()
            client.logout()
        except PytolinoException:
            msg = 'registration failed'
            return msg
        else:
            msg = 'registered!'
            return msg

    def unregister_device(self):
        """unregister device on server
        :return: msg of success or failure

        """
        server_name =self._config_dict['tolino_cloud_config']['server_name']
        username =self._config_dict['tolino_cloud_config']['username']
        password =self._config_dict['tolino_cloud_config']['password']
        try:
            client = Client(server_name)
            client.login(username, password)
            client.unregister()
            client.logout()
        except PytolinoException:
            msg = 'unregistration failed'
            return msg
        else:
            msg = 'unregistered!'
            return msg


class NewsLoaderConfiguration(object):

    """class to set configuration of the news loader app"""

    def __init__(self):
        """initiate and create dict config and path to file"""
        self._config_dict = dict(
                recipes=dict(),
                comics_rss_feeds=list(),
                tolino_cloud_config=dict(),
                )

        directory = os.path.join(
                xdg.xdg_config_home(),
                'tolino_news',
                )
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.config_fp = os.path.join(directory, 'config.toml')
        self._cronjob_id = 'tolino news'

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

    def add_tolino_cloud_config(self, server_name: str, username: str, password: str, epub_name: str):
        """add tolino cloud credentials and server in config

        :server_name: must be accepted by pytolino client (ex:www.buecher.de)
        :username: from mytolino
        :password: from mytolino
        :epub_name: title of the merged epub

        """
        tolino_config = self._config_dict['tolino_cloud_config']
        tolino_config['server_name'] = server_name
        tolino_config['username'] = username
        tolino_config['password'] = password
        tolino_config['epub_name'] = epub_name

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


    def add_in_crontab(self, hour: int, minute: int):
        """add the news loader job in user crontab

        :hour: time at which job is run
        :minute: time at which job is run

        """
        cron = CronTab(user=getpass.getuser())
        if [el for el in cron.find_comment(self._cronjob_id)]:
            raise FileExistsError
        tmp_file = f'/tmp/tolino_news_log_{getpass.getuser()}'
        job = cron.new(command=f'{EXEC_PATH} > {tmp_file} 2>&1', comment=self._cronjob_id)
        job.hour.on(hour)
        job.minute.on(minute)

        cron.write()


    def del_crontab(self):
        """delete the news loader job in the crontab


        """
        cron = CronTab(user=getpass.getuser())
        cron.remove_all(comment=self._cronjob_id)
        cron.write()


    def load_config(self):
        """load toml file present in config user directory
        :returns: tomli_dict from config file

        """
        with open(self.config_fp, 'rb') as f:
            toml_dict = tomli.load(f)
        return toml_dict

    def install_epubmerge_plugin(self):
        """use calibre customize to install zip file

        """
        filename = 'EpubMerge.zip'
        plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        path = os.path.join(plugin_dir, filename)

        cmd = [
                'calibre-customize',
                '-a',
                f'{path}'
                ]
        subprocess.run(cmd)


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    pass
