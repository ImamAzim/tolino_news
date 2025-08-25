import unittest
import warnings
import inspect


from tolino_news.models.configurators import Configurator
from tolino_news.models.cloud_connectors import TolinoCloudConnector


TEST_RECIPE_FN = 'test_recipe.recipe'


class TestConfigurator(unittest.TestCase):

    """all test concerning configurator. """

    @classmethod
    def setUpClass(cls):
        cls._configurator = Configurator()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_calibre_recipes(self):
        recipes = self._configurator.get_all_calibre_recipes()
        if not recipes:
            warnings.warn('no calibre recipes returned. Is the custom'
                          'recipes folder empty?')
        for fp in recipes:
            self.assertTrue(fp.exists())

    def test_save_and_load_config(self):
        test_user = 'me'
        test_password = 'secret_pass'
        test_server = 'some_server'
        recipe_fp = __file__.parent / TEST_RECIPE_FN
        self._configurator.add_recipe(
                recipe_fp,
                username=test_user,
                password=test_password,
                )
        cloud_connector_name = TolinoCloudConnector.__name__
        sig = inspect.signature(TolinoCloudConnector)
        test_credentials = dict()
        for arg in sig.parameters:
            test_credentials[arg] = 'dummy'
        self._configurator.add_cloud_credentials(
                cloud_connector_name,
                test_credentials)
        self._configurator.save_config()
        res = self._configurator.load_cloud_credentials()
        cloud_connector_cls, credentials = res

        self.assertEqual(cloud_connector_cls, TolinoCloudConnector)
        self.assertDictEqual(test_credentials, credentials)


    # def test_add_recipe(self):
        # self.config.add_recipe('recipe1')
        # self.config.add_recipe('recipe2', 'me', 'mypassword')

        # recipe_dict = self.config._config_dict['recipes']

        # self.assertIn('recipe1', recipe_dict)
        # recipe = recipe_dict['recipe1']
        # self.assertIsNone(recipe.get('username'))
        # self.assertIsNone(recipe.get('password'))

        # self.assertIn('recipe2', recipe_dict)
        # recipe = recipe_dict['recipe2']
        # self.assertEqual(recipe.get('username'), 'me')
        # self.assertEqual(recipe.get('password'), 'mypassword')

    # def test_add_tolino_cloud_config(self):
        # mytolino_config = dict(
                # server_name='server name',
                # username='me',
                # password='secret',
                # epub_name='test',
                # )
        # self.config.add_tolino_cloud_config(**mytolino_config)
        # config_dict = self.config._config_dict
        # self.assertIn('tolino_cloud_config', config_dict)
        # tolino_config = config_dict['tolino_cloud_config']
        # self.assertDictEqual(mytolino_config, tolino_config)

    # def test_save_config_file(self):
        # timestamps = time.time()
        # self.config.add_recipe('recipe1')
        # self.config.add_recipe('recipe2', 'me', 'mypassword')

        # toml_str = self.config.save_config(test=True)
        # toml_dict = tomli.loads(toml_str)

    # def test_load_config(self):
        # if os.path.exists(self.config.config_fp):
            # data = self.config.load_config()
            # self.assertIsInstance(data, dict)
        # else:
            # with self.assertRaises(FileNotFoundError):
                # self.config.load_config()

if __name__ == '__main__':
    pass
