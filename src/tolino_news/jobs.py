import logging
import sys


from varboxes import VarBox


from tolino_news.models.configurators import Configurator
from tolino_news.models.epub_creators import EpubCreator, EpubCreatorError
from tolino_news.models import interfaces
from tolino_news import APP_NAME, LOG_FP


class NewsCreatorJob(object):

    """class to start the job to fetch news and upload them"""

    def __init__(self):
        config = Configurator()
        resp = config.load_cloud_credentials()
        cloud_connector_cls, cloud_credentials = resp
        epub_creator = EpubCreator()
        varbox = VarBox(APP_NAME, cloud_connector_cls.__name__)

        self._configurator = config
        self._cloud_connector_cls = cloud_connector_cls
        self._cloud_credentials = cloud_credentials
        self._epub_creator = epub_creator
        if not hasattr(varbox, 'last_uploaded_file'):
            varbox.last_uploaded_file = None
        self._last_uploaded_file = varbox.last_uploaded_file

    def run(self):
        logging.info('run job news loader...')

        logging.info('clean cache')
        self._epub_creator.clean_cache_folder()

        logging.info('download news')
        recipe_fps, usernames, passwords = self._configurator.load_recipes()
        epub_fps = list()
        for recipe_fp, username, password in zip(
                recipe_fps, usernames, passwords):
            try:
                epub_fp = self._epub_creator.download_news(
                        recipe_fp, username, password)
            except EpubCreatorError as e:
                print(e)
            else:
                epub_fps.append(epub_fp)
        if not epub_fps:
            print('no news to upload!')
        else:
            logging.info('merge epubs')
            title = self._configurator.load_epub_title()
            merged_epub_fp = self._epub_creator.merge_epubs(title, epub_fps)

            with self._cloud_connector_cls(**self._cloud_credentials) as cc:
                cc: interfaces.CloudConnector
                if self._last_uploaded_file:
                    logging.info('delete last uploaded file')
                    cc.delete_file(self._last_uploaded_file)
                logging.info('upload news')
                epub_id = cc.upload(merged_epub_fp)
                self._last_uploaded_file = epub_id
            logging.info('job finished')


def run_news_loader_job():
    logging.basicConfig(
            filename=LOG_FP,
            encoding='utf-8',
            level=logging.INFO,
            format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
            )
    sys.stderr = open(LOG_FP, 'a')
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


if __name__ == '__main__':
    run_news_loader()
