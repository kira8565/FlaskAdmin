from flask import Blueprint
from flask import app

# from login import login
from flask import render_template

login = Blueprint('login', __name__,
                  template_folder="./templates",
                  static_folder="../static")


@login.route('/')
def index():
    return render_template("login.html")
