from pathlib import Path


from tolino_news.models.interfaces import BaseConfigurator


class Configurator(BaseConfigurator):

    def __init__(self):
        pass

    def get_all_calibre_recipes(self) -> Path:
        pass

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

    def save_config(self, overwrite=False, test=False):
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

    def install_epubmerge_plugin(self):
        pass
