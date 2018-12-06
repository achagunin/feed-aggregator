"""Модуль для добавления новых пользователей. Запускать отдельно."""

from werkzeug.security import generate_password_hash
from webapp import app, db_users_mod


def add_user(login: str, password_1: str, password_2: str) -> None:
    """
    Функция добавления нового пользователя в users_tab.
    :param login: строка для логина
    :param password_1: строка для пароля
    :param password_2: строка для пароля
    :return: None.
    """
    if password_1 == password_2:

        if not db_users_mod.search_user_by_login(login):
            password_hash = generate_password_hash(password_1)
            print('Хэш пароля: ', password_hash, len(password_hash))
            db_users_mod.add_user_to_db(login, password_hash)

            if db_users_mod.search_user_by_login(login):
                print('User с логином {} успешно добавлен'.format(login))
            else:
                print('Не удалось добавить User с логином {}'.format(login))
        else:
            print('User с логином {} уже есть.'.format(login))
    else:
        print('Вы ошиблись при наборе пароля.')


def remove_user(login: str) -> None:
    """
    Удаляет пользователя с указанным логином из users_tab.
    :param login: строка логина пользователя.
    :return: None.
    """

    if db_users_mod.search_user_by_login(login):
        db_users_mod.remove_user_by_login(login)

        if not db_users_mod.search_user_by_login(login):
            print('User с логином {} успешно удалён.'.format(login))
        else:
            print('Не удалось удалить User с логином {}'.format(login))
    else:
        print('User с логином {} не существует'.format(login))


operation = input('Введите add что бы добавить пользователя, или remove что бы удалить: ')

if operation == 'add':
    login = input('Введите желаемый логин: ')
    password_1 = input('Введите пароль: ')
    password_2 = input('Повторите пароль: ')
    add_user(login, password_1, password_2)
elif operation == 'remove':
    login = input('Введите логин удаляемого пользователя: ')
    remove_user(login)
else:
    print('Некорректная операция.')



