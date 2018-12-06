from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователей.
    """
    username = wtforms.StringField('Логин', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[wtforms.validators.DataRequired()])
    remember_me = wtforms.BooleanField('Запомнить меня')
    submit = wtforms.SubmitField('Войти')


class URLForm(FlaskForm):
    """
    Форма для ввода URL RSS-канала.
    """
    url_address = wtforms.StringField('URL', validators=[wtforms.validators.URL()])
    render_kw = {"placeholder": "http://www.example.com/rss"}
    submit = wtforms.SubmitField('Добавить')


class IDForm(FlaskForm):
    """
    Форма для ввода id элементов БД.
    """
    id = wtforms.IntegerField('ID', validators=[wtforms.validators.NumberRange(min=1)])
    submit = wtforms.SubmitField('Удалить')


class TextSearchForm(FlaskForm):
    """
    Форма для поиска по тексту.
    """
    text = wtforms.StringField('Текст', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Искать')


class DateSearchForm(FlaskForm):
    """
    Форма для поиска по дате.
    """
    date = wtforms.DateField('Дата', validators=[wtforms.validators.DataRequired()])
    render_kw = {"placeholder": "ГГГГ-ММ-ДД"}
    submit = wtforms.SubmitField('Искать')


class ComplexSearchForm(FlaskForm):
    """
    Форма для поиска по тексту и дате.
    """
    text = wtforms.StringField('Текст', validators=[wtforms.validators.DataRequired()])
    date = wtforms.DateField('Дата', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Искать')