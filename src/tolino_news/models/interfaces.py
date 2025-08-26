from abc import abstractmethod, ABC
from pathlib import Path


class CloudConnector(ABC):

    """class to connect to a cloud for file upload and folder cleaning"""

    def __init__(self, credentials: dict):
        """

        :credentials: info to connect to the server

        """
        ABC.__init__(self)

        self._credentials = credentials

    @abstractmethod
    def connect(self):
        """login and register device (if applicable)
        :returns: TODO

        """
        pass

    @abstractmethod
    def disconnect(self):
        """logout and unregister device (if applicable)
        :returns: TODO

        """
        pass

    @abstractmethod
    def __enter__(self):
        """connect before asking operation to cloud for context manager
        :returns: TODO

        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """make sure to disconnect after exiting context manager

        :exc_type: None if exited without expections
        :exc_value: None if exited without expections
        :traceback: None if exited without expections

        """
        pass

    @abstractmethod
    def upload(self, fp: Path) -> str:
        """upload a file to the cloud. must be called after connect.

        :fp: path to file to upload
        :returns: adress of uploaded file

        """
        pass

    @abstractmethod
    def delete_file(self, adress: str):
        """delete online file

        :adress: point to the file to be deleted
        :returns: TODO

        """
        pass


class BaseConfigurator(ABC):

    """helper class to store and load configuration for recipes
    and cloud"""

    @abstractmethod
    def get_all_calibre_recipes(self) -> list[Path]:
        """find present custom recipes in calibre config folder
        :returns: list of recipes fp

        """
        pass

    @abstractmethod
    def add_recipe(
            self,
            recipe_fp: Path,
            username=None,
            password=None):
        """add a recipe to the configuration

        :recipe_fp: point to recipe file
        :username: str if required
        :password: str if required

        """
        pass

    @abstractmethod
    def add_cloud_credentials(
            self,
            cloud_connector: str,
            credentials: dict,
            ):
        """add credentials of the cloud to the config

        :cloud_connector: name of the class of the cloud_connector to use
        :credentials: kwargs for the cloud_connector class

        """
        pass

    @abstractmethod
    def save_config(self, overwrite=False, test=False):
        """save the current configuration

        :overwrite: True if you want to replace previous file
        :test: True if you want to use a test config file

        """
        pass

    @abstractmethod
    def delete_config(self):
        """delete stored configuration

        """
        pass

    @abstractmethod
    def add_in_crontab(self, hour: int, minute: int):
        """add the news loader job in user crontab

        :hour: time at which job is run
        :minute: time at which job is run

        """
        pass

    @abstractmethod
    def del_crontab(self):
        """delete the news loader job in the crontab

        """
        pass

    @abstractmethod
    def load_cloud_credentials(
            self,
            ) -> tuple[type, dict]:
        """get the stored cloud credentials and cloud connector

        :returns: cloud connector class and required arguments

        """
        pass

    @abstractmethod
    def get_stored_recipes(
            self,
            ) -> tuple[list[Path], list[str | None], list[str | None]]:
        """get all the stored recipes from config and credentials if any
        :returns: recipes_fp, users, passwords

        """
        pass

    @abstractmethod
    def install_epubmerge_plugin(self):
        """use calibre customize to install zip file

        """
        pass
