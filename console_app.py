from settings_manager import FormatSettingsManager, ParserSettingsManager #Используются для получения настроек приложения
from html_downloader import HTMLDownloader #Используется для загрузки URL страниц
from html_parser import HTMLParser #Используется для получения полезной информации из HTML страницы
from content_manager import save_content #Используется для сохранения контента в файле .txt
from time import time

def create_filename(text):
    """Используется для получения названия файла, который нужно сохранить"""
    i = 0 
    title = text.split('\n')[i]
    while not title:
        i += 1
        title = text.split('\n')[i]
    return u'{}'.format(title[:80])


if __name__ == "__main__":
    format_settings_manager = FormatSettingsManager()
    format_settings = format_settings_manager.get_settings()
    content_place = 'content/{title}.txt'
    parser_settings_manager = ParserSettingsManager()


    input_str = ''
    while input_str != '0':
        print('Введите url для парсинга страницы:')
        url = input()
        try:
            html_downloader = HTMLDownloader(url)
            html = html_downloader.get_html()
        except:
            print('Вы ввели неверную ссылку')
            continue
        parser_settings = parser_settings_manager.get_settings(html_downloader.get_domain())
        html_parser = HTMLParser(html, parser_settings, format_settings)
        content = html_parser.get_text()
        print(content)
        print('Хотите сохранить текст?(Y - да)')
        if input().upper() == 'Y':
            save_content(content_place.format(title = create_filename(content)), content)
        print('\n\n Введите: 0, если хотите выйти\n')
        input_str = input().upper()
            
        

