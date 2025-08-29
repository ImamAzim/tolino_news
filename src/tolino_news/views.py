import getpass
import inspect


from tolino_news.models.epub_creators import EpubCreator, EpubCreatorError
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
        try:
            self._epub_creator.install_epubmerge_plugin()
        except EpubCreatorError as e:
            print(e)
        print('===')

    def case_1(self):
        """add configuration file

        """
        # epub title
        title = input('enter name of the epub [news]:\n')
        title = 'news' if not title else title
        self._configurator.save_epub_title(title)
        # add recipes
        recipes = self._configurator.get_all_calibre_recipes()
        for recipe in recipes:
            answer = input(f'add {recipe.name}? (y/n) [y]:\n')
            answer = 'y' if not answer else answer
            if answer.lower() == 'y':
                print('give credentials (or press enter to skip)')
                username = input('username: ')
                if username:
                    password = getpass.getpass()
                else:
                    password = ''
                self._configurator.save_recipe(recipe, username, password)

        # cloud config
        print('select a cloud connection:')
        index = 0
        options = dict()
        for cloud_connector, cloud_connector_cls in cloud_connectors.items():
            print(f'[{index}]: {cloud_connector}')
            print(inspect.getdoc(cloud_connector_cls))
            options[str(index)] = cloud_connector
            index += 1
        answer = input(f'[0-{len(cloud_connectors)}]?: ')
        choice = options.get(answer)
        if choice:
            cloud_connector_name = choice
            cloud_connector_cls = cloud_connectors[cloud_connector_name]
            signature = inspect.signature(cloud_connector_cls)
            credentials = dict()
            for arg, param in signature.parameters.items():
                answer = input(f'{arg} [{param.default}]: ')
                answer = answer if answer else param.default
                credentials[arg] = answer
            self._configurator.save_cloud_credentials(
                    cloud_connector_name, credentials)
        else:
            print('invalid choice')
        print('===')

    def case_2(self):
        """delete configuration file

        """
        try:
            self._configurator.delete_config()
        except ConfiguratorError as e:
            print(e)
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
        try:
            self._configurator.del_crontab()
        except ConfiguratorError as e:
            print(e)
        else:
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
