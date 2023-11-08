import logging
import sys


from news_loader.models import NewsCreator, NewsLoaderConfiguration


logger = logging.getLogger('news loader')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


class NewsCreatorJob(object):

    """class to start the job to fetch news and upload them"""

    def __init__(self):
        news_loader_configuration = NewsLoaderConfiguration()
        config_dict = news_loader_configuration.load_config()
        self.news_creator = NewsCreator(config_dict)

    def run(self):
        logger.info('run job news loader...')

        logger.info('download news')
        epubs = self.news_creator.download_all_news()

        logger.info('merge epubs')
        merged_epub = self.news_creator.merge_epubs(epubs)

        # logger.info('download comics')
        # images = self.news_creator.download_all_comics()

        # logger.info('create cbz')
        # cbz = self.news_creator.create_cbz_file(images)

        # self.news_creator.clean_webdav()
        # self.news_creator.upload_file(merged_epub)
        # self.news_creator.upload_file(cbz)

        # logger.info('clean data folder')
        # self.news_creator.clean_data_folder()
        
        logger.info('job finished')


def run_news_loader_job():
    job = NewsCreatorJob()
    job.run()


if __name__ == '__main__':
    run_news_loader_job()
