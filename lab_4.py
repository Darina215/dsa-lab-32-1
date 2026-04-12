from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Модель пользователя

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Главная страница

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html', user=current_user)


# Страница входа (GET)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


# Авторизация (POST)

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Все поля обязательны')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Пользователь не найден')
        return redirect(url_for('login'))

    if not check_password_hash(user.password, password):
        flash('Неверный пароль')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('index'))


# Страница регистрации (GET)

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


# Регистрация (POST)

@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        flash('Все поля обязательны')
        return redirect(url_for('signup'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Пользователь уже существует')
        return redirect(url_for('signup'))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


# Выход

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Запуск

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)