from pathlib import Path
import tomllib
import getpass


import xdg_base_dirs
import tomli_w
from crontab import CronTab


from tolino_news.models.interfaces import BaseConfigurator
from tolino_news import APP_NAME, LOG_FP, RUNJOB_FP, DATA_FOLDER
from tolino_news import TOKEN_UPDATE_RUNJOB_FP, LOG_TOKEN
from tolino_news.models.cloud_connectors import cloud_connectors


class ConfiguratorError(Exception):
    pass


class Configurator(BaseConfigurator):

    _KEY_TITLE = 'epub title'
    _KEY_CLOUD_CREDENTIALS = 'cloud credentials'
    _KEY_CLOUD_CONNECTOR = 'cloud connector'
    _KEY_RECIPES = 'recipes'
    _KEY_USERNAME = 'username'
    _KEY_PASSWORD = 'password'
    _KEY_FP = 'file path'
    _TOKEN_UPDATE_COMMENT = ' update access token'

    def __init__(self, test=False):
        if test:
            config_fn = 'test_config.toml'
        else:
            config_fn = 'config.toml'
        self._config_fp = DATA_FOLDER / config_fn
        self._test = test
        self._config_dict = dict()
        self._config_dict[self._KEY_RECIPES] = dict()

    def __repr__(self):
        """load config from toml file and return dict
        :returns: configuration

        """
        self._load_config_file()
        return repr(self._config_dict)

    def _check_config_file(self):
        """

        """
        if not self._config_fp.exists():
            raise ConfiguratorError('config file not present')

    def _load_config_file(self):
        """
        """
        self._check_config_file()
        with open(self._config_fp, 'rb') as f:
            data = tomllib.load(f)
        self._config_dict.update(data)

    def get_all_calibre_recipes(self) -> list[Path]:
        config_home = xdg_base_dirs.xdg_config_home()
        folder_path = config_home / 'calibre' / 'custom_recipes'
        recipes = list()
        if folder_path.exists():
            for fp in folder_path.iterdir():
                if fp.suffix == '.recipe':
                    recipes.append(fp)
        return recipes

    def save_recipe(
            self,
            recipe_fp: Path,
            username='',
            password=''):
        recipes: dict = self._config_dict[self._KEY_RECIPES]
        recipe = dict()
        recipe[self._KEY_USERNAME] = username
        recipe[self._KEY_PASSWORD] = password
        recipe[self._KEY_FP] = recipe_fp.as_posix()
        recipe_name = recipe_fp.name
        recipes[recipe_name] = recipe
        self._save_config()

    def save_cloud_credentials(
            self,
            cloud_connector: str,
            credentials: dict,
            ):
        self._config_dict[self._KEY_CLOUD_CONNECTOR] = cloud_connector
        self._config_dict[self._KEY_CLOUD_CREDENTIALS] = credentials
        self._save_config()

    def save_epub_title(self, title: str):
        self._config_dict[self._KEY_TITLE] = title
        self._save_config()

    def load_epub_title(self) -> str:
        self._load_config_file()
        title = self._config_dict.get(self._KEY_TITLE)
        return title

    def _save_config(self, overwrite=False):
        with open(self._config_fp, 'wb') as f:
            tomli_w.dump(self._config_dict, f)

    def delete_config(self):
        self._config_fp.unlink(missing_ok=True)

    def add_in_crontab(self, hour: int, minute: int):
        cron = CronTab(user=getpass.getuser())
        if [el for el in cron.find_comment(APP_NAME)]:
            raise ConfiguratorError('there is already a crontab job')

        job = cron.new(
                command=f'{RUNJOB_FP} > {LOG_FP} 2>&1',
                comment=APP_NAME)
        job.hour.on(hour)
        job.minute.on(minute)
        cron.write()

    def add_token_update_in_crontab(
            self,
            partner: str,
            periodicity: int,
            ):
        cron = CronTab(user=getpass.getuser())
        comment = APP_NAME + self._TOKEN_UPDATE_COMMENT
        cron.remove_all(comment=comment)

        command = f'{TOKEN_UPDATE_RUNJOB_FP} -p {partner} >> {LOG_TOKEN} 2>&1'
        job = cron.new(
                command=command,
                comment=comment)
        job.minute.every(periodicity)
        cron.write()

    def del_crontab(self):
        cron = CronTab(user=getpass.getuser())
        cron.remove_all(comment=APP_NAME)
        comment = APP_NAME + self._TOKEN_UPDATE_COMMENT
        cron.remove_all(comment=comment)
        cron.write()

    def load_cloud_credentials(
            self,
            ) -> tuple[type, dict]:
        self._load_config_file()
        credentials = self._config_dict.get(self._KEY_CLOUD_CREDENTIALS)
        connector_name = self._config_dict.get(self._KEY_CLOUD_CONNECTOR)
        connector_cls = cloud_connectors.get(connector_name)
        return connector_cls, credentials

    def load_recipes(
            self,
            ) -> tuple[list[Path], list[str], list[str]]:
        self._load_config_file()
        recipes: dict = self._config_dict[self._KEY_RECIPES]
        fps = list()
        usernames = list()
        passwords = list()
        recipe: dict
        for recipe in recipes.values():
            fp = Path(recipe.get(self._KEY_FP))
            username = recipe.get(self._KEY_USERNAME)
            password = recipe.get(self._KEY_PASSWORD)
            fps.append(fp)
            usernames.append(username)
            passwords.append(password)
        return fps, usernames, passwords
