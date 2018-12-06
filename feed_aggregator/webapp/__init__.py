from flask import Flask

# для авторизации
from flask_login import LoginManager

# для логера
import os
import logging
from logging.handlers import RotatingFileHandler

# считывание настроек
from webapp import config_mod

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKeyForSiteInformer'
app.config['settings'] = config_mod.read_config(section='settings')
app.config['rss_db_config'] = config_mod.read_config(section='rss_db_config')
app.config['log_db_config'] = config_mod.read_config(section='log_db_config')
app.config['users_db_config'] = config_mod.read_config(section='users_db_config')


login = LoginManager(app)
login.login_view = 'do_login'  # для проверки авторизации при просмотре страниц

from webapp import routes_mod  # должен быть ниже строки: app = Flask(__name__)


# Ведение журнала ошибок
if app.config['settings']['error_log'] == 'ON':

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/feed_aggregator.log', maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('feed_aggregator startup')


