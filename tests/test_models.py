#!/usr/bin/env python


"""
test models
"""

import unittest
import os


from news_loader.models import NewsCreator, NewsLoaderConfiguration


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
            self.assertTrue(os.path.exists(os.path.join(folder_path, f'{name}.recipe')))

    def test_add_recipe(self):
        self.config.add_recipe('recipe1')
        self.config.add_recipe('recipe2', 'me', 'mypassword')

        recipe_dict = self.config._config_dict

        self.assertIn('recipe1', recipe_dict)
        recipe = recipe_dict['recipe1']
        self.assertIsNone(recipe.get('username'))
        self.assertIsNone(recipe.get('password'))

        self.assertIn('recipe2', recipe_dict)
        recipe = recipe_dict['recipe2']
        self.assertEqual(recipe.get('username'), 'me')
        self.assertEqual(recipe.get('password'), 'mypassword')


def create_config_file():
    news_creator = NewsCreator()
    try:
        news_creator.create_config_file()
    except FileExistsError:
        answer = input(
                'a config file is already present.'
                'do you want to overwrite it with a new one? (y/n) [n]',
                )
        if answer == 'y':
            news_creator.create_config_file(overwrite=True)


if __name__ == '__main__':
    create_config_file()
