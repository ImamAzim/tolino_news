import configparser
from pathlib import Path


from tolino_news.models.cloud_connectors import CloudConnector


def get_credentials():
    fp = Path.home() / 'credentials.ini'
    if fp.exists():
        credentials = configparser.ConfigParser()
        credentials.read(fp)
        server = credentials['DEFAULT']['server']
        username = credentials['DEFAULT']['username']
        password = credentials['DEFAULT']['password']
    else:
        import getpass
        server = input('server:\n')
        username = input('username:\n')
        password = getpass.getpass()
    return server, username, password


def test_tolino_cloud_connector():
    credentials = get_credentials()
    print(credentials)


if __name__ == '__main__':
    test_tolino_cloud_connector()
