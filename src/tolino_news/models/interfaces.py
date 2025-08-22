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
