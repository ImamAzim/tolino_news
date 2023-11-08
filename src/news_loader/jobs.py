from news_loader.models import NewsCreator, NewsLoaderConfiguration


class NewsCreatorJob(object):

    """class to start the job to fetch news and upload them"""

    def __init__(self):
        news_loader_configuration = NewsLoaderConfiguration()
        config_dict = news_loader_configuration.load_config()
        self.news_creator = NewsCreator(config_dict)

    def run(self):
        self.news_creator.download_all_news()

        # self.news_creator.clean_data_folder()


def run_news_loader_job():
    job = NewsCreatorJob()
    job.run()


if __name__ == '__main__':
    run_news_loader_job()
