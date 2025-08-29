import subprocess
import shutil
from pathlib import Path
import datetime


from tolino_news import PLUGIN_FP, cache_folder
from tolino_news.models.interfaces import BaseEpubCreator


class EpubCreatorError(Exception):
    pass


class EpubCreator(BaseEpubCreator):

    _CALIBRE_ENTRY = 'calibre'
    _CALIBRE_CUSTOMIZE = 'calibre-customize'
    _CALIBRE_DEBUG = 'calibre-debug'
    _EBOOK_CONVERT = 'ebook-convert'
    _EPUB_MERGE = 'EpubMerge'

    def _check_calibre_installation(self):
        """
        :returns: TODO

        """
        fp = shutil.which(self._CALIBRE_ENTRY)
        if fp is None:
            raise EpubCreatorError('calibre is not installed')

    def download_news(self,
                      recipe_fp: Path,
                      username: str = '',
                      password: str = '',
                      ) -> Path:
        output_fp = cache_folder / f'{recipe_fp.stem}.epub'
        cmd = [
                self._EBOOK_CONVERT,
                recipe_fp,
                output_fp,
                '--output-profile=kobo',
                ]
        if username:
            cmd.append(f'--username={username}')
        if password:
            cmd.append(f'--password={password}')
        try:
            subprocess.run(cmd)
        except FileNotFoundError as e:
            print(e)
            raise EpubCreator('failed to convert recipe.is calibre installed?')
        else:
            return output_fp

    def merge_epubs(
            self,
            title: str,
            epub_fps: list[Path],
            ) -> Path:

        date = datetime.date.today().isoformat()
        dated_title = f'{title}_{date}'
        output_fp = cache_folder / f'{dated_title}.epub'

        cmd = [
                self._CALIBRE_DEBUG,
                '--run-plugin',
                self._EPUB_MERGE,
                '--',
                f'--title={dated_title}',
                f'--output={output_fp}',
                ]
        cmd += epub_fps
        try:
            subprocess.run(cmd)
        except FileNotFoundError as e:
            print(e)
            raise EpubCreator('failed to convert recipe.is calibre installed?')
        else:
            return output_fp

    def clean_cache_folder(self):
        for child in cache_folder.iterdir():
            if child.is_file():
                child.unlink()
            else:
                shutil.rmtree(child)

    def install_epubmerge_plugin(self):
        self._check_calibre_installation()
        cmd = [
                'calibre-customize',
                '-a',
                f'{PLUGIN_FP}'
                ]
        subprocess.run(cmd)


if __name__ == '__main__':
    pass
    # ec = EpubCreator()
    # ec._check_calibre_installation()
