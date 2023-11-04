#!/usr/bin/env python


"""
test models
"""

import unittest


from news_loader.models import NewsCreator


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


def create_config_file():
    news_creator = NewsCreator()
    try:
        news_creator.create_config_file()
    except FileExistsError:
        answer = input(
                'a config file is already present.',
                'do you want to overwrite it with a new one? (y/n) [n]',
                )
        if answer == 'y':
            news_creator.create_config_file(overwrite=True)


if __name__ == '__main__':
    pass
