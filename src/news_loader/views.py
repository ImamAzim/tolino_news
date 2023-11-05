import getpass

from news_loader.models import NewsLoaderConfiguration

class NewsLoaderMenu(object):

    """view in shell with a menu to configure news_loader"""

    def __init__(self):
        self._menu = {
                '1': 'add configuration file',
                '2': 'delete configuration file',
                '3': 'test the news loader now',
                '4': 'add a crontab job to load news',
                '5': 'delete crontab job',
                'q': 'quit',
                }
        self._running = True
        self.config = NewsLoaderConfiguration()

    def start(self):
        self._print_welcome()
        while self._running:
            self._print_menu()
            choice = input('please select:\n')
            try:
                getattr(self, f'case_{choice}')()
            except AttributeError:
                print('please select a valid option')

    def _print_welcome(self):
        print(
                'welcome to the news loader menu'
                )
        print('===')

    def _print_menu(self):
        for key, value in self._menu.items():
            print(key, value)
        print('===')

    def case_1(self):
        """add configuration file

        """
        # add recipes
        recipes, fp = self.config.get_recipes_names()
        for recipe in recipes:
            print(f'add {recipe}? (y/n) [y]')
            answer = input()
            if not answer.lower()=='n':
                print('write credentials (or press enter to skip)')
                username = input('username: ')
                if username:
                    password = getpass.getpass()
                    self.config.add_recipe(recipe, username, password)
                else:
                    self.config.add_recipe(recipe)

        # add rss
        self.config.empty_comics_rss()
        print('enter rss feeds links of comics')
        answer = True
        while answer:
            answer = input('new rss (or enter to skip): ')
            if answer:
                self.config.add_comics_rss(answer)

        print('===')

    def case_2(self):
        """delete configuration file

        """
        print('you have chosen option 2')
        print('===')

    def case_3(self):
        """test the news loader now

        """
        print('you have chosen option 3')
        print('===')

    def case_4(self):
        """add crontab job

        """
        print('you have chosen option 4')
        print('===')

    def case_5(self):
        """delete crontab job

        """
        print('you have chosen option 5')
        print('===')

    def case_q(self):
        """quit

        """
        print('goodbye')
        self._running = False


if __name__ == '__main__':
    pass
