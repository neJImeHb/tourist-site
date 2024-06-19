from flask import Flask, render_template, g, request, flash, url_for, redirect, message_flashed, abort, session
import sqlite3
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


DEBUG = True
DATABASE = "instance/tour_site_db.db"

administrator = ["viktorvoytovich2008@gmail.com", "trovo1100@gmail.com"]

def query_db(query, args=(), one=False):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, args)
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    return (results[0] if results else None) if one else results

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tour_site_db.db'
app.config['SECRET_KEY'] = 'fdger2232rdfdfbg@31231fddasss'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_1 = db.Column(db.String(50))
    name_2 = db.Column(db.String(50))
    name_3 = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    psw = db.Column(db.String(50))

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    h_name_1 = db.Column(db.String(50))
    h_name_2 = db.Column(db.String(50))
    h_name_3 = db.Column(db.String(50))
    h_email = db.Column(db.String(120))
    h_theme = db.Column(db.String(50))
    h_quest = db.Column(db.Text(50000))
    h_date = db.Column(db.DateTime, default=datetime.utcnow)
    h_answer = db.Column(db.Text(50000), nullable=True)
    h_admin_name_1 = db.Column(db.String(50), nullable=True)
    h_admin_name_2 = db.Column(db.String(50), nullable=True)


    def __repr__(self):
        return "<Questions %r>" % self.id

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    o_name_1 = db.Column(db.String(50))
    o_name_2 = db.Column(db.String(50))
    o_name_3 = db.Column(db.String(50))
    o_email = db.Column(db.String(120)) 
    o_place = db.Column(db.String(120)) 
    o_house = db.Column(db.String(50))
    o_time = db.Column(db.String(50))
    o_people = db.Column(db.String(50))
    o_transport = db.Column(db.String(50))
    o_sum = db.Column(db.String(50))
    o_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Orders %r>" % self.id
    
class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(50))

    def __repr__(self):
        return "<Places %r>" % self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin):
    def __init__(self, user_id, email, password, name_1, name_2, name_3):
        self.id = str(user_id)  
        self.email = email
        self.password = password
        self.name_1 = name_1
        self.name_2 = name_2
        self.name_3 = name_3

    def get_id(self):
        return self.id
    
    def get_auth_token(self):
        return self.email + '|' + self.password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, psw, name_1, name_2, name_3 FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5])
        return user
    return None


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/message", methods=["POST", "GET"])
def message():
    current_user_email = current_user.email

    user_queries = Questions.query.order_by(Questions.h_date.desc()).filter_by(h_email=current_user_email).all()
    return render_template("message.html", user_queries=user_queries)

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/karpats", methods=["POST", "GET"])
def karpats():
    place = Places.query.filter_by(id=1).all()
    return render_template("karpats.html", place=place)

@app.route("/test", methods=["POST", "GET"])
@login_required
def test():
    if request.method == 'POST':
        p_name = request.form['p_name']

        place = Places(p_name=p_name)
        
        try:
            db.session.add(place)
            db.session.commit()
            return redirect(url_for('test'))
        except:
            return "Помилка"
    else:
        return render_template("test.html", administrator=administrator)

@app.route("/faroe_island")
def faroe():
    place = Places.query.filter_by(id=2).all()
    return render_template("faroe.html", place=place)

@app.route("/switzerland")
def switzerland():
    place = Places.query.filter_by(id=3).all()
    return render_template("switzerland.html", place=place)

@app.route("/iceland")
def iceland():
    place = Places.query.filter_by(id=4).all()
    return render_template("iceland.html", place=place)

@app.route("/poland")
def poland():
    place = Places.query.filter_by(id=5).all()
    return render_template("poland.html", place=place)

@app.route("/sweden")
def sweden():
    place = Places.query.filter_by(id=6).all()
    return render_template("sweden.html", place=place)

@app.route("/ticket")
def ticket():
    return render_template("ticket.html")

@app.route("/have_tour")
def have_tour():
    return render_template("have_tour.html")

@app.route("/cost_tarifs")
def cost_tarifs():
    return render_template("cost_tarifs.html")

@app.route("/when_armor")
def when_armor():
    return render_template("when_armor.html")

@app.route("/documents_tour")
def documents_tour():
    return render_template("documents_tour.html")

@app.route("/save_tour")
def save_tour():
    return render_template("save_tour.html")

@app.route("/problems_tour")
def problems_tour():
    return render_template("problems_tour.html")

@app.route("/change_armor")
def change_armor():
    return render_template("change_armor.html")

@app.route("/individuality")
def individuality():
    return render_template("individuality.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/help_success")
def help_success():
    return render_template("help_success.html")

@app.route("/order_success")
def order_success():
    return render_template("order_success.html")

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/history_request')
@login_required
def history_request():
    user_queries = Questions.query.order_by(Questions.h_date.desc()).all()
    return render_template("history_request.html", user_queries=user_queries, administrator=administrator)

@app.route('/requests_help')
@login_required
def requests_help():
    current_user_email = current_user.email

    # Получаем запросы в тех. поддержку для текущего пользователя
    user_queries = Questions.query.order_by(Questions.h_date.desc()).filter_by(h_email=current_user_email).all()

    return render_template('requests_help.html', user_queries=user_queries)


@app.route('/requests_help/<int:id>')
@login_required
def requests_help_detail(id):
    user_queries = Questions.query.get(id)
    currentDate = user_queries.h_date.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('requests_help_detail.html', user_queries=user_queries, currentDate=currentDate, administrator=administrator)

@app.route('/answer/<int:id>', methods=["GET", "POST"])
@login_required
def answer(id):
    question = Questions.query.get(id)

    if not question:
        return "Запит не знайдений"

    if request.method == "POST":
        h_answer = request.form["h_answer"]

        if question.h_answer:
            question.h_answer += "\n" + h_answer
        else:
            question.h_answer = h_answer

        question.h_admin_name_1 = current_user.name_1
        question.h_admin_name_2 = current_user.name_2

        try:
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('success_admin'))
        except Exception as e:
            print(e)  # Выводим ошибку для отладки
            return "Произошла ошибка при обновлении записи"
    else:
        return render_template("answer.html", question=question)

@app.route('/success_admin')
def success_admin():
    return render_template('/success_admin.html')

@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    user_queries = Questions.query.order_by(Questions.h_date.desc()).all()

    return render_template("admin.html", user_queries=user_queries, administrator=administrator)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["psw"]
        remember = request.form.get("remember", False)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, psw FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()
        if not is_valid_email(email):
            flash("Пошта повинна мати в собі символ '@'", category="flash3")
        elif not len(password) >= 8:
            flash("Мінімальна довжина паролю: 8 символів", category="flash4")
        else:
            if user_data and password == user_data[2]:
                user = User(user_data[0], user_data[1], user_data[2], '', '', '')
                login_user(user, remember=remember)
                flash("Вход выполнен успешно", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Пара почта/пароль не совпадают", "error")

    return render_template("login.html")


def is_valid_email(email):
    return '@' in email


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # Инициализация переменных
    name_1 = ''
    name_2 = ''
    name_3 = ''
    email = ''
    psw = ''

    if request.method == 'POST':
        name_1 = request.form['name_1']
        name_2 = request.form['name_2']
        name_3 = request.form['name_3']
        email = request.form['email']
        psw = request.form['psw']

        if not is_valid_email(email):
            flash("Пошта повинна мати в собі символ '@'", category="flash3")
        elif not len(psw) >= 8:
            flash("Мінімальна довжина паролю: 8 символів", category="flash4")
        else:
            # Проверка наличия совпадений в базе данных
            duplicate_found = False
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT name_2 FROM users')
                cursor.execute('SELECT email FROM users')
                names = cursor.fetchall()

            for name in names:
                result = name[0]
                if name_2 == result:
                    duplicate_found = True
                    flash("Така фамілія вже існує", category="flash1")
                    break

            for name in names:
                result = name[0]
                if email == result:
                    duplicate_found = True
                    flash("Така пошта вже існує", category="flash2")
                    break


            if not duplicate_found:
                # Вставляем данные в базу данных
                query = "INSERT INTO users (email, psw, name_1, name_2, name_3) VALUES (?, ?, ?, ?, ?)"
                query_db(query, (email, psw, name_1, name_2, name_3))
                return redirect(url_for('success'))

    return render_template('sign_up.html', name_1=name_1, name_2=name_2, name_3=name_3, email=email, psw=psw)

@app.route("/help", methods=['GET', 'POST'])
@login_required
def help():
    if request.method == 'POST':
        h_theme = request.form['h_theme']
        h_quest = request.form['h_quest']

        questions = Questions(h_name_1=current_user.name_1, h_name_2=current_user.name_2, h_name_3=current_user.name_3, h_email=current_user.email, h_theme=h_theme, h_quest=h_quest)

        try:
            db.session.add(questions)
            db.session.commit()
            return redirect(url_for('help_success'))
        except:
            return "При додаванні статті відбулась помилка"
    else:
        return render_template("help.html")

@app.route("/order/<int:id>", methods=["POST", "GET"])
@login_required
def order(id):
    place = Places.query.get(id)

    if request.method == "POST":
        o_house = request.form['o_house']
        o_time = request.form['o_time']
        o_people = request.form['o_people']
        o_transport = request.form['o_transport']
        o_sum_text = request.form.get('o_sum', '0₴')
        o_sum = int(o_sum_text.replace('₴', ''))

        order = Orders(o_name_1=current_user.name_1, o_name_2=current_user.name_2, o_name_3=current_user.name_3, o_email=current_user.email, o_place=place.p_name, o_house=o_house, o_time=o_time, o_people=o_people, o_transport=o_transport, o_sum=o_sum)

        try:
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('order_success'))
        except:
            return f"{o_house}, {o_time}, {o_people} При додаванні статті відбулась помилка"
    else:
        return render_template("order.html", place=place)

@app.route("/order_history", methods=["POST", "GET"])
@login_required
def order_history():
    user_queries = Orders.query.order_by(Orders.o_date.desc()).filter_by(o_email=current_user.email).all()
    return render_template("order_history.html", user_queries=user_queries)

@app.route('/order_history/<int:id>')
@login_required
def order_history_detail(id):
    user_queries = Orders.query.get(id)
    currentDate = user_queries.o_date.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('order_history_detail.html', user_queries=user_queries, currentDate=currentDate, administrator=administrator)

@app.route('/process-selection', methods=['POST', 'GET'])
def process_selection():
    selected_option = request.form['option']
    result = f"{selected_option}"
    return result

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
     

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
