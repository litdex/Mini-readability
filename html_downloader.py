import requests # Используется для получения html по url
from urllib.parse import urlparse # Используется для извлечения доменного имени



class HTMLDownloader():
    """Класс, предназначеный для загрузки html страницы по URL"""

    def __init__(self, url):
        self._url = url

    def get_domain(self):
        return urlparse(self._url).hostname

    def get_url(self):
        return self._url

    def get_html(self):
        return requests.get(self._url).text



