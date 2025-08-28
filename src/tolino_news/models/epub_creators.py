import subprocess
from pathlib import Path


from tolino_news import PLUGIN_FP
from tolino_news.models.interfaces import BaseEpubCreator


class EpubCreatorError(Exception):
    pass


class EpubCreator(BaseEpubCreator):

    def _check_calibre_installation(self):
        """
        :returns: TODO

        """
        pass

    def _check_epubmergeplugin_installation(self):
        """
        :returns: TODO

        """
        self._check_calibre_installation()

    def download_news(self,
                      recipe_fp: Path,
                      username: None | str = None,
                      password: None | str = None,
                      ) -> Path:
        self._check_calibre_installation()

    def merge_epubs(self, epub_fps: list[Path]) -> Path:
        self._check_epubmergeplugin_installation()

    def clean_cache_folder(self):
        pass

    def install_epubmerge_plugin(self):
        cmd = [
                'calibre-customize',
                '-a',
                f'{PLUGIN_FP}'
                ]
        subprocess.run(cmd)
