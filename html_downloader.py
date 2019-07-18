import requests # Используется для получения html по url
from urllib.parse import urlparse # Используется для извлечения доменного имени



class HTMLDownloader():
    """Класс, предназначеный для загрузки html страницы по URL"""

    def __init__(self, url):
        """ При указании url, конструктор сам получает html страницу и извлекает доменное имя"""
        self._url = url
        self._domain = urlparse(url).hostname
        self._html = requests.get(url).text

    def get_domain(self):
        return self._domain

    def get_url(self):
        return self._url

    def get_html(self):
        return self._html



