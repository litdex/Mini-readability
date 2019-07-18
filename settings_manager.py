import json # Используется для излечения и сохранения настроек в json формате
from abc import ABC, abstractmethod # Используется для обьявления абастрактного класса и указания абстрактных методов


class SettingsManager(ABC):
    '''Абстрактный класс для работы с настройками приложения'''

    def __init__(self):
        """При вызове конструктора класса сразу загружается настройки из файла, указанного в self._filepath

        Абстрактные переменные для обязательного определения в дочернем классе:
        self._filepath - содержит путь и название файла, куда стоит сохранить настройки
        self._DEFAULT_SETTINGS - содержит в себе шаблон настроек, который устанавливается по стандарту
        """

        # Будет хранить в себе настройки в течение работы приложения
        self._SETTINGS = self._download_settings()

    def _download_settings(self):
        """Выгружает настройки проверяя их в validate_settings и устанавливает стандартные, если с файлом что-то не то"""
        try:
            f = open(self._filepath)
            settings = json.load(f)
            if not self._validate_settings(settings):
                settings = self._DEFAULT_SETTINGS
        except Exception:
            settings = self._DEFAULT_SETTINGS
        finally:
            return settings

    def set_default(self):
        """Устанавливает настройки по умолчанию"""
        self._SETTINGS = self._DEFAULT_SETTINGS

    @abstractmethod
    def _validate_settings(self, settings)-> bool: 
        """Проверяет настройки на соответствие стандартному шаблону"""
        pass

    def save_settings(self):
        """Сохраняет все настройки в json формате по умолчанию"""
        with open(self._filepath , 'w') as f:
            json.dump(self._SETTINGS, f)

    @abstractmethod
    def get_settings(self):
        pass

    @abstractmethod 
    def set_settings(self, **kwargs):
        pass



class FormatSettingsManager(SettingsManager):
    """Класс, работающий с настройками формата возвращаемого результата"""

    def __init__(self):
        
        self._filepath = 'format_settings.json'

        self._DEFAULT_SETTINGS = {
            # Максимальная длина строки. Если ее превысить происходит перенос слова на следующую 
            "str_len": 80,
            # Шаблон вывода ссылки {data} -> текст внутри ссылки, {href} -> сама ссылка
            "link_format": '{data}[{href}]',
        }
        super().__init__()

    def get_settings(self, *args) -> dict:
        """Либо возвращает все настройки, либо возвращает словарь настроек, ключи которых указаны в *args"""
        if not args:
            return self._SETTINGS
        s = dict()
        for arg in args:
            if arg in self._SETTINGS:
                s[arg] = self._SETTINGS[arg]
        return s 

    def set_settings(self, kwargs:dict):
        """Устанавливает настройки по всем ключам в kwargs"""
        for key in kwargs:
            if key in self._SETTINGS:
                self._SETTINGS[key] = kwargs[key]

    def _validate_settings(self, settings):
        """Проверяет настройки на валидность, пока только по наличию ключа в стандартных настройках и по типу значений"""
        for key in self._DEFAULT_SETTINGS:
            if not key in settings or not type(settings[key]) == type(self._DEFAULT_SETTINGS[key]):
                return False
        return True




class ParserSettingsManager(SettingsManager):
    """Класс, работающий с настройками парсера"""


    def __init__(self):
        self._filepath = 'parser_settings.json'

        self._DEFAULT_SETTINGS ={
            # Обычно тут будет название домена, но стандартные настройки для всех остальных сайтов будут называться default
            'default':
                {
                    # Список тагов для заголовка
                    "title_tags": ["h1"],
                    # Атрибуты для дополнительного описания тага(например title_tags = 'div', content_atr{'class':'title_class'})
                    "title_atr": {},
                    # Таг, предназначеный для отбора данных
                    "content_tag": 'p',
                    # Атрибуты для дополнительного описания тага(например content_tag = 'div', content_atr{'class':'paragraph'})
                    "content_atr": {},
                },
        }

        super().__init__()


    def get_settings(self, domain:str = None, all_setting:bool = False):
        """ Возвращает настройки для парсера по домену или возвращает все настройки

        Если не найдено каких-либо настроек по имени хоста, то будут вставляется настройки из стандартного словаря
        Если установлен флаг all_settings, возвращает все настройки
        """
        if all_setting: return self._SETTINGS
        s = dict()
        if domain in self._SETTINGS:
            s = self._SETTINGS[domain]
            for setting in self._DEFAULT_SETTINGS['default']:
                if not setting in s:
                    s[setting] = self._DEFAULT_SETTINGS['default'][setting]
            return s
        return self._SETTINGS['default']



    def set_settings(self, kwargs:dict, domain:str = None):
        """Позволяет изменить настройки для опредленного домена.
        
        Если domain отсутсвует, то изменяет стандартные настройки
        """
        if not domain:
            settings = self._SETTINGS['default']
        else:
            if domain in self._SETTINGS:
                settings = self._SETTINGS[domain]
            else: return
        for key in kwargs:
            if key in settings:
                settings[key] = kwargs[key]
        

    def delete_settings(self, domain:str):
        """Позволяет удалить настройки парсера для определенного домена"""
        if domain != 'default':
            self._SETTINGS.pop(domain, None)


    def _validate_settings(self, settings_list):
        """Проверяет настройки на валидность, пока только по наличию ключа в стандартных настройках и по типу значений"""
        if not 'default' in settings_list: return False
        for settings_dict in settings_list:
            for setting in settings_list[settings_dict]:
                if not setting in self._DEFAULT_SETTINGS['default']:
                    return False
        return True

    def expand_settings(self, domain:str, **kwargs):
        """Добавляет настройки(указанные в *kwargs) для нового домена"""
        self._SETTINGS[domain] = kwargs