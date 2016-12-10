from flask import Flask

from login.views import login

app = Flask(__name__)

app.register_blueprint(login)
if __name__ == '__main__':
    app.run(debug=True)
