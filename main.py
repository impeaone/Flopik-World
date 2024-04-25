import sys
import json

import requests
from flask import Flask, render_template, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from requests import get

from data import minecraft
from data import statistic_api
from data import db_session
from data.users import User
from data.users_uuid import User_uuid
from data.departments import Department
from data.depart_form import AddDepartForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(statistic_api.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/main", methods=["GET", "POST"])
def main_():
    if request.method == 'GET':
        return render_template('main.html')


@app.route("/")
def pusto_():
    return redirect("/main")


@app.route('/register', methods=["GET", "POST"])
def register():
    db_sess = db_session.create_session()
    if request.method == 'GET':
        return render_template('reg.html')
    elif request.method == 'POST':
        if not request.form['email'] and not request.form['password'] and not request.form['name']:
            return redirect('/register')

        user = User(
            name=request.form['name'],
            about=request.form["about"],
            email=request.form['email'],
        )
        user.set_password(request.form['password'])
        db_sess.add(user)
        db_sess.commit()
        print(request.form['name'])
        try:
            minecraft.add_player(str(request.form['name']))
            with open('MinecraftServer/whitelist.json', 'r') as jsonf:
                f = json.load(jsonf)

                for i in f:
                    if i["name"].lower() == request.form['name'].lower():
                        uuid = User_uuid(
                            name=request.form['name'],
                            uuid=i["uuid"],
                        )
                        db_sess.add(uuid)
                        db_sess.commit()

        except ConnectionError:
            return redirect('/login')

        return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("log.html", message="")
    elif request.method == "POST":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == request.form['email']).first()
        print(user.name)
        if user and user.check_password(request.form['password']):
            return redirect(f'/profile/{user.name}/{request.form['password']}')
        return render_template('log.html', message="Неверная почта или неправильльный пароль")
    return redirect("/")


@app.route('/profile/<string:nick>/<string:passs>')
def profile(nick, passs):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == nick).first()
    print(user.hashed_password)
    if user.check_password(passs):
        return render_template('profile.html', data=[user.name,user.email, user.about])
    else:
        return redirect("/")


@app.route('/add_news', methods=['GET', 'POST'])
def add_depart():
    add_form = AddDepartForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = Department(
            title=add_form.title.data,
            chief=add_form.chief.data,
            members=add_form.members.data,
            email=add_form.email.data
        )
        db_sess.add(depart)
        db_sess.commit()
        return redirect('/news')
    return render_template('add_depart.html', title='Adding a News', form=add_form)


@app.route("/news")
def depart():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    print(departments)
    users = db_sess.query(User).all()
    names = {name.id: name.name for name in users}
    return render_template("departments.html", departments=departments, names=names,
                           title='List of News')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_edit(id):
    form = AddDepartForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (
                                                          current_user.id == 1)).first()
        print(depart)
        if depart:
            form.title.data = depart.title
            form.chief.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (
                                                          current_user.id == 1)).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_depart.html', title='News Edit', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_delete(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Department).filter(Department.id == id,
                                              (Department.chief == current_user.id) | (
                                                      current_user.id == 1)).first()
    print(depart)
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    main()
