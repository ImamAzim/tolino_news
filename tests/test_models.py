#!/usr/bin/env python


"""
test models
"""

import unittest
import os
import tomli
import time
import shutil
import tempfile


from tolino_news.models import NewsCreator, NewsLoaderConfiguration


class TestNewsCreator(unittest.TestCase):

    """all test concerning NewsCreator. """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestNewsLoaderConfiguration(unittest.TestCase):

    """all test concerning news loader configuration. """

    @classmethod
    def setUpClass(cls):
        cls.config = NewsLoaderConfiguration()
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_names(self):
        names, folder_path = self.config.get_recipes_names()
        for name in names:
            self.assertTrue(
                    os.path.exists(os.path.join(
                        folder_path, f'{name}.recipe')))

    def test_add_recipe(self):
        self.config.add_recipe('recipe1')
        self.config.add_recipe('recipe2', 'me', 'mypassword')

        recipe_dict = self.config._config_dict['recipes']

        self.assertIn('recipe1', recipe_dict)
        recipe = recipe_dict['recipe1']
        self.assertIsNone(recipe.get('username'))
        self.assertIsNone(recipe.get('password'))

        self.assertIn('recipe2', recipe_dict)
        recipe = recipe_dict['recipe2']
        self.assertEqual(recipe.get('username'), 'me')
        self.assertEqual(recipe.get('password'), 'mypassword')

    def test_add_tolino_cloud_config(self):
        mytolino_config = dict(
                server_name='server name',
                username='me',
                password='secret',
                epub_name='test',
                )
        self.config.add_tolino_cloud_config(**mytolino_config)
        config_dict = self.config._config_dict
        self.assertIn('tolino_cloud_config', config_dict)
        tolino_config = config_dict['tolino_cloud_config']
        self.assertDictEqual(mytolino_config, tolino_config)

    def test_save_config_file(self):
        timestamps = time.time()
        feed_name = str(timestamps)
        self.config.add_comics_rss(feed_name)
        self.config.add_recipe('recipe1')
        self.config.add_recipe('recipe2', 'me', 'mypassword')

        toml_str = self.config.save_config(test=True)
        toml_dict = tomli.loads(toml_str)
        self.assertIn(feed_name, toml_dict['comics_rss_feeds'])

    def test_load_config(self):
        if os.path.exists(self.config.config_fp):
            data = self.config.load_config()
            self.assertIsInstance(data, dict)
        else:
            with self.assertRaises(FileNotFoundError):
                self.config.load_config()


def load_news():
    config = NewsLoaderConfiguration()
    config_dict = config.load_config()
    recipe_path = os.path.join(os.path.dirname(__file__), 'test_recipe.recipe')

    news_creator = NewsCreator(config_dict)

    epub_path = news_creator.download_news(recipe_path, 'test')
    shutil.copy(epub_path, os.environ['HOME'])

    merged_epub = news_creator.merge_epubs([epub_path, epub_path])
    shutil.copy(merged_epub, os.environ['HOME'])

    news_creator.clean_data_folder()
    print('epubs have been created in home folder')


def upload_file():
    config = NewsLoaderConfiguration()
    config_dict = config.load_config()
    news_creator = NewsCreator(config_dict)

    with tempfile.NamedTemporaryFile() as fp:
        news_creator.upload_file(fp.name)


def add_to_crontab():
    config = NewsLoaderConfiguration()
    config.add_in_crontab(8, 10)
    # config.del_crontab()


if __name__ == '__main__':
    add_to_crontab()
