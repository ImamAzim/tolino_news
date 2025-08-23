from pathlib import Path


from pytolino.tolino_cloud import PARTNERS, Client, PytolinoException


from tolino_news.models.interfaces import CloudConnector


DEFAULT_PARTNER = PARTNERS[0]


class TolinoCloudConnector(CloudConnector):

    """use a tolino cloud (based on pytolino)"""

    def __init__(
            self,
            username: str,
            password: str,
            server: str = DEFAULT_PARTNER):
        """

        :username: credential from tolino cloud
        :password: credential from tolino cloud
        :server: partner url hosting cloud

        """
        self._username = username
        self._password = password
        self._client = Client(server_name=server)

    def connect(self):
        self._client.login(self._username, self._password)
        self._client.register()

    def disconnect(self):
        self._client.unregister()
        self._client.logout()

    def __enter__(self):
        try:
            self.connect()
        except PytolinoException as e:
            print('failed to login or register')
            print(e)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.disconnect()
        except PytolinoException as e:
            print('failed to unregister or logout')
            print(e)

    def upload(self, fp: Path) -> str:
        pass

    def delete_file(self, adress: str):
        pass
