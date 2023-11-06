from news_loader.models import NewsCreator


class NewsCreatorJob(object):

    """class to start the job to fetch news and upload them"""

    def __init__(self):
        self.news_creator = NewsCreator()

    def run(self):
        pass


def run_news_loader_job():
    job = NewsCreatorJob()
    job.run()
