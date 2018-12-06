from werkzeug.security import check_password_hash  # generate_password_hash для генерации пароля
from flask_login import UserMixin
from webapp.db_users_mod import search_user_by_login, search_user_by_id


class User(UserMixin):
    """
    Класс необходимый для авторизации пользователей.
    """

    def __init__(self, login=None, id=None):
        if login:
            contents = search_user_by_login(login)
            if contents:
                self.id = contents[0][0]
                self.username = contents[0][1]
                self.password_hash = contents[0][2]
            else:
                self.id = None
                self.username = None
                self.password_hash = None

        elif id:
            contents = search_user_by_id(id)
            if contents:
                self.id = contents[0][0]
                self.username = contents[0][1]
                self.password_hash = contents[0][2]

            else:
                self.id = None
                self.username = None
                self.password_hash = None

    def check_password(self, password: str) -> bool:
        """
        Метод для проверки пароля.
        :param password: пароль введённый в форме авторизации.
        :return: Возращает True если пользователь с данным username существует в users_tab и пароль верен, False иначе.
        """
        if self.username:
            return check_password_hash(self.password_hash, password)  # True/False
        else:
            return False

