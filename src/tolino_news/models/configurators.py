from pathlib import Path


import xdg_base_dirs


from tolino_news.models.interfaces import BaseConfigurator


class Configurator(BaseConfigurator):

    def __init__(self, test=False):
        self._test = test
        self._config_dict = dict()

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
        pass

    def save_config(self, overwrite=False):
        pass

    def delete_config(self):
        pass

    def add_in_crontab(self, hour: int, minute: int):
        pass

    def del_crontab(self):
        pass

    def load_cloud_credentials(
            self,
            ) -> tuple[type, dict]:
        pass

    def get_stored_recipes(
            self,
            ) -> tuple[list[Path], list[str | None], list[str | None]]:
        pass

    def install_epubmerge_plugin(self):
        pass
