"""Модуль диспетчера контекста баз данных"""

import mysql.connector


# Собственные "пустые" классы исключений, наследующий Exception.


class ConnectionError(Exception):
    """
    При проблемах с подключением к БД.
    """
    pass


class CredentialsError(Exception):
    """
    При проблемах с регистрацией (имя пользователя пароль MySQL).
    """
    pass


class SQLError(Exception):
    """
    При возникновении ошибки внутри блока with DatabaseConnection
    Перехватывается в конце блока __exit__.
    """
    pass


class DatabaseConnection:
    """
    Диспетчер контекста базы данных.
    """

    def __init__(self, config: dict) -> None:
        """
        Принимает на вход словарь с параметрами подключения.
        """
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """
        Создаёт подключение к БД, используя параметры self.configuration.
        """
        try:
            self.conn = mysql.connector.connect(**self.configuration)  # Установка соеденения.
            self.cursor = self.conn.cursor()  # Cоздаём курсор (дескриптер для соеденения).
            return self.cursor

        # Ссылаемся на исключения для конкректной БД, по их полным именам.
        # И в ответ на это вызываем собственные исключения.
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)

        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """
        Подтверждает запись данных в БД, а затем закрывает курсор
        и соединение.
        """
        self.conn.commit()  # Заставляем записать кэшированные данные в таблицу
        self.cursor.close()
        self.conn.close()

        # Если возникло ProgrammingError возбуждаем SQLError.
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        # Повторно возбуждаем любое другое исключение которое может возникнуть.
        elif exc_type:
            raise exc_type(exc_value)