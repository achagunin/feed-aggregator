from webapp import app
from webapp.db_context_manager_mod import DatabaseConnection, ConnectionError, CredentialsError, SQLError


def search_user_by_login(login: str) -> list:
    """
    Для поиска элемента по логину в users_tab.
    :param login: login искомого элемента в users_tab.
    :return: список с результатом поиска.
    """

    try:
        with DatabaseConnection(app.config['users_db_config']) as cursor:

            _SQL = """SELECT * FROM users_tab WHERE login=%s;"""

            cursor.execute(_SQL, (login,))
            contents = cursor.fetchall()

            return contents

    except ConnectionError as err:
        app.logger.info('search_user_by_login failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_user_by_login failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_user_by_login failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_user_by_login failed with this error: ' + str(err))


def search_user_by_id(id: int) -> tuple:
    """
    Для поиска элемента по id в users_tab.
    :param id: id искомого элемента в users_tab.
    :return: список с результатом поиска.
    """

    try:
        with DatabaseConnection(app.config['users_db_config']) as cursor:

            _SQL = """SELECT * FROM users_tab WHERE id=%s;"""

            cursor.execute(_SQL, (id,))
            contents = cursor.fetchall()

            return contents

    except ConnectionError as err:
        app.logger.info('search_user_by_id failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('search_user_by_id failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('search_user_by_id failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('search_user_by_id failed with this error: ' + str(err))


def add_user_to_db(login: str, password_hash: str) -> None:
    """
    Добавляет юзера в users_tab.
    :param login: логин юзера.
    :param password_hash: хеш пароля.
    :return: None.
    """

    print("Проверка из add_user_to_db", login, password_hash)

    try:
        with DatabaseConnection(app.config['users_db_config']) as cursor:

            _SQL = """INSERT INTO users_tab
                      (login, password_hash)
                       VALUES
                      (%s, %s)"""

            cursor.execute(_SQL, (login,
                                  password_hash,))

    except ConnectionError as err:
        app.logger.info('add_user_to_db failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('add_user_to_db failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('add_user_to_db failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('add_user_to_db failed with this error: ' + str(err))


def remove_user_by_login(login: str) -> None:
    """
    Удаляет юзера из users_tab.
    :param login: логин юзера.
    :return: None.
    """

    print('Проверка из remove_user_by_login', login)

    try:
        with DatabaseConnection(app.config['users_db_config']) as cursor:

            _SQL = """DELETE FROM users_tab WHERE login=%s;"""

            cursor.execute(_SQL, (login,))

    except ConnectionError as err:
        app.logger.info('remove_user_by_login failed with this error: ConnectionError ' + str(err))
    except CredentialsError as err:
        app.logger.info('remove_user_by_login failed with this error: CredentialsError.' + str(err))
    except SQLError as err:
        app.logger.info('remove_user_by_login failed with this error: SQLError ' + str(err))
    except Exception as err:
        app.logger.info('remove_user_by_login failed with this error: ' + str(err))
