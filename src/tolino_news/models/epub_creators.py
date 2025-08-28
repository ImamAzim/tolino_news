from tolino_news.models.interfaces import BaseEpubCreator


class EpubCreator(BaseEpubCreator):

    def install_epubmerge_plugin(self):
        pass

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
