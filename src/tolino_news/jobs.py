import logging
import sys


from varboxes import VarBox


from tolino_news.models.cloud_connectors import CloudConnectorException
from tolino_news.models.configurators import Configurator, ConfiguratorError
from tolino_news.models.epub_creators import EpubCreator, EpubCreatorError
from tolino_news.models import interfaces
from tolino_news import APP_NAME


class NewsCreatorJob(object):

    """class to start the job to fetch news and upload them"""

    def __init__(self):
        config = Configurator()
        resp = config.load_cloud_credentials()
        cloud_connector_cls, cloud_credentials = resp
        cloud_connector: interfaces.CloudConnector = cloud_connector_cls(
                **cloud_credentials)
        epub_creator = EpubCreator()
        varbox = VarBox(APP_NAME, cloud_connector_cls.__name__)

        self._configurator = config
        self._cloud_connector = cloud_connector
        self._epub_creator = epub_creator

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


# def run_news_loader_job():
    # directory = os.path.join(
            # xdg.xdg_state_home(),
            # 'tolino_news',
            # )
    # if not os.path.exists(directory):
        # os.makedirs(directory)
    # logfile = os.path.join(directory, 'log')
    # logging.basicConfig(
            # filename=logfile,
            # encoding='utf-8',
            # level=logging.INFO,
            # format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            # datefmt="%Y.%m.%d %H:%M:%S",
            # )
    # # logfile = os.path.join(directory, 'errors')
    # # with open(filename, 'w') as logfile:
    # sys.stderr = open(logfile, 'a')
    # job = NewsCreatorJob()
    # job.run()
    # sys.stderr = sys.__stderr__


def run_news_loader():
    logging.basicConfig(
            encoding='utf-8',
            level=logging.INFO,
            format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
            )
    job = NewsCreatorJob()
    job.run()


if __name__ == '__main__':
    run_news_loader()
