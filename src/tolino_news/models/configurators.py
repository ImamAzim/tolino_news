from pathlib import Path
import tomllib


import xdg_base_dirs
import tomli_w


from tolino_news.models.interfaces import BaseConfigurator
from tolino_news import APP_NAME


DATA_FOLDER = xdg_base_dirs.xdg_data_home() / APP_NAME


class ConfiguratorError(Exception):
    pass


class Configurator(BaseConfigurator):

    _KEY_TITLE = 'epub title'

    def __init__(self, test=False):
        if test:
            config_fn = 'test_config.toml'
        else:
            config_fn = 'config.toml'
        self._config_fp = DATA_FOLDER / config_fn
        self._test = test
        self._config_dict = dict()

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
            username=None,
            password=None):
        self._save_config()

    def save_cloud_credentials(
            self,
            cloud_connector: str,
            credentials: dict,
            ):
        self._save_config()

    def save_epub_title(self, title: str):
        self._config_dict[self._KEY_TITLE] = title
        self._save_config()

    def load_epub_title(self) -> str:
        self._load_config_file()
        return self._config_dict[self._KEY_TITLE]

    def _save_config(self, overwrite=False):
        with open(self._config_fp, 'wb') as f:
            tomli_w.dump(self._config_dict, f)

    def delete_config(self):
        self._config_fp.unlink(missing_ok=True)

    def add_in_crontab(self, hour: int, minute: int):
        pass

    def del_crontab(self):
        pass

    def load_cloud_credentials(
            self,
            ) -> tuple[type, dict]:
        self._load_config_file()

    def load_recipes(
            self,
            ) -> tuple[list[Path], list[str | None], list[str | None]]:
        self._load_config_file()

    def install_epubmerge_plugin(self):
        pass
