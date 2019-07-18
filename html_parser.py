from bs4 import BeautifulSoup #библиотека, которая парсит страницу html и позволяет работать с ней
from queue import Queue #содержит в себе структуру данных очереди, где извлечение и добавление элемента O(1)
import textwrap #позволяет переносить текст по словам

class HTMLParser():
    """Класс, выполняющий основную фукнцию приложения, извлекает полезные данные из страницы html и преобразует их в текст"""

    def __init__(self, html:str, parser_settings:dict, format_settings:dict):
        """Происходит настройка работы парсера

        parser_settings:
            title_tags 
            title_atr
            content_tag 
            content_atr 
        
        format settings:
            self._str_len: int
            self._link_format: str  описывает шаблон для ссылки с {data}{href}
        """
        self._html = html
        self._soup = BeautifulSoup(html)
        self._title_tags = parser_settings['title_tags']
        self._title_atr = parser_settings['title_atr']
        self._content_tag = parser_settings['content_tag']
        self._content_atr = parser_settings['content_atr']
        self._delete_all_excess()

        self._str_len = format_settings['str_len']
        self._link_format = format_settings['link_format']

    def _delete_all_excess(self):
        """Удаляет все скрипты и стили из html"""
        for tag in self._soup.findAll():
            if tag.name in ["script", "style",]:
                tag.extract()
    
    def _parse_document(self):
        """Получает очередь из полезной информации, в которой вперемешку хранятся ссылки, текст и заголовки"""
        def filter_by(item, tags:str, atrs):
            """Фильтрует тег по атрибутам. 
            
            К сожалению это вынужденная операция, так как в soup.FindAll() сразу для нескольких тагов этого сделать нельзя"""

            if item.name not in tags: return False
            for atr in atrs:
                try:
                    if atrs[atr] == " ".join(item.get(atr)):
                        return True
                    else: return False
                except Exception:
                    return False
            return True

        all_doc = self._soup.findAll([self._title_tags, self._content_tag]) #Находим все содержимое указанных в параметрах тагах(включая их самих)
        output_queue = Queue()
        for tag in all_doc: #Проходим по содержимому 
                if filter_by(tag, self._content_tag, self._content_atr):#Фильтруем таг контента по атрибутам
                    paragraph = ''
                    for item in tag: #Проходим по всему в теге контента
                        if item.name == 'a': #Добавляем ссылку в очередь по формату 
                            paragraph += self._link_format.format(data = item.string, href = item.get('href'))
                        elif item.string: #Иначе добавляем текст в очередь
                            paragraph += item.string
                    output_queue.put(paragraph)
                if filter_by(tag, self._title_tags, self._title_atr): #Фильтруем таг заголовка по атрибутам
                    for item in tag.contents:
                        output_queue.put(item.string) #Добавляем заголовок в очередь
        return output_queue 

    def get_text(self):
        """Метод для получения текста из очереди полученой в _parse_document"""
        text = ''
        output_text = ''
        text_queue = self._parse_document()
        while not text_queue.empty():
            text = text_queue.get()
            output_text += '\n'.join(textwrap.wrap(text, self._str_len, break_long_words=False, replace_whitespace = False) ) + "\n\n   "
        return output_text



