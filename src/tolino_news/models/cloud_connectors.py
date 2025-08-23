from pathlib import Path


import pytolino


from tolino_news.models.interfaces import CloudConnector


class TolinoCloudConnector(CloudConnector):

    """use a tolino cloud (based on pytolino)"""

    def __init__(self, credentials: dict):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def upload(self, fp: Path) -> str:
        pass

    def delete_file(self, adress: str):
        pass
