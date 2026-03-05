from pathlib import Path
from abc import ABCMeta
import logging


from pytolino.tolino_cloud import PARTNERS, Client, PytolinoException
import nextcloud_client


from tolino_news.models.interfaces import CloudConnector


DEFAULT_PARTNER = list(PARTNERS)[0]
DEFAULT_EPUB_NAME = 'news'


class CloudConnectorException(Exception):
    pass


cloud_connectors = dict()


class MetaCloudConnector(ABCMeta):

    """meta class for cloud connector to store class in a dict"""

    def __init__(cls, name, bases, dict):
        """store the class in a dict upon creation"""
        ABCMeta.__init__(cls, name, bases, dict)
        cloud_connectors[name] = cls


class TolinoCloudConnector(CloudConnector, metaclass=MetaCloudConnector):

    """use cloud provided by Tolino (with tolino API) requires
    partner name (ex orellfuessli)."""
    _COLLECTION = 'news'

    def __init__(
            self,
            username: str,
            password: str,
            server: str = DEFAULT_PARTNER,
            login_with_chromium=False,
            ):
        """

        :server: partner url hosting cloud
        :username: to login to server
        :password: to login to server
        :login_with_chromim: use seleniumbase, chromium-browser
        (and xvfb on headless device) to login. will not work with a rpi
        zero

        """
        self._client = Client(server_name=server, username=username)
        self._password = password
        self._login_with_chromium = login_with_chromium

    def connect(self):
        self._client.login(self._password, self._login_with_chromium)

    def disconnect(self):
        pass

    def __enter__(self):
        try:
            self.connect()
        except PytolinoException as e:
            logging.error('failed to be logged in')
            logging.error(e)
            self._connected = False
        else:
            self._connected = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        self._connected = False

    def upload(self, fp: Path) -> str:
        try:
            epub_id = self._client.upload(fp)
            self._client.add_to_collection(epub_id, self._COLLECTION)
        except PytolinoException as e:
            print(e)
            raise CloudConnectorException
        return epub_id

    def delete_file(self, adress: str):
        try:
            self._client.delete_ebook(adress)
        except PytolinoException as e:
            print(e)
            raise CloudConnectorException


class NextCloudConnector(CloudConnector, metaclass=MetaCloudConnector):

    """use a nextcloud drive. (with webdav for public folders enabled)"""

    def __init__(
            self,
            webdav_link: str,
            ):
        """

        :webdav_link: must be shared with public

        """
        self._client = nextcloud_client.Client.from_public_link(
                webdav_link,
                )

    def connect(self):
        pass

    def disconnect(self):
        pass

    def __enter__(self):
        self.connect()
        self._connected = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        self._connected = False

    def upload(self, fp: Path) -> str:
        try:
            success = self._client.drop_file(fp)
        except (
                nextcloud_client.HTTPResponseError,
                nextcloud_client.OCSResponseError,
                ) as e:
            print(e)
            raise CloudConnectorException
        else:
            if not success:
                print('failed to upload')
                raise CloudConnectorException
            else:
                epub_id = fp.name
                return epub_id

    def delete_file(self, adress: str):
        try:
            success = self._client.delete(adress)
        except nextcloud_client.HTTPResponseError as e:
            print(e)
            raise CloudConnectorException
        else:
            if not success:
                print('failed to delete file')
                raise CloudConnectorException
