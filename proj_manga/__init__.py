from proj_manga.mod_imports import *
from proj_manga.mod_init import init
# noinspection PyUnresolvedReferences
from flask import Flask
init()
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
#服务器每次重启都会自动生成新的secret key
app.secret_key ="12345" # randomSecretKey(64)
import proj_manga.views
