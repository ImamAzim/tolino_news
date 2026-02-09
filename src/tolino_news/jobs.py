import logging
import sys
import argparse


from varboxes import VarBox
from pytolino.tolino_cloud import Client, PytolinoException


from tolino_news.models.configurators import Configurator
from tolino_news.models.epub_creators import EpubCreator, EpubCreatorError
from tolino_news.models.cloud_connectors import CloudConnectorException
from tolino_news.models import interfaces
from tolino_news import APP_NAME, LOG_FP, LOG_TOKEN


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
        self._varbox = varbox

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
                if self._varbox.last_uploaded_file:
                    logging.info('delete last uploaded file')
                    try:
                        cc.delete_file(self._varbox.last_uploaded_file)
                    except CloudConnectorException as e:
                        print(e)
                logging.info('upload news')
                try:
                    epub_id = cc.upload(merged_epub_fp)
                except CloudConnectorException as e:
                    print(e)
                    self._varbox.last_uploaded_file = None
                else:
                    self._varbox.last_uploaded_file = epub_id
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


def get_new_token_job():
    """get a new access token from refresh token. intended to be called
    by crontab every hours

    """
    parser = argparse.ArgumentParser(
            prog='token updater',
            description='get a new access token',
            )

    parser.add_argument('-p', '--partner', help='name of tolino partner')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='ouput in stdout and info log level')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
                encoding='utf-8',
                level=logging.INFO,
                format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
                datefmt="%Y.%m.%d %H:%M:%S",
                )
    else:
        logging.basicConfig(
                level=logging.INFO,
                filename=LOG_TOKEN,
                encoding='utf-8',
                format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
                datefmt="%Y.%m.%d %H:%M:%S",
                )
        sys.stderr = open(LOG_TOKEN, 'a')

    partner = args.partner
    logging.info('get a new acess token...')

    client = Client(partner)
    try:
        client.get_new_token(APP_NAME)
    except PytolinoException as e:
        logging.error(e)
        logging.error('failed to get a new access token')
    finally:
        if not args.verbose:
            sys.stderr = sys.__stderr__


if __name__ == '__main__':
    run_news_loader()
