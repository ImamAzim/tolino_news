import configparser
from pathlib import Path


from tolino_news.models.cloud_connectors import TolinoCloudConnector


TEST_EPUB = 'basic-v3plus2.epub'


def get_credentials():
    fp = Path.home() / 'credentials.ini'
    if fp.exists():
        credentials_config = configparser.ConfigParser()
        credentials_config.read(fp)
        credentials = credentials_config['DEFAULT']
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
        epub_id = tcc.upload(epub_fp)
        input('check your cloud if a new epub has been created!\npress enter')
        tcc.delete_file(epub_id)
        input('check your cloud if epub has been deleted!')


if __name__ == '__main__':
    test_tolino_cloud_connector()
