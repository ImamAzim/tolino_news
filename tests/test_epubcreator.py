import unittest
from pathlib import Path


from tolino_news.models.epub_creators import EpubCreator
from tolino_news import cache_folder

test_recipe_fp = Path(__file__).parent / 'test_recipe.recipe'
test_epub = Path(__file__).parent / 'basic-v3plus2.epub'

class TestEpubCreator(unittest.TestCase):

    """all test concerning EpubCreator calss. """

    @classmethod
    def setUpClass(cls):
        cls._epub_creator = EpubCreator()

    @classmethod
    def tearDownClass(cls):
        cls._epub_creator.clean_cache_folder()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clean_cache(self):
        test_file = cache_folder / 'test'
        test_file.touch()
        self._epub_creator.clean_cache_folder()
        self.assertFalse(test_file.exists())

    def test_download_news(self):
        self._epub_creator.clean_cache_folder()
        epub_fp = self._epub_creator.download_news(test_recipe_fp)
        self.assertTrue(epub_fp.exists())
        self.assertEqual(epub_fp.suffix, '.epub')

    def test_merge_epubs(self):
        self._epub_creator.clean_cache_folder()
        epubs = list((test_epub, test_epub))
        epub_fp = self._epub_creator.merge_epubs('test', epubs)
        self.assertTrue(epub_fp.exists())
        self.assertEqual(epub_fp.suffix, '.epub')
