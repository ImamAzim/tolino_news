from news_loader.views import news_loader_menu


def main():
    pass


def example():
    app = ExampleApp()
    app.start()


class ExampleApp(object):

    """example app"""

    def __init__(self):
        """
        construct the app
        """

        view = ExampleView()
        controller = ExampleController(view)
        view.set_controller(controller)
        self._view = view

    def start(self):
        self._view.start()


if __name__ == '__main__':
    main()
