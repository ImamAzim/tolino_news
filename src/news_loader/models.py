import os


CONFIG_FP = os.path.join(os.path.dirname(__file__), 'config', 'config.toml')

class NewsCreator(object):

    """contains tools to fetch news, merge to an epub and upload it"""

    def __init__(self):
        """TODO: to be defined. """
        pass

    def create_config_file(self):
        """create a config file of news_loader for current user

        """
        pass


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    pass
