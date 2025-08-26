from pathlib import Path


import xdg_base_dirs


from tolino_news.models.interfaces import BaseConfigurator
from tolino_news import APP_NAME


DATA_FOLDER = xdg_base_dirs.xdg_data_home() / APP_NAME


class ConfiguratorError(Exception):
    pass


class Configurator(BaseConfigurator):

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

    def get_all_calibre_recipes(self) -> list[Path]:
        config_home = xdg_base_dirs.xdg_config_home()
        folder_path = config_home / 'calibre' / 'custom_recipes'
        recipes = list()
        if folder_path.exists():
            for fp in folder_path.iterdir():
                if fp.suffix == '.recipe':
                    recipes.append(fp)
        return recipes

    def add_recipe(
            self,
            recipe_fp: Path,
            username=None,
            password=None):
        pass

    def add_cloud_credentials(
            self,
            cloud_connector: str,
            credentials: dict,
            ):
        pass

    def add_epub_title(self, title: str):
        pass

    def load_epub_title(self) -> str:
        self._check_config_file()

    def save_config(self, overwrite=False):
        pass

    def delete_config(self):
        self._config_fp.unlink(missing_ok=True)

    def add_in_crontab(self, hour: int, minute: int):
        pass

    def del_crontab(self):
        pass

    def load_cloud_credentials(
            self,
            ) -> tuple[type, dict]:
        self._check_config_file()

    def get_stored_recipes(
            self,
            ) -> tuple[list[Path], list[str | None], list[str | None]]:
        self._check_config_file()

    def install_epubmerge_plugin(self):
        pass
