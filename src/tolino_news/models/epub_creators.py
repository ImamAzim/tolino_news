import subprocess
import shutil
from pathlib import Path


from tolino_news import PLUGIN_FP, cache_folder
from tolino_news.models.interfaces import BaseEpubCreator


class EpubCreatorError(Exception):
    pass


class EpubCreator(BaseEpubCreator):

    _CALIBRE_ENTRY = 'calibre'
    _CALIBRE_CUSTOMIZE = 'calibre-customize'
    _EBOOK_CONVERT = 'ebook-convert'

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
        output_fp = cache_folder / f'{recipe_fp.stem}.epub'
        cmd = [
                self._EBOOK_CONVERT,
                recipe_fp,
                output_fp,
                '--output-profile=kobo',
                ]
        if username is not None:
            cmd.append(f'--username={username}')
        if password is not None:
            cmd.append(f'--password={password}')
        # stdout = open(os.devnull, 'w') if supress_output else None
        stdout = None
        try:
            subprocess.run(cmd, stdout=stdout)
        except FileNotFoundError as e:
            print(e)
            raise EpubCreator('failed to convert recipe.is calibre installed?')
        else:
            return output_fp

    def merge_epubs(self, epub_fps: list[Path]) -> Path:
        pass

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
    # ec = EpubCreator()
    # ec._check_calibre_installation()
