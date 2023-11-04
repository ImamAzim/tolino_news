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

        path = os.path.join(xdg.XDG_CONFIG_HOME, 'news_loader', 'config.toml')
        if os.path.exists(path) and not overwrite:
            raise FileExistsError
        else:
            shutil.copy(CONFIG_FP, path)


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    pass
