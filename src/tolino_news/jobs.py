import logging
import os
import sys
import contextlib


import xdg


from tolino_news.models import NewsCreator, NewsLoaderConfiguration




class NewsCreatorJob(object):

    """class to start the job to fetch news and upload them"""

    def __init__(self):
        news_loader_configuration = NewsLoaderConfiguration()
        config_dict = news_loader_configuration.load_config()
        self.news_creator = NewsCreator(config_dict)

    def run(self):
        logging.info('run job news loader...')

        logging.info('download news')
        epubs = self.news_creator.download_all_news()

        logging.info('merge epubs')
        merged_epub = self.news_creator.merge_epubs(epubs)

        logging.info('register')
        register_device()

        logging.info('clean cloud folder')
        self.news_creator.clean_cloud()

        logging.info('upload news')
        self.news_creator.upload_file(merged_epub)

        logging.info('clean data folder')
        self.news_creator.clean_data_folder()

        logging.info('unregister')
        unregister_device()

        logging.info('job finished')


def run_news_loader_job():
    directory = os.path.join(
            xdg.xdg_state_home(),
            'tolino_news',
            )
    if not os.path.exists(directory):
        os.makedirs(directory)
    logfile = os.path.join(directory, 'log')
    logging.basicConfig(
            filename=logfile,
            encoding='utf-8',
            level=logging.INFO,
            format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
            )
    # logfile = os.path.join(directory, 'errors')
    # with open(filename, 'w') as logfile:
    sys.stderr = open(logfile, 'a')
    job = NewsCreatorJob()
    job.run()
    sys.stderr = sys.__stderr__


def run_news_loader():
    logging.basicConfig(
            encoding='utf-8',
            level=logging.INFO,
            format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
            )
    job = NewsCreatorJob()
    job.run()


def register_device():
    """register the device on the server (do this only once)
    :returns: msg to inform success

    """
    news_loader_configuration = NewsLoaderConfiguration()
    try:
        config_dict = news_loader_configuration.load_config()
    except FileNotFoundError:
        msg = 'file not found! did you create a config files?'
        return msg
    else:
        news_creator = NewsCreator(config_dict)
        msg = news_creator.register_device()
        return msg


def unregister_device():
    """unregister the device on the server (do this only once)
    :returns: msg to inform success

    """
    news_loader_configuration = NewsLoaderConfiguration()
    try:
        config_dict = news_loader_configuration.load_config()
    except FileNotFoundError:
        msg = 'file not found! did you create a config files?'
        return msg
    else:
        news_creator = NewsCreator(config_dict)
        msg = news_creator.unregister_device()
        return msg


if __name__ == '__main__':
    run_news_loader_job()
