import getpass
import inspect


from pytolino.tolino_cloud import Client, PytolinoException

from tolino_news.models.epub_creators import EpubCreator, EpubCreatorError
from tolino_news.models.configurators import Configurator, ConfiguratorError
from tolino_news.models.cloud_connectors import cloud_connectors
from tolino_news.jobs import run_news_loader
from tolino_news import APP_NAME


class NewsLoaderMenu(object):

    """view in shell with a menu to configure news_loader"""

    def __init__(self):
        self._menu = {
                '0': 'install epubmerge plugin (mandatory before first use)',
                '1': 'add access token (necessary for tolino cloud)',
                '2': 'add configuration file',
                '3': 'delete configuration file',
                '4': 'test the tolino news now',
                '5': 'add a crontab job to tolino news',
                '6': 'delete crontab job',
                '7': 'show configuration file',
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
        """add an access token

        """
        default_partner = 'orellfuessli'
        partner = input(f'partner[{default_partner}]:\n')
        partner = partner if partner else default_partner
        client = Client(partner)

        print(f'login on your browser at {partner} and get the token.')
        refresh_token = input('refresh token:\n')
        expires_in = int(input('expires_in:\n'))
        hardware_id = input('hardware id:\n')
        Client.store_token(
                APP_NAME, refresh_token, expires_in, hardware_id)
        try:
            client.get_new_token(APP_NAME)
        except PytolinoException:
            print('failed to get a new access token')
        else:
            print('TODO: create cronjob')
            periodicity = expires_in // 60 - 5
            if periodicity > 0:
                self._configurator.add_token_update_in_crontab(
                        partner,
                        periodicity,
                        )
            else:
                print('expiration time is too short')

        print('===')

    def case_2(self):
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
        answer = input(f'[0-{len(cloud_connectors)-1}]?: ')
        choice = options.get(answer)
        if choice:
            cloud_connector_name = choice
            cloud_connector_cls = cloud_connectors[cloud_connector_name]
            signature = inspect.signature(cloud_connector_cls)
            credentials = dict()
            for arg, param in signature.parameters.items():
                if param.default == param.empty:
                    default_value = ''
                else:
                    default_value = param.default
                answer = input(f'{arg} [{default_value}]: ')
                answer = answer if answer else default_value
                credentials[arg] = answer
            self._configurator.save_cloud_credentials(
                    cloud_connector_name, credentials)
        else:
            print('invalid choice')
        print('===')

    def case_3(self):
        """delete configuration file

        """
        try:
            self._configurator.delete_config()
        except ConfiguratorError as e:
            print(e)
        print('===')

    def case_4(self):
        """test the tolino news now

        """
        run_news_loader()
        print('===')

    def case_5(self):
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

    def case_6(self):
        """delete crontab job

        """
        try:
            self._configurator.del_crontab()
        except ConfiguratorError as e:
            print(e)
        else:
            print('cron job deleted. Tolino News will not run daily anymore')
        print('===')

    def case_7(self):
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
