import unittest
import warnings
import inspect
from pathlib import Path
import subprocess


from tolino_news.models.configurators import Configurator, ConfiguratorError
from tolino_news.models.cloud_connectors import TolinoCloudConnector


TEST_RECIPE_FN = 'test_recipe.recipe'


class TestConfigurator(unittest.TestCase):

    """all test concerning configurator. """

    @classmethod
    def setUpClass(cls):
        cls._configurator = Configurator(test=True)
        cls._configurator2 = Configurator(test=True)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self._configurator.delete_config()
        self._configurator2.delete_config()

    def test_del_config(self):
        self._configurator.save_epub_title('mytitle')
        self._configurator.load_epub_title()
        self._configurator.delete_config()
        with self.assertRaises(ConfiguratorError):
            self._configurator.load_epub_title()

    def test_get_calibre_recipes(self):
        recipes = self._configurator.get_all_calibre_recipes()
        if not recipes:
            warnings.warn('no calibre recipes returned. Is the custom'
                          'recipes folder empty?')
        for fp in recipes:
            self.assertTrue(fp.exists())

    def test_add_cloud(self):
        cloud_connector_name = TolinoCloudConnector.__name__
        sig = inspect.signature(TolinoCloudConnector)
        test_credentials = dict()
        for arg in sig.parameters:
            test_credentials[arg] = 'dummy'
        self._configurator.save_cloud_credentials(
                cloud_connector_name,
                test_credentials)
        res = self._configurator2.load_cloud_credentials()
        cloud_connector_cls, credentials = res
        self.assertEqual(cloud_connector_cls, TolinoCloudConnector)
        self.assertDictEqual(test_credentials, credentials)

    def test_add_recipe(self):
        test_user = 'me'
        test_password = 'secret_pass'
        recipe_fp = Path(__file__).parent / TEST_RECIPE_FN
        self._configurator.save_recipe(
                recipe_fp,
                username=test_user,
                password=test_password,
                )
        res = self._configurator2.load_recipes()
        fps, users, passwords = res
        user = users[0]
        password = passwords[0]
        fp = fps[0]
        self.assertEqual(fp, recipe_fp)
        self.assertEqual(user, test_user)
        self.assertEqual(password, test_password)

    def test_add_title(self):
        test_title = 'mytitle'
        self._configurator.save_epub_title(test_title)
        title = self._configurator2.load_epub_title()
        self.assertEqual(title, test_title)


def check_crontab():
    configurator = Configurator(True)
    try:
        configurator.add_in_crontab(8, 42)
    except ConfiguratorError as e:
        print(e)
    subprocess.run(['crontab', '-l'])
    input('check you crontab if there is a task at 8:42')
    configurator.del_crontab()
    subprocess.run(['crontab', '-l'])
    input('check you crontab if task has been deleted')
    configurator.delete_config()


def check_print_config():
    configurator = Configurator(True)
    sig = inspect.signature(TolinoCloudConnector)
    test_credentials = dict()
    for arg in sig.parameters:
        test_credentials[arg] = 'dummy'
    configurator.save_cloud_credentials(
            TolinoCloudConnector.__name__, test_credentials)
    configurator.save_epub_title('title')
    recipe_fp = Path(__file__).parent / TEST_RECIPE_FN
    configurator.save_recipe(recipe_fp)
    print(configurator)


if __name__ == '__main__':
    check_print_config()
