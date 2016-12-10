import flask
import flask_login
from flask import Flask
from flask import render_template
from flask.ext.admin import Admin
from flask.ext.login import LoginManager

from models import User

app = Flask(__name__)
admin = Admin(app, name='自动化运维平台', template_mode='bootstrap3')
app.secret_key = 'AutoOps'

# app.register_blueprint(login)

login_manager = LoginManager()

login_manager.init_app(app)

users = {'admin': {'password': 'admin'}}


@login_manager.user_loader
def user_loader(username):
    app.logger.debug("加载用户名{}".format(username), )

    if username not in users:
        app.logger.debug("加载用户信息失败，无该用户")
        return

    user = User()
    user.id = username
    app.logger.debug("加载用户成功")
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    user.is_authenticated = request.form['password'] == users[username]['password']

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    error = None
    username = flask.request.form['username']
    if username in users and flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        app.logger.info("用户{}登录成功".format(username))
        return flask.redirect(flask.url_for('admin.index'))
    else:
        app.logger.debug("登录失败，用户名密码不匹配")
        error = "登录失败"
        return render_template('login.html', error=error)


@app.route('/protected')
@flask_login.login_required
def protected():
    return '登录成功: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return '登出'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return '未认证'


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
