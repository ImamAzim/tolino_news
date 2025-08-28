import subprocess
import shutil
from pathlib import Path


from tolino_news import PLUGIN_FP
from tolino_news.models.interfaces import BaseEpubCreator


class EpubCreatorError(Exception):
    pass


class EpubCreator(BaseEpubCreator):

    _CALIBRE_ENTRY = 'calibre'
    _CALIBRE_CUSTOMIZE = 'calibre-customize'

    def _check_calibre_installation(self):
        """
        :returns: TODO

        """
        fp = shutil.which(self._CALIBRE_ENTRY)
        if fp is None:
            raise EpubCreatorError('calibre is not installed')

    def download_news(self,
                      recipe_fp: Path,
                      username: None | str = None,
                      password: None | str = None,
                      ) -> Path:
        pass

    def merge_epubs(self, epub_fps: list[Path]) -> Path:
        pass

    def clean_cache_folder(self):
        pass

    def install_epubmerge_plugin(self):
        self._check_calibre_installation()
        cmd = [
                'calibre-customize',
                '-a',
                f'{PLUGIN_FP}'
                ]
        subprocess.run(cmd)


if __name__ == '__main__':
    ec = EpubCreator()
    ec._check_calibre_installation()
