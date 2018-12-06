from threading import Thread

from webapp import app, db_log_mod
from webapp.db_context_manager_mod import DatabaseConnection, ConnectionError, CredentialsError, SQLError


def add_rss(list_from_request: tuple) -> None:
    """
     Добавляет элемент в rss_tab.
    :param list_from_request: list_from_request: данные из запроса.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """INSERT INTO rss_tab
                      (url_channel_r, title_item, summary_item, url_item, published_item)
                       VALUES
                      (%s, %s, %s, %s, %s);"""

            cursor.execute(_SQL, (list_from_request[0],
                                  list_from_request[1],
                                  list_from_request[2],
                                  list_from_request[3],
                                  list_from_request[4],
                                  ))

    except ConnectionError as err:
        app.logger.info('add_rss failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('add_rss failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('add_rss failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('add_rss failed with this error: ' + str(err))


def show_rss() -> tuple:
    """
    Отоброжает содержимое rss_tab.
    :return: список кортежей со всеми данными из таблицы.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT * FROM rss_tab ORDER BY id DESC LIMIT 10000;"""

            cursor.execute(_SQL)
            contents = cursor.fetchall()

        return contents

    except ConnectionError as err:
        app.logger.info('show_rss failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('show_rss failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('show_rss failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('show_rss failed with this error: ' + str(err))


def show_channel_content(url_channel: str, list_for_log: tuple) -> list:
    """
    Отоброжаем содержимое определённого канала из rss_tab.
    :param url_channel: url канала, содержимое которого будем отображать.
    :param list_for_log: данные для add_log.
    :return: список кортежей с данными из таблицы соответствущие каналу.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT title_item, summary_item, published_item, url_item
             FROM rss_tab WHERE url_channel_r=%s ORDER BY published_item DESC LIMIT 1000;"""

            cursor.execute(_SQL, ( url_channel ,) )
            contents = cursor.fetchall()

            try:
                t = Thread(target=db_log_mod.add_log, args=(list_for_log, 'show channel content'))
                t.start()

            except Exception as err:
                app.logger.info('Thread in show_channel_content failed with this error:' + str(err))

        return contents

    except ConnectionError as err:
        app.logger.info('show_channel_content failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('show_channel_content failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('show_channel_content failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('show_channel_content failed with this error: ' + str(err))


def search_rss_by_id(id: int) -> bool:
    """
    Для поиска по id в channel_tab.
    Применяется для поиска элемента при удалении конкретного элемента из rss_tab.
    :param id: id искомого элемента в rss_tab.
    :return: возращает True если находит элемент, и False если нет.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT * FROM rss_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))
            contents = cursor.fetchall()

            if not contents:
                return False
            else:
                return True

    except ConnectionError as err:
        app.logger.info('search_rss_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_rss_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_rss_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_rss_by_id failed with this error: ' + str(err))


def search_rss_by_url_item(url_item: str) -> bool:
    """
    Для поиска по url_item в rss_tab.
    Применяется для поиска элемента при добавлении новых данных, для избегания дублирования.
    :param url_item: url конкретного rss item
    :return: возращает True если находит элемент, и False если нет.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT * FROM rss_tab WHERE url_item=%s;"""

            cursor.execute(_SQL, (url_item,))
            contents = cursor.fetchall()

            if not contents:
                return False
            else:
                return True

    except ConnectionError as err:
        app.logger.info('search_rss_by_url_item failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_rss_by_url_item failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_rss_by_url_item failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_rss_by_url_item failed with this error: ' + str(err))


def remove_rss_by_id(id: int) -> None:  # возможно переименовать
    """
    Удаление выбранного элемента из rss_tab по id.
    Применяется для удаления конкретного элемента из rss_tab.
    :param id: id удаляемого элемента в rss_tab.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """DELETE FROM rss_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))

    except ConnectionError as err:
        app.logger.info('db_rss_mod.remove_rss_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('db_rss_mod.remove_rss_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('db_rss_mod.remove_rss_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('db_rss_mod.remove_rss_by_id failed with this error: ' + str(err))


def remove_rss_by_url_channel(url_channel: str) -> None:  # возможно переименовать
    """
    Удаление выбранного элемента/ов из rss_tab по url_channel.
    Применяется для групового удаления элементов связанных с url_channel из rss_tab,
    при удалении, в свою очередь, данного канала из channel_tab
    :param url_channel: url_channel удаляемого элемента/ов в rss_tab.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """DELETE FROM rss_tab WHERE url_channel_r=%s;"""

            cursor.execute(_SQL, (url_channel,))

    except ConnectionError as err:
        app.logger.info('db_rss_mod.remove_rss_by_url_channel failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('db_rss_mod.remove_rss_by_url_channel failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('db_rss_mod.remove_rss_by_url_channel failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('db_rss_mod.remove_rss_by_url_channel failed with this error: ' + str(err))


def search_rss_by_text(text: str, list_for_log: tuple) -> list:
    """
    Для поиска по тексту в поле summary_item таблицы rss_tab.
    :param text: подстрока, вхождение которой в summary_item необходимо найти.
    :param list_for_log: данные для add_log.
    :return: список кортежей с результатами поиска из rss_tab.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT url_channel_r, title_item, summary_item, published_item, url_item
             FROM rss_tab WHERE summary_item LIKE CONCAT('%',%s,'%') ORDER BY published_item DESC LIMIT 1000;"""

            cursor.execute(_SQL, (text,))
            contents = cursor.fetchall()

            try:
                t = Thread(target=db_log_mod.add_log,
                           args=(list_for_log, ('search rss by text <{}> '.format(text))))
                t.start()

            except Exception as err:
                app.logger.info('Thread in search_rss_by_text failed with this error:' + str(err))

            return contents

    except ConnectionError as err:
        app.logger.info('db_rss_mod.search_rss_by_text failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('db_rss_mod.search_rss_by_text failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('db_rss_mod.search_rss_by_text failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('db_rss_mod.search_rss_by_text failed with this error: ' + str(err))


def search_rss_by_date(date: str, list_for_log: tuple) -> list:
    """
    Для поиска по дате в поле published_item таблицы rss_tab.
    :param date: подстрока, вхождение которой в published_item необходимо найти.
    :param list_for_log: данные для add_log.
    :return: список кортежей с результатами поиска из rss_tab.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT url_channel_r, title_item, summary_item, published_item, url_item
             FROM rss_tab WHERE published_item LIKE CONCAT(%s,'%') ORDER BY published_item DESC LIMIT 1000;"""

            cursor.execute(_SQL, (date,))
            contents = cursor.fetchall()

            try:
                t = Thread(target=db_log_mod.add_log,
                           args=(list_for_log, ('search rss by date <{}> '.format(date))))
                t.start()

            except Exception as err:
                app.logger.info('Thread in search_rss_by_date failed with this error:' + str(err))

            return contents

    except ConnectionError as err:
        app.logger.info('db_rss_mod.search_rss_by_date failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('db_rss_mod.search_rss_by_date failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('db_rss_mod.search_rss_by_date failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('db_rss_mod.search_rss_by_date failed with this error: ' + str(err))


def search_rss_complex(text: str, date: str, list_for_log: tuple) -> list:
    """
    Для комплексного поиска по тексту в поле summary_item, и дате в поле published_item таблицы rss_tab.
    :param text: подстрока, вхождение которой в summary_item необходимо найти.
    :param date: подстрока, вхождение которой в published_item необходимо найти.
    :param list_for_log: данные для add_log.
    :return: список кортежей с результатами поиска из rss_tab.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT url_channel_r, title_item, summary_item, published_item, url_item
                         FROM rss_tab WHERE published_item LIKE CONCAT(%s,'%') AND summary_item LIKE CONCAT('%',%s,'%')
                          ORDER BY published_item DESC LIMIT 1000;"""

            cursor.execute(_SQL, (date, text))
            contents = cursor.fetchall()

            try:
                t = Thread(target=db_log_mod.add_log,
                           args=(list_for_log, ('search rss complex <{}> <{}> '.format(text, date))))
                t.start()

            except Exception as err:
                app.logger.info('Thread in search_rss_complex failed with this error:' + str(err))

            return contents

    except ConnectionError as err:
        app.logger.info('db_rss_mod.search_rss_complex failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('db_rss_mod.search_rss_complex failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('db_rss_mod.search_rss_complex failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('db_rss_mod.search_rss_complex failed with this error: ' + str(err))