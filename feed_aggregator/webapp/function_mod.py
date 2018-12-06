from threading import Thread
from datetime import datetime
import flask
import requests
import feedparser
import re

from webapp import app, db_log_mod, db_rss_channel_mod, db_rss_item_mod


def requester(url: str) -> tuple:
    """
    Для проверки доступности URL и RSS-контента на нём.
    И получения некоторых параметров с данного URL (в случае доступности).
    :param url: адрес по которому посылается запрос.
    :return: кортеж с параметрами (url, status_code, length_content, title_channel, url_site, result)
    """

    # Проверка доступности URL.
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        # для того что бы быть опознанным как браузер

        page = requests.get(url, headers=headers)
        status_code = page.status_code
        length_content = len(page.content)

    except Exception as err:
        result = 'Запрашиваемый сайт недоступен.'
        # result = 'Failed to open url.'
        # app.logger.info('requester failed with this error: Failed to open url. ' + str(err))
        return url, 'Error', 'Error', 'Error', 'Error', result

    # Проверка доступности RSS-контента.
    try:
        feed = feedparser.parse(url)
        title_channel = feed.channel.title
        url_site = feed.channel.link

    except Exception as err:
        result = 'Ошибка при попытке считывания rss.'
        # result = 'Failed to open rss.'
        # app.logger.info('requester failed with this error: Failed to open rss. ' + str(err))
        return url, status_code, length_content, 'Error', 'Error', result

    # result = 'completed' признак успешного завершения запроса.
    return url, status_code, length_content, title_channel, url_site, 'completed'


def checker(list_from_request: tuple, contents: list) -> bool:
    """
    Сравнивает размер страницы из запроса и channel_tab.
    :param list_from_request: данные из запроса.
    :param contents: данные из channel_tab.
    :return: Возвращает True если размер совпадает.
    Вызывает add_rss и возращает False если размер не совпадает.
    """

    try:
        if list_from_request[2] != contents[0][4]:
            add_rss(list_from_request[0])
            return False
        else:
            return True

    except Exception as err:
        app.logger.info('checker failed with this error: ' + str(err))


def do_search(url: str) -> None:
    """
    Посылает запрос (requester), ивлекает данные из запроса, выполняет поиск по БД возвращает результаты.
    :param url: адрес по которому посылается запрос
    :return: None.
    """

    try:

        # Данные для лога
        list_for_log = (url,
                        flask.request.remote_addr,
                        flask.request.user_agent.browser,
                        flask.request.user_agent.platform,)

        list_from_request = requester(url)

        if list_from_request[5] == 'completed' and 100 <= int(list_from_request[1]) <= 299:
            contents = db_rss_channel_mod.search_channel(list_from_request, list_for_log)

            if not contents:
                db_rss_channel_mod.add_channel(list_from_request, list_for_log)  # Добавляем новый канал.
                add_rss(list_from_request[0]) # Добавляем rss контент.
                flask.flash('Результаты проверки: <{}>'.format(url))
                flask.flash('Канал добавлен.')

            # Проверка наличия изменений
            elif not checker(list_from_request=list_from_request, contents=contents):
                db_rss_channel_mod.update_channel(list_from_request, list_for_log)  # Апдейтим данные в БД
                flask.flash('Результаты проверки: <{}>'.format(url))
                flask.flash('Информация на канале была изменена со времени последней проверки.')

            elif checker(list_from_request=list_from_request, contents=contents):
                db_rss_channel_mod.update_timestamp(list_from_request, list_for_log)  # Апдейтим timestamp для элемента.
                flask.flash('Результаты проверки: <{}>'.format(url))
                flask.flash('Информация на канале со времени последней проверки не изменялась.')

        else:
            flask.flash('Результаты проверки: <{}>'.format(url))
            flask.flash('{}'.format(list_from_request[5]))

            try:
                t = Thread(target=db_log_mod.add_log, args=(list_for_log, 'failed to open url'))
                t.start()

            except Exception as err:
                app.logger.info('Thread in do_search failed with this error:' + str(err))

    except Exception as err:
        app.logger.info('do_search failed with this error: ' + str(err))


def remove_channel(id: int) -> None:  # переименовать
    """
    Получает URL канала. Удаляет RSS-контент связанный с каналом, затем удаляет сам канал.
    :param id: id удаляемого элемента в channel_tab.
    :return: None.
    """

    try:
        if db_rss_channel_mod.search_channel_by_id(id):
            url_channel = db_rss_channel_mod.get_url_channel_by_id(id)
            db_rss_item_mod.remove_rss_by_url_channel(url_channel)
            db_rss_channel_mod.remove_channel_by_id(id)

            if db_rss_channel_mod.search_channel_by_id(id):
                flask.flash('Элемент с ID {} не был удалён.'.format(id))
            else:
                flask.flash('Элемент с ID {} был удалён.'.format(id))

        else:
            flask.flash('Элемента с ID {} нет в БД.'.format(id))

    except Exception as err:
        app.logger.info('function_mod.remove_channel_by_id failed with this error: ' + str(err))


def remove_log(id: int) -> None:  # переименовать
    """
    Удаление выбранного элемента из log_tab по id.
    :param id: id удаляемого элемента в channel_tab.
    :return: None.
    """

    try:
        if db_log_mod.search_log_by_id(id):
            db_log_mod.remove_log(id)

            if db_log_mod.search_log_by_id(id):
                flask.flash('Элемент с ID {} не был удалён.'.format(id))
            else:
                flask.flash('Элемент с ID {} был удалён.'.format(id))

        else:
            flask.flash('Элемента с ID {} нет в БД.'.format(id))

    except Exception as err:
        app.logger.info('function_mod.remove_log_by_id failed with this error: ' + str(err))


def remove_rss(id: int) -> None:  # переименовать
    """
    Удаление выбранного элемента из rss_tab по id.
    :param id: id удаляемого элемента в rss_tab.
    :return: None.
    """

    try:
        if db_rss_item_mod.search_rss_by_id(id):
            db_rss_item_mod.remove_rss_by_id(id)

            if db_rss_item_mod.search_rss_by_id(id):
                flask.flash('Элемент с ID {} не был удалён.'.format(id))
            else:
                flask.flash('Элемент с ID {} был удалён.'.format(id))

        else:
            flask.flash('Элемента с ID {} нет в БД.'.format(id))

    except Exception as err:
        app.logger.info('function_mod.remove_rss_by_id failed with this error: ' + str(err))


def add_rss(url: str) -> None:
    """
    Посылает запрос по URL. Проверяет наличие элемента в rss_tab по url_item.
    При отсутствии элементта в БД добавляет его.
    :param url: адрес по которому посылается запрос.
    :return: None.
    """

    def clean_html(raw_html: str) -> str:
        """
        Для удаления html тегов из текста.
        Вспомогательная функция для add_rss
        :param raw_html: строка которая может содержать теги.
        :return: строка без тегов
        """

        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, '', raw_html)
        return clean_text

    def time_convert(input_time: str) -> str:
        """
        Для преобразования времени в формат удобный для сортировки в БД.
        Вспомогательная функция для add_rss.
        :param input_time: исходная строка даты-времени.
        :return: преобразованная строка даты-времени.
        """

        dt = datetime.strptime(input_time, '%a, %d %b %Y %X %z')
        output_time = str(dt.strftime('%Y-%m-%d %X %z'))
        return output_time

    try:
        feed = feedparser.parse(url)

        for item in feed['items']:
            if not db_rss_item_mod.search_rss_by_url_item(item.link):
                db_rss_item_mod.add_rss((url, item.title, clean_html(item.summary),
                                         item.link, time_convert(item.published)))

    except Exception as err:
        app.logger.info('add_rss failed with this error: ' + str(err))


def channels_to_listdict() -> list:
    """
    Преобразует список кортежей каналов в список словарей, для отображения на entry.html.
    :return: список словарей.
    """

    try:
        contents = db_rss_channel_mod.show_channel_restrict()
        channel_list = []

        for content in contents:
            channel_dict = {}
            channel_dict['id'] = content[0]
            channel_dict['url'] = content[1]
            channel_dict['title'] = content[2]
            channel_dict['time'] = content[3]
            channel_list.append(channel_dict)

        return channel_list

    except Exception as err:
        app.logger.info('channels_to_listdict failed with this error: ' + str(err))


def show_content(url_channel: str) -> list:
    """
    Отоброжаем содержимое определённого канала из rss_tab.
    Добавляет данные в log_tab, при отображении содержимого канала.
    :param url_channel: url канала, содержимое которого будет отображаться.
    :return: список словарей с данными из таблицы соответствущие каналу.
    """

    try:
        list_for_log = (url_channel,
                        flask.request.remote_addr,
                        flask.request.user_agent.browser,
                        flask.request.user_agent.platform,)

        contents = db_rss_item_mod.show_channel_content(url_channel, list_for_log)

        rss_list = []

        for content in contents:
            rss_dict = {}
            rss_dict['title'] = content[0]
            rss_dict['summary'] = content[1]
            rss_dict['published'] = content[2]
            rss_dict['url'] = content[3]
            rss_list.append(rss_dict)

        return rss_list

    except Exception as err:
        app.logger.info('show_content failed with this error: ' + str(err))


def text_search(text: str) -> list:  # добавить данные для лога
    """
    Для поиска по тексту в поле summary_item таблицы rss_tab.
    Добавляет данные в log_tab, при поиске.
    :param text: подстрока, вхождение которой в summary_item необходимо найти.
    :return: список словарей с результатами поиска из rss_tab.
    """

    try:
        # Данные для лога
        list_for_log = ('None',
                        flask.request.remote_addr,
                        flask.request.user_agent.browser,
                        flask.request.user_agent.platform,)

        contents = db_rss_item_mod.search_rss_by_text(text, list_for_log)

        search_list = []

        for content in contents:
            search_dict = {}
            search_dict['url_channel'] = content[0]
            search_dict['title'] = content[1]
            search_dict['summary'] = content[2]
            search_dict['published'] = content[3]
            search_dict['url'] = content[4]
            search_list.append(search_dict)

        return search_list

    except Exception as err:
        app.logger.info('text_search failed with this error: ' + str(err))


def date_search(date: str) -> list:
    """
    Для поиска по дате в поле published_item таблицы rss_tab.
    Добавляет данные в log_tab, при поиске.
    :param date: подстрока, вхождение которой в published_item необходимо найти.
    :return: список словарей с результатами поиска из rss_tab.
    """

    try:
        # Данные для лога
        list_for_log = ('None',
                        flask.request.remote_addr,
                        flask.request.user_agent.browser,
                        flask.request.user_agent.platform,)

        contents = db_rss_item_mod.search_rss_by_date(date, list_for_log)

        search_list = []

        for content in contents:
            search_dict = {}
            search_dict['url_channel'] = content[0]
            search_dict['title'] = content[1]
            search_dict['summary'] = content[2]
            search_dict['published'] = content[3]
            search_dict['url'] = content[4]
            search_list.append(search_dict)

        return search_list

    except Exception as err:
        app.logger.info('date_search failed with this error: ' + str(err))


def complex_search(text: str, date: str) -> list:
    """
    Для комплексного поиска по тексту в поле summary_item, и дате в поле published_item таблицы rss_tab.
    Добавляет данные в log_tab, при поиске.
    :param text: подстрока, вхождение которой в summary_item необходимо найти.
    :param date: подстрока, вхождение которой в published_item необходимо найти.
    :return: список словарей с результатами поиска из rss_tab.
    """

    try:
        # Данные для лога
        list_for_log = ('None',
                        flask.request.remote_addr,
                        flask.request.user_agent.browser,
                        flask.request.user_agent.platform,)

        contents = db_rss_item_mod.search_rss_complex(text, date, list_for_log)

        search_list = []

        for content in contents:
            search_dict = {}
            search_dict['url_channel'] = content[0]
            search_dict['title'] = content[1]
            search_dict['summary'] = content[2]
            search_dict['published'] = content[3]
            search_dict['url'] = content[4]
            search_list.append(search_dict)

        return search_list

    except Exception as err:
        app.logger.info('complex_search failed with this error: ' + str(err))

