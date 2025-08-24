import configparser
from pathlib import Path
import inspect


from tolino_news.models.cloud_connectors import TolinoCloudConnector
from tolino_news.models.cloud_connectors import CloudConnectorException
from tolino_news.models.cloud_connectors import cloud_connectors


TEST_EPUB = 'basic-v3plus2.epub'


def get_credentials():
    fp = Path.home() / 'credentials.ini'
    if fp.exists():
        credentials_config = configparser.ConfigParser()
        credentials_config.read(fp)
        credentials = credentials_config.defaults()
    else:
        import getpass
        server = input('server:\n')
        username = input('username:\n')
        password = getpass.getpass()
        credentials = dict(
                server=server,
                username=username,
                password=password
                )
    return credentials


def test_tolino_cloud_connector():
    credentials = get_credentials()
    epub_fp = Path(__file__).parent / TEST_EPUB
    with TolinoCloudConnector(**credentials) as tcc:
        try:
            epub_id = tcc.upload(epub_fp)
        except CloudConnectorException as e:
            print(e)
            print('failed to upload')
        input('check your cloud if a new epub has been created!\npress enter')
        try:
            tcc.delete_file(epub_id)
        except CloudConnectorException as e:
            print(e)
            print('failed to delete file')
        input('check your cloud if epub has been deleted!')


def test_cloud_connectors():
    for name, cls in cloud_connectors.items():
        sig = inspect.signature(cls)
        for arg, param in sig.parameters.items():
            print(arg)
            if param.default is not param.empty:
                print(param.default)


if __name__ == '__main__':
    # test_tolino_cloud_connector()
    test_cloud_connectors()
