import getpass


from tolino_news.models.epub_creators import EpubCreator
from tolino_news.models.configurators import Configurator, ConfiguratorError
from tolino_news.models.cloud_connectors import cloud_connectors
from tolino_news.jobs import run_news_loader


class NewsLoaderMenu(object):

    """view in shell with a menu to configure news_loader"""

    def __init__(self):
        self._menu = {
                '0': 'install epubmerge plugin (mandatory before first use)',
                '1': 'add configuration file',
                '2': 'delete configuration file',
                '3': 'test the tolino news now',
                '4': 'add a crontab job to tolino news',
                '5': 'delete crontab job',
                '6': 'show configuration file',
                'q': 'quit',
                }
        self._running = True
        self._configurator = Configurator()
        self._epub_creator = EpubCreator()

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
        self._epub_creator.install_epubmerge_plugin()
        print('===')

    def case_1(self):
        """add configuration file

        """
        # define a name
        epub_name = input('enter name of the epub [news]')
        epub_name = 'news' if not epub_name else epub_name
        # add recipes
        recipes, fp = self.config.get_recipes_names()
        for recipe in recipes:
            print(f'add {recipe}? (y/n) [y]')
            answer = input()
            if not answer.lower() == 'n':
                print('write credentials (or press enter to skip)')
                username = input('username: ')
                if username:
                    password = getpass.getpass()
                    self.config.add_recipe(recipe, username, password)
                else:
                    self.config.add_recipe(recipe)

        # tolino cloud config
        server_name = input('tolino server name [www.buecher.de]:\n')
        server_name = 'www.buecher.de' if not server_name else server_name
        username = input('username:\n')
        password = getpass.getpass()

        self.config.add_tolino_cloud_config(
                server_name,
                username,
                password,
                epub_name)

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
        self._configurator.delete_config()
        print('===')

    def case_3(self):
        """test the tolino news now

        """
        run_news_loader()
        print('===')

    def case_4(self):
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
                    self._configurator.add_in_crontab(hour, minute)
                except ConfiguratorError as e:
                    print(e)
        print('===')

    def case_5(self):
        """delete crontab job

        """
        self._configurator.del_crontab()
        print('cron job deleted. Tolino News will not run daily anymore')
        print('===')

    def case_6(self):
        """show config file

        """
        try:
            print(self._configurator)
        except ConfiguratorError as e:
            print(e)
        print('===')

    def case_q(self):
        """quit

        """
        print('goodbye')
        self._running = False


if __name__ == '__main__':
    pass
