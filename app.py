<<<<<<< HEAD
from flask import Flask, render_template
import sqlite3
=======
from flask import Flask, render_template, request, flash, redirect
from data.db_session import global_init, create_session
from flask_login import LoginManager
from data.login import LoginForm
from data.register import RegisterForm
from data.users import Users

>>>>>>> origin/main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
global_init("db/apelsin.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


<<<<<<< HEAD
@app.route('/courses.html')
=======
@app.route('/courses')
>>>>>>> origin/main
def courses():
    return render_template('courses.html')


<<<<<<< HEAD
@app.route('/performances.html')
=======
@app.route('/performances')
>>>>>>> origin/main
def performances():
    return render_template('performances.html')


<<<<<<< HEAD
@app.route('/teachers.html')
def teachers():
    conn = sqlite3.connect('apelsin.sqlite')
    cur = conn.cursor()
    cur.execute("""select name, foto from teachers""")
    dct = []
    for name, foto in cur.fetchall():
        dct.append({'name': name, 'foto': foto})
    context = {'dct': dct}
    conn.close()
    return render_template('teachers.html', **context)


=======
@app.route('/teachers')
def teachers():
    return render_template('teachers.html')


@app.route('/health_issues')
def doctors():
    return render_template('teachers.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        db_sess = create_session()
        user = Users()
        user.name, user.email, user.hashed_password = form.name.data, form.email.data, form.password.data
        db_sess.add(user)
        db_sess.commit()
        flash('Спасибо за регистрацию')
        return redirect('/')
    # если HTTP-метод GET, то просто отрисовываем форму
    return render_template('sign_up.html', form=form)


#{% if user.is_authenticated %}
 #           <a href="/logout">Выйти</a>
  #          {% else %}
   #         <a href="/login">Войти</a>
    #        {% endif %}
>>>>>>> origin/main
if __name__ == '__main__':
    app.run()
