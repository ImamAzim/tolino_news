from pathlib import Path


import pytolino
from pytolino.tolino_cloud import PARTNERS


from tolino_news.models.interfaces import CloudConnector


DEFAULT_PARTNER = PARTNERS[0]


class TolinoCloudConnector(CloudConnector):

    """use a tolino cloud (based on pytolino)"""

    def __init__(self, username: str, password: str, server: str = DEFAULT_PARTNER):
        """

        :username: credential from tolino cloud
        :password: credential from tolino cloud
        :server: partner url hosting cloud

        """
        self._username = username
        self._password = password
        self._server = server
        print(server)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def upload(self, fp: Path) -> str:
        pass

    def delete_file(self, adress: str):
        pass
