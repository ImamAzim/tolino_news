import getpass

from tolino_news.models import NewsLoaderConfiguration
from tolino_news.jobs import run_news_loader, register_device

class NewsLoaderMenu(object):

    """view in shell with a menu to configure news_loader"""

    def __init__(self):
        self._menu = {
                '0': 'install epubmerge plugin (mandatory before first use)',
                '1': 'add configuration file',
                '2': 'delete configuration file',
                '3': 'register device (necessary to do it once before first use)',
                '4': 'unregister device',
                '5': 'test the tolino news now',
                '6': 'add a crontab job to tolino news',
                '7': 'delete crontab job',
                '8': 'show configuration file',
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
                'welcome to the tolino news menu'
                )
        print('===')

    def _print_menu(self):
        for key, value in self._menu.items():
            print(key, value)
        print('===')

    def case_0(self):
        """install epubmerge plugin

        """
        self.config.install_epubmerge_plugin()
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

        #tolino cloud config
        server_name =input('tolino server name [www.buecher.de]:\n')
        server_name = 'www.buecher.de' if not server_name else server_name
        username = input('username:\n')
        password = getpass.getpass()

        self.config.add_tolino_cloud_config(server_name, username, password)

        # create config file

        try:
            self.config.save_config()
        except FileExistsError:
            answer = input(
                    'a config file is already present.'
                    'do you want to overwrite it with a new one? (y/n) [n]',
                    )
            if answer.lower() == 'y':
                self.config.save_config(overwrite=True)
        print('===')

    def case_2(self):
        """delete configuration file

        """
        self.config.delete_config()
        print('===')

    def case_3(self):
        """register device

        """
        msg = register_device()
        print(msg)
        print('===')

    def case_4(self):
        """unregister device

        """
        print('===')

    def case_5(self):
        """test the tolino news now

        """
        run_news_loader()
        print('===')

    def case_6(self):
        """add crontab job

        """
        hour_str = input('hours=')
        try:
            hour = int(hour_str)
        except ValueError:
            print('invalid hour')
        else:
            min_str = input('minutes=')
            try:
                minute = int(min_str)
            except ValueError:
                print('invalid minutes')
            else:
                try:
                    self.config.add_in_crontab(hour, minute)
                except FileExistsError:
                    print('there is already such cron job. please delete it first.')

        print('===')

    def case_7(self):
        """delete crontab job

        """
        self.config.del_crontab()
        print('cron job deleted. Tolino News will not run daily anymore')
        print('===')

    def case_8(self):
        """show config file

        """
        try:
            config_dict = self.config.load_config()
        except FileNotFoundError:
            print('file not found! did you create a config files?')
        else:
            print(config_dict)
        print('===')

    def case_q(self):
        """quit

        """
        print('goodbye')
        self._running = False


if __name__ == '__main__':
    pass
