import os
import shutil


import xdg


CONFIG_FP = os.path.join(os.path.dirname(__file__), 'config', 'config.toml')

class NewsCreator(object):

    """contains tools to fetch news, merge to an epub and upload it"""

    def __init__(self):
        """TODO: to be defined. """
        pass

    def create_config_file(self, overwrite=False):
        """create a config file of news_loader for current user

        :overwrite: True is you want to overwrite previous config

        """
        directory = os.path.join(xdg.XDG_CONFIG_HOME, 'news_loader')
        if not os.path.exists(directory):
            os.makedirs(directory)

        path = os.path.join(directory, 'config.toml')
        if os.path.exists(path) and not overwrite:
            raise FileExistsError
        else:
            shutil.copy(CONFIG_FP, path)


class NewsLoaderConfiguration(object):

    """class to set configuration of the news loader app"""

    def __init__(self):
        """initiate and create dict config and path to file"""
        self._config_dict = dict()

        directory = os.path.join(xdg.XDG_CONFIG_HOME, 'news_loader')
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.config_fp = os.path.join(directory, 'config.toml')


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    pass
