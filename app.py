from flask import Flask, render_template, request, flash, redirect
from data.db_session import global_init, create_session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash
from data.login import LoginForm
from data.register import RegisterForm
from data.users import Users
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
global_init("db/apelsin.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)


def api_location():
    import requests

    map_request = "http://static-maps.yandex.ru/1.x/?ll=30.460838,59.908141&spn=0.009,0.009&l=map&pt=30.459679,59.906147,org~30.455727,59.909856,org"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "static/image/map.png"
    file = open(map_file, "wb")
    file.write(response.content)
    file.close()


api_location()


@app.route('/')
@app.route('/index')
def index():
    print(current_user)
    return render_template('index.html', title='Домашняя страница',
                           style_file='/static/css/style.css', user=current_user)


@app.route('/time_table')
def time_table():
    return render_template('time_table.html', title='Расписание', style_file='/static/css/style_for_courses.css')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакты', style_file='/static/css/style_for_courses.css')


@app.route('/courses')
def courses():
    return render_template('courses.html', title='Курсы', style_file='/static/css/style_for_courses.css')


@app.route('/price')
def price():
    return render_template('price.html', title='Цены', style_file='/static/css/style_for_courses.css')


@app.route('/lesson')
def lesson():
    try:
        print('register')
        form = RegisterForm()
        if request.method == 'POST' and form.validate():
            db_sess = create_session()
            user = Users()
            print('register2')
            if type(form.day.data) is datetime.date:
                print('register3')
                user.name, user.lesson, user.day = current_user, form.lesson.data, form.day.data
                db_sess.add(user)
                db_sess.commit()
                return redirect('/')
            else:
                return render_template('lesson.html', form=form, title='Запись', message='Дата введена неправильно',
                                       style_file='/static/css/style_for_courses.css')
        return render_template('lesson.html', form=form, title='Запись',
                               style_file='/static/css/style_for_courses.css')
    except Exception:
        message = "Возникла ошибка при обработке формы"
        return render_template('lesson.html', form=form, title='Запись', message=message,
                               style_file='/static/css/style_for_courses.css')


@app.route('/performances')
def performances():
    return render_template('performances.html', title='Выступления', style_file='/static/css/style_for_courses.css')


@app.route('/teachers')
def teachers():
    conn = sqlite3.connect('db/apelsin.sqlite')
    cur = conn.cursor()
    cur.execute("""select surname, photo, about from teachers""")
    dct = []
    for surname, photo, about  in cur.fetchall():
        dct.append({'name': surname, 'foto': photo, 'about': about})
    context = {'dct': dct}
    conn.close()
    return render_template('teachers.html', style_file='/static/css/style_for_courses.css', title='Учителя', **context)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            db_sess = create_session()
            user = db_sess.query(Users).filter(Users.email == form.email.data).first()
            print(user, user.password, form.password.data)
            if user and user.password == form.password.data:
                login_user(user, remember=form.remember_me.data)
                return redirect("/index")
            return render_template('login.html', style_file='/static/css/style_for_courses.css',
                                   message="Неправильный логин или пароль", form=form)
    except Exception as Ex:
        return render_template('login.html', title='Авторизация',
                               message="Такого пользователя нет в базе данных, зарегистрируйтесь!",
                               style_file='/static/css/style_for_courses.css', form=form)
    return render_template('login.html', style_file='/static/css/style_for_courses.css', form=form)


@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    try:
        form = RegisterForm()
        if request.method == 'POST' and form.validate():
            db_sess = create_session()
            user = Users()
            user.name, user.email, user.password = form.name.data, form.email.data, form.password.data
            db_sess.add(user)
            db_sess.commit()
            flash('Спасибо за регистрацию')
            if user:
                login_user(user, remember=form.remember_me.data)
                return redirect("/index")
            return redirect('/')
        # если HTTP-метод GET, то просто отрисовываем форму
        return render_template('sign_up.html', form=form, title='Вход',
                               style_file='/static/css/style_for_courses.css')
    except Exception:
        message = 'Этот логин уже занят'
        return render_template('sign_up.html', form=form, title='Вход', message=message,
                               style_file='/static/css/style_for_courses.css')


if __name__ == '__main__':
    app.run()
