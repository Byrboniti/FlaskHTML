from contextlib import closing
from FDataBase import *
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import sqlite3
import os

DATABASE = 'D:/PythonProjects/Flask/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'asjdiu1iuf12j'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    db = get_db()
    dbase = FDateBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts= dbase.getPostsAnonce())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db

@app.route('/add_post', methods= ['POST','GET'])
def addPost():
    db = get_db()
    dbase = FDateBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'],request.form['post'],request.form['url'])
            if not res:
                flash('Ошбика добавления статьи', category='error')
            else:
                flash('успех', category='success')
        else:
            flash('Ошбика добавления статьи', category='error')

    return render_template('add_post.html', menu = dbase.getMenu(), title= 'Добавление статьи')

@app.route('/post/<alias>')
def showPost(alias):
    db = get_db()
    dbase = FDateBase(db)
    title = dbase.getPost(alias)
    post = dbase.getPost(alias)

    if not title:
        abort(404)
    return render_template('post.html', menu= dbase.getMenu(),title= title, post= post)


if __name__ == '__main__':
    app.run(debug=True)















# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'asjdiu1iuf12j'
# menu = [
#     {"name": "установка", "url": "install-flask"},
#     {"name": "первое приложение", "url": "first-app"},
#     {"name": "обратная связь", "url": "contact"}
# ]
#
#
# @app.route("/")
# def index():
#     print(url_for('index'))
#     return render_template("index.html", menu=menu)
#
#
# @app.route("/contact", methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         if len(request.form['username']) > 2:
#             flash('massage send')
#         else:
#             flash('ERROR send')
#
#     return render_template('contact.html', title="contact", menu=menu)
#
#
# @app.route("/about")
# def about():
#     print(url_for('about'))
#     return render_template("about.html", title="about site", menu=menu)
#
#
# @app.route('/profile/<username>')
# def profile(username, ):
#     return f'User: {username},'
#
#
# @app.errorhandler(404)
# def pageNotFount(error):
#     return render_template('page404.html', title='Старница не найдена', menu=menu),
#
#
# # with app.test_request_context():
# #     print(url_for('index'))
# #     print(url_for('about'))
# #     print(url_for('profile', username= 'selfed'))
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('pofile', username=session['userLogged']))
#
#     elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == '123':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     return render_template('login.html', title='Авторизация', menu=menu)
#
#
# @app.route('/profile/<username>')
# def profile(username):
#     if 'userLogged' not in session or ['userLogged'] != username:
#         abort(401)
#     return f'Профиль пользователя {username}'
#
#

