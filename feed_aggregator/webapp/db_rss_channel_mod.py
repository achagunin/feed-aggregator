from threading import Thread

from webapp import app, db_log_mod
from webapp.db_context_manager_mod import DatabaseConnection, ConnectionError, CredentialsError, SQLError


def add_channel(list_from_request: tuple, list_for_log: tuple) -> None:
    """
    Добавляет элемент в channel_tab.
    :param list_from_request: данные из запроса (url_channel, status_code, length_content, title_channel, url_site).
    :param list_for_log: данные для add_log.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """INSERT INTO channel_tab
                      (url_channel_c, status_code, length_content, title_channel, url_site)
                       VALUES
                      (%s, %s, %s, %s, %s);"""

            cursor.execute(_SQL, (list_from_request[0],
                                  list_from_request[1],
                                  list_from_request[2],
                                  list_from_request[3],
                                  list_from_request[4],
                                  ))

    except ConnectionError as err:
        app.logger.info('add_channel failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('add_channel failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('add_channel failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('add_channel failed with this error: ' + str(err))

    try:
        t = Thread(target=db_log_mod.add_log, args=(list_for_log, 'add channel'))
        t.start()

    except Exception as err:
        app.logger.info('Thread in add_channel failed with this error:' + str(err))


def search_channel(list_from_request: tuple, list_for_log: tuple) -> list:
    """
    Для поиска элемента по url в channel_tab.
    Применяется для поиска добавляемого через форму канала в БД.
    :param list_from_request: данные из запроса (url_channel, status_code, length_content, title_channel, url_site).
    :param list_for_log: данные для add_log.
    :return: кортеж с результатами поиска.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:  # попробовать вынести в function

            _SQL = """SELECT * FROM channel_tab WHERE url_channel_c=%s;"""

            cursor.execute(_SQL, (list_from_request[0],))
            contents = cursor.fetchall()

            return contents

    except ConnectionError as err:
        app.logger.info('search_channel failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_channel failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_channel failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_channel failed with this error: ' + str(err))


def remove_channel_by_id(id: int) -> None:
    """
    Удаление выбранного элемента из channel_tab по id.
    :param id: id удаляемого элемента в channel_tab.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """DELETE FROM channel_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))

    except ConnectionError as err:
        app.logger.info('db_rss_mod.remove_channel_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('db_rss_mod.remove_channel_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('db_rss_mod.remove_channel_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('db_rss_mod.remove_channel_by_id failed with this error: ' + str(err))


def update_channel(list_from_request: tuple, list_for_log: tuple) -> None:
    """
    Обновление данных для изменённого элемента в channel_tab.
    :param list_from_request: данные из запроса (url_channel, status_code, length_content, title_channel, url_site).
    :param list_for_log: данные для add_log.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """UPDATE channel_tab SET
                      status_code=%s,
                      length_content=%s,
                      title_channel=%s,
                      url_site=%s
                      WHERE
                      url_channel_c=%s;"""

            cursor.execute(_SQL, (list_from_request[1],
                                  list_from_request[2],
                                  list_from_request[3],
                                  list_from_request[4],
                                  list_from_request[0]))

    except ConnectionError as err:
        app.logger.info('update_channel failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('update_channel failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('update_channel failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('update_channel failed with this error: ' + str(err))

    try:
        t = Thread(target=db_log_mod.add_log, args=(list_for_log, 'update channel'))
        t.start()

    except Exception as err:
        app.logger.info('Thread in update_channel failed with this error:' + str(err))


def update_timestamp(list_from_request: tuple, list_for_log: tuple) -> None:
    """
    Для обновления timestamp элемента в channel_tab. Без измененя остальных данных.
    :param list_from_request: данные из запроса (url_channel, status_code, length_content, title_channel, url_site).
    :param list_for_log: данные для add_log.
    :return: None.
    """

    temp_status = 999  # Костыль для обновлеия timestamp.

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """UPDATE channel_tab SET
                      status_code=%s
                      WHERE
                      url_channel_c=%s;"""

            cursor.execute(_SQL, (temp_status,
                                  list_from_request[0]))

            _SQL = """UPDATE channel_tab SET
                      status_code=%s
                      WHERE
                      url_channel_c=%s;"""

            cursor.execute(_SQL, (list_from_request[1],
                                  list_from_request[0]))

    except ConnectionError as err:
        app.logger.info('update_timestamp failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('update_timestamp failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('update_timestamp failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('update_timestamp failed with this error: ' + str(err))

    try:
        t = Thread(target=db_log_mod.add_log, args=(list_for_log, 'update timestamp'))
        t.start()

    except Exception as err:
        app.logger.info('Thread in update_timestamp failed with this error:' + str(err))


def show_channel() -> list:
    """
    Отоброжает содержимое channel_tab.
    :return: список кортежей со всеми данными из таблицы.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:  # попробовать *

            _SQL = """SELECT * FROM channel_tab ORDER BY id DESC LIMIT 1000;"""

            cursor.execute(_SQL)
            contents = cursor.fetchall()

        return contents

    except ConnectionError as err:
        app.logger.info('show_channel failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('show_channel failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('show_channel failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('show_channel failed with this error: ' + str(err))


def show_channel_restrict() -> list:  # попробавать убрать
    """
    Отоброжает содержимое channel_tab.
    :return: список кортежей с некоторыми данными из таблицы.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT id, url_site, title_channel, ts
                      FROM channel_tab ORDER BY ts DESC LIMIT 1000;"""

            cursor.execute(_SQL)
            contents = cursor.fetchall()

        return contents

    except ConnectionError as err:
        app.logger.info('show_channel_restrict failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('show_channel_restrict failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('show_channel_restrict failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('show_channel_restrict failed with this error: ' + str(err))


def search_channel_by_id(id: int) -> bool:
    """
    Поиск выбранного элемента в channel_tab по id.
    :param id: id искомого элемента в channel_tab.
    :return: возращает True если находит элемент, и False если нет.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT * FROM channel_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))
            contents = cursor.fetchall()

            if not contents:
                return False
            else:
                return True

    except ConnectionError as err:
        app.logger.info('search_channel_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_channel_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_channel_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_channel_by_id failed with this error: ' + str(err))


def get_url_channel_by_id(id: int) -> str:
    """
    Для поиска url_channel_c по id в channel_tab.
    :param id: id искомого элемента в channel_tab.
    :return: возвращает url_channel_c из channel_tab.
    """

    try:
        with DatabaseConnection(app.config['rss_db_config']) as cursor:

            _SQL = """SELECT url_channel_c FROM channel_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))
            contents = cursor.fetchone()

            return contents[0]

    except ConnectionError as err:
        app.logger.info('get_url_channel_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('get_url_channel_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('get_url_channel_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('get_url_channel_by_id failed with this error: ' + str(err))
