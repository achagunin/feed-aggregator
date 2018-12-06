from webapp import app
from webapp.db_context_manager_mod import DatabaseConnection, ConnectionError, CredentialsError, SQLError


def add_log(list_for_log: tuple, operation='error') -> None:
    """
    Добавляет элементы в log_tab.
    :param list_for_log: логируемые данные (url, ip, browser, os).
    :param operation: вид совершённой операции.
    :return: None
    """

    try:
        with DatabaseConnection(app.config['log_db_config']) as cursor:

            _SQL = """INSERT INTO log_tab
                      (operation, url, ip, browser, os)
                       VALUES
                      (%s, %s, %s, %s, %s);"""

            cursor.execute(_SQL, (operation,
                                  list_for_log[0],
                                  list_for_log[1],
                                  list_for_log[2],
                                  list_for_log[3],
                                  ))

    except ConnectionError as err:
        app.logger.info('add_log failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('add_log failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('add_log failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('add_log failed with this error: ' + str(err))


def remove_log(id: int) -> None:
    """
    Удаление выбранного элемента из log_tab по id.
    :param id: id удаляемого элемента в log_tab.
    :return: None
    """

    try:
        with DatabaseConnection(app.config['log_db_config']) as cursor:

            _SQL = """DELETE FROM log_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))

    except ConnectionError as err:
        app.logger.info('remove_log failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('remove_log failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('remove_log failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('remove_log failed with this error: ' + str(err))


def show_log() -> list:
    """
    Отоброжает содержимое log_tab.
    :return: список кортежей со всеми данными из таблицы.
    """

    try:
        with DatabaseConnection(app.config['log_db_config']) as cursor:

            _SQL = """SELECT * FROM log_tab ORDER BY ts DESC LIMIT 1000;"""

            cursor.execute(_SQL)
            contents = cursor.fetchall()

        return contents

    except ConnectionError as err:
        app.logger.info('show_log failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('show_log failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('show_log failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('show_log failed with this error: ' + str(err))


def search_log_by_id(id: int) -> bool:
    """
    Поиск выбранного элемента в log_tab по id.
    :param id: id искомого элемента в log_tab.
    :return: возращает True если находит элемент, и False если нет.
    """

    try:
        with DatabaseConnection(app.config['log_db_config']) as cursor:

            _SQL = """SELECT * FROM log_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))
            contents = cursor.fetchall()

            if not contents:
                return False
            else:
                return True

    except ConnectionError as err:
        app.logger.info('search_log_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_log_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_log_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_log_by_id failed with this error: ' + str(err))


def delete_all_log() -> None:
    """
    Удаляет все записи в таблице log_tab и сбрасывает id на 1.
    :return: None.
    """

    try:
        with DatabaseConnection(app.config['log_db_config']) as cursor:

            _SQL = """DELETE FROM log_tab;"""

            cursor.execute(_SQL)

            _SQL = """ALTER TABLE log_tab AUTO_INCREMENT = 1;"""

            cursor.execute(_SQL)

    except ConnectionError as err:
        app.logger.info('delete_all_log failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('delete_all_log failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('delete_all_log failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('delete_all_log failed with this error: ' + str(err))
