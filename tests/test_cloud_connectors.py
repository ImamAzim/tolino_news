import configparser
from pathlib import Path
import inspect


from tolino_news.models.cloud_connectors import CloudConnectorException
from tolino_news.models.cloud_connectors import cloud_connectors


TEST_EPUB = 'basic-v3plus2.epub'


def get_credentials(cloud_connector_name):
    fp = Path.home() / 'credentials.ini'
    if fp.exists():
        credentials_config = configparser.ConfigParser()
        credentials_config.read(fp)
        credentials = credentials_config[cloud_connector_name]
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


def cloud_connector_test(cloud_connector_name):
    credentials = get_credentials(cloud_connector_name)
    epub_fp = Path(__file__).parent / TEST_EPUB
    cloud_connector_cls = cloud_connectors[cloud_connector_name]
    with cloud_connector_cls(**credentials) as tcc:
        print(cloud_connector_name)
        try:
            epub_id = tcc.upload(epub_fp)
            print(epub_id)
        except CloudConnectorException as e:
            print(e)
        else:
            input(
                    'check your cloud if a new epub has been created'
                    '!\npress enter')
            try:
                print('deleting', epub_id)
                tcc.delete_file(epub_id)
            except CloudConnectorException as e:
                print(e)
                print('failed to delete file')
            input('check your cloud if epub has been deleted!')


def all_cloud_connector_test():
    for cloud_connector_name in cloud_connectors:
        cloud_connector_test(cloud_connector_name)


def check_cloud_connectors():
    for name, cls in cloud_connectors.items():
        print(cls.__name__)
        sig = inspect.signature(cls)
        for arg, param in sig.parameters.items():
            print(arg)
            if param.default is not param.empty:
                print(param.default)


if __name__ == '__main__':
    # all_cloud_connector_test()
    cloud_connector_test('NextCloudConnector')
