import unittest


from tolino_news.models.configurators import Configurator


class TestConfigurator(unittest.TestCase):

    """all test concerning configurator. """

    @classmethod
    def setUpClass(cls):
        cls.config = Configurator()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_get_names(self):
        # names, folder_path = self.config.get_recipes_names()
        # for name in names:
            # self.assertTrue(
                    # os.path.exists(os.path.join(
                        # folder_path, f'{name}.recipe')))

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
