import os
import time


import xdg
import tomli_w



CUSTOM_RECIPES_PATH = os.path.join(xdg.XDG_CONFIG_HOME, 'calibre', 'custom_recipes')


class NewsCreator(object):

    """contains tools to fetch news, merge to an epub and upload it"""

    def __init__(self):
        """TODO: to be defined. """
        pass

    def download_news(self):
        """download news for all the recipes and create epub for each
        :returns: TODO

        """
        pass


class NewsLoaderConfiguration(object):

    """class to set configuration of the news loader app"""

    def __init__(self):
        """initiate and create dict config and path to file"""
        self._config_dict = dict(
                recipes=dict(),
                comics_rss_feeds=list(),
                )

        directory = os.path.join(xdg.XDG_CONFIG_HOME, 'news_loader')
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
                    for filename in files if filename.split('.')[-1] == 'recipe']
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


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    pass
