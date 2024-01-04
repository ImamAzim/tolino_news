from tolino_news.views import NewsLoaderMenu


def start_news_loader_menu():
    app = NewsLoaderApp()
    app.start()


class NewsLoaderApp(object):

    """start the app to configure news loader"""

    def __init__(self):
        """
        construct the app
        """

        view = NewsLoaderMenu()
        self._view = view

    def start(self):
        self._view.start()


if __name__ == '__main__':
    start_news_loader_menu()
