# -*- coding: utf-8 -*- # для поддержки кирилицы

from flask import render_template, request, send_from_directory, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import os

from webapp import app, db_rss_channel_mod, db_rss_item_mod, db_log_mod, function_mod
from webapp import login  # из init: login = LoginManager(app)
from webapp.forms_mod import LoginForm, URLForm, IDForm, TextSearchForm, DateSearchForm, ComplexSearchForm
from webapp.user_mod import User


@app.route('/favicon.ico')
def favicon() -> str:
    """
    Функция для отоброжения иконки в браузере.
    :return: Возвращает путь до иконки приложения.
    """

    try:
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    except Exception as err:
        app.logger.info('favicon failed with this error: ' + str(err))


@login.user_loader
def load_user(id: int):
    """
    Возвращает объект класса User по его id. Служебная функция flask_login.
    :param id: id юзера (id из users_tab).
    :return: объект класса User.
    """

    try:
        return User(id=id)

    except Exception as err:
        app.logger.info('load_user failed with this error: ' + str(err))


@app.errorhandler(404)
def not_found_error(error):
    """
    Пользовательский обработчик ошибок.
    Чтобы его объявить используется декоратор @errorhandler.
    :param error: вид ошибки.
    :return: Перенаправление на страницу заглушку.
    """

    return render_template('error.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def do_login() -> 'html':
    """
    Функция для отображения страницы авторизации пользователей (login.html).
    :return: Выводит HTML страницу.
    """
    try:
        if current_user.is_authenticated:
            # Когда пользователь уже вошел в систему, его перенаправит на страницу entry_page.html
            return redirect(url_for('entry'))

        form = LoginForm()

        if form.validate_on_submit():
            user = User(login=request.form['username'])

            if user.check_password(request.form['password']):
                login_user(user, remember=form.remember_me.data)
                flash('Вы авторизовались как {}'.format(form.username.data))
                next_page = request.args.get('next')

                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('entry')
                return redirect(next_page)

            flash('Неправильный логин или пароль')
            return redirect(url_for('do_login'))

        return render_template('login.html', the_title='Авторизация', the_form=form)

    except Exception as err:
        app.logger.info('do_login failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/logout')
def do_logout() -> 'html':
    """
    Функция для разлогинивания.
    :return: Выводит HTML страницу.
    """
    try:
        logout_user()
        flash('Вы разлогинились')
        return redirect(url_for('entry'))

    except Exception as err:
        app.logger.info('do_logout failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/', methods=['GET', 'POST'])
@app.route('/entry_page', methods=['GET', 'POST'])
def entry() -> 'html':
    """
    Функция для отображения главной страницы (entry_page.html).
    :return: Выводит HTML страницу.
    """

    try:
        form = URLForm()
        if form.validate_on_submit():
            url = form.url_address.data
            function_mod.do_search(url)

            return redirect(url_for('entry'))

        titles = ('URL сайта', 'Название канала', 'Дата обновленя', ' ', ' ',)
        channel_list = function_mod.channels_to_listdict()

        return render_template('entry_page.html',
                               the_title='Агрегатор RSS каналов',
                               the_row_titles=titles,
                               the_data=channel_list,
                               the_form=form)

    except Exception as err:
        app.logger.info('entry failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/channel_page', methods=['GET', 'POST'])
@login_required
def view_channel() -> 'html':
    """
    Функция для отображения страницы с БД каналов (channel_page.html).
    :return: Выводит HTML страницу.
    """

    try:
        contents = db_rss_channel_mod.show_channel()
        titles = ('ID', 'TIMESTAMP', 'URL_CHANNEL_C', 'STATUS_CODE', 'LENGTH_CONTENT', 'TITLE_CHANNEL', 'URL_SITE')

        form = IDForm()
        if form.validate_on_submit():
            id = form.id.data
            function_mod.remove_channel(id)
            return redirect(url_for('view_channel'))

        return render_template('channel_page.html',
                               the_title='БД каналов',
                               the_row_titles=titles,
                               the_data=contents,
                               the_form=form)

    except Exception as err:
        app.logger.info('view_channel failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/log_page', methods=['POST', 'GET'])
@login_required
def view_log() -> 'html':  # Переименовать
    """
    Функция для отображения страницы с БД статистики (log_page.html).
    :return: Выводит HTML страницу.
    """

    try:
        contents = db_log_mod.show_log()
        titles = ('ID', 'TIMESTAMP', 'OPERATION', 'URL', 'IP', 'BROWSER', 'OS')

        form = IDForm()
        if form.validate_on_submit():
            id = form.id.data
            function_mod.remove_log(id)
            return redirect(url_for('view_log'))

        return render_template('log_page.html',
                               the_title='Статистика',
                               the_row_titles=titles,
                               the_data=contents,
                               the_form=form)

    except Exception as err:
        app.logger.info('view_log failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/clear_log')
def clear_log() -> 'html':
    """
    Очистка журнала (log_tab).
    :return: Выводит HTML страницу.
    """

    try:
        db_log_mod.delete_all_log()
        flash('Журнал обращений очищен')
        return redirect(url_for('view_log'))

    except Exception as err:
        app.logger.info('clear_log failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/rss_page', methods=['GET', 'POST'])
@login_required
def view_rss() -> 'html':
    """
    Функция для отображения страницы с БД RSS-контента (rss_page.html).
    :return: Выводит HTML страницу.
    """

    try:
        contents = db_rss_item_mod.show_rss()
        titles = ('ID', 'URL_CHANNEL_R', 'TITLE_ITEM', 'SUMMARY_ITEM', 'URL_ITEM', 'PUBLISHED_ITEM')

        form = IDForm()
        if form.validate_on_submit():
            id = form.id.data
            function_mod.remove_rss(id)
            return redirect(url_for('view_rss'))

        return render_template('rss_page.html',
                               the_title='БД RSS',
                               the_row_titles=titles,
                               the_data=contents,
                               the_form=form)

    except Exception as err:
        app.logger.info('view_rss failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/update_channel/<id_channel>')
def update_channel(id_channel) -> 'html':
    """
    Функция для обновления содержимого канала при нажатии кнопки 'Обновить' на странице entry_page.html.
    :param id_channel: id канала, берётся из entry_page.html (channel_row['id']).
    :return: Выводит HTML страницу.
    """

    try:
        url_channel = db_rss_channel_mod.get_url_channel_by_id(id_channel)
        function_mod.do_search(url_channel)
        return redirect(url_for('entry'))

    except Exception as err:
        app.logger.info('search_channel failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/read_channel/<id_channel>')
def read_channel(id_channel) -> 'html':  # переименовать
    """
    Функция для отображения содержимого канала при нажатии кнопки 'Читать' на странице entry_page.html.
    :param id_channel: id канала, берётся из entry_page.html (channel_row['id']).
    :return: Выводит HTML страницу.
    """

    try:
        url_channel = db_rss_channel_mod.get_url_channel_by_id(id_channel)
        rss_list = function_mod.show_content(url_channel)

        return render_template('channel_rss.html',
                               the_title=url_channel,
                               the_data=rss_list,
                               )

    except Exception as err:
        app.logger.info('read_channel failed with this error: ' + str(err))
        return render_template('error.html'), 404


@app.route('/search_page', methods=['GET', 'POST'])
def search_rss() -> 'html':  # Переименовать
    """
    Функция для отображения страницы поиска (search_page.html).
    :return: Выводит HTML страницу.
    """

    try:
        text_form = TextSearchForm()
        date_form = DateSearchForm()
        complex_form = ComplexSearchForm()

        if complex_form.validate_on_submit():  # поиск по двум полям.
            complex_text = complex_form.text.data
            complex_date = complex_form.date.data
            search_list = function_mod.complex_search(complex_text, complex_date)

            if not search_list:
                flash('Поиск по тексту <{}>  и дате <{}> не дал результатов'.format(complex_text, complex_date))
                return redirect(url_for('search_rss'))

            return render_template('search_results.html',
                                   the_title=('Поиск по тексту <{}>  и дате <{}>'.format(complex_text, complex_date)),
                                   the_data=search_list,
                                   )

        if text_form.validate_on_submit():  # поиск по тексту.
            text = text_form.text.data
            search_list = function_mod.text_search(text)

            if not search_list:
                flash('Поиск по тексту <{}> не дал результатов'.format(text))
                return redirect(url_for('search_rss'))

            return render_template('search_results.html',
                                   the_title=('Поиск по тексту <{}>'.format(text)),
                                   the_data=search_list,)

        if date_form.validate_on_submit():  # поиск по дате.
            date = date_form.date.data
            search_list = function_mod.date_search(date)

            if not search_list:
                flash('Поиск по дате <{}> не дал результатов'.format(date))
                return redirect(url_for('search_rss'))

            return render_template('search_results.html',
                                   the_title=('Поиск по дате <{}>'.format(date)),
                                   the_data=search_list,)

        return render_template('search_page.html',
                               the_title='Поиск',
                               the_text_form=text_form,
                               the_date_form=date_form,
                               the_complex_form=complex_form,)

    except Exception as err:
        app.logger.info('search_page failed with this error: ' + str(err))
        return render_template('error.html'), 404
