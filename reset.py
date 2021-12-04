from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = '/=q3|40~$<l?6($!g$0|'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/site'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

sqlconnection = psycopg2.connect(
    database="site",
    user="postgres",
    host="localhost",
    password="password"
)
cursor = sqlconnection.cursor()


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, autoincrement=True)
    fname = db.Column(db.String(50), primary_key=True, nullable=False)
    sname = db.Column(db.String(50), primary_key=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Columnes(db.Model):
    __tablename__ = 'columnes'
    id = db.Column(db.Integer, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    sname = db.Column(db.String(50), nullable=False)
    mark = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(100), primary_key=True, nullable=False)
    link_image = db.Column(db.String(100), nullable=False)
    name_music = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Columnes %r>' % self.id


class Article(db.Model):
    __tablename__ = 'Articles'
    id = db.Column(db.Integer, autoincrement=True)
    name_music = db.Column(db.String(100), primary_key=True, nullable=False)
    cfname = db.Column(db.String(50), nullable=False)
    csname = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(100), nullable=False)
    cmark = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        fname = request.form["fname"]
        sname = request.form["sname"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]
        rep_password = request.form["rep_password"]
        if not (fname or sname or age or email or password or rep_password):
            flash("Please , fill all fields!")
        elif len(password) < 6 or password != rep_password:
            flash("Password is incorrect!")
        else:
            hash1 = generate_password_hash(password)
            user = User(fname=fname, sname=sname, age=age, email=email, password=hash1)
            db.session.add(user)
            db.session.commit()
            return redirect('/home')
    else:
        return render_template('sign-up.html')


@app.route('/home')
def home():  # put application's code here
    articles = "select cmark from Articles " \
               "Order by cmark"
    return render_template('index.html', articles=articles)


@app.route('/composition/<string:name>')
def composition(name):
    name_music = name
    article = Article.query.order_by(Article.cmark.desc()).all()
    query = "select * from db where article.name_music='{name_music}'".format(name_music=name)
    print(query)
    return render_template('composition.html', comp=query)


@app.route('/create-col', methods=['POST', 'GET'])
def create_col():
    if request.method == 'POST':
        fname = request.form["fname"]
        sname = request.form["sname"]
        age = request.form["age"]
        mark = request.form["mark"]
        name_music = request.form["name_music"]
        link = request.form["link"]
        link_image = "https://i.ytimg.com/vi/" + link[32:] + "/mqdefault.jpg"
        article = Article.query.order_by(Article.cmark.desc()).all()
        column = Columnes(sname=sname, fname=fname, link=link, link_image=link_image, age=age, mark=mark,
                          name_music=name_music)
        cursor.execute(
            "UPDATE site set article.array.append('{column}') Where article.name_music='{name_music}'".format(
                name_music=name_music, column=column))
        db.session.commit()
        return redirect('/home')
    else:
        return render_template('column.html')


@app.route('/login_page')
def login_page():
    return render_template('base.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')


@app.route('/login', methods=['POST', 'GET'])
def check_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        query1 = "SELECT email , password from User WHERE email='{email}' AND password='{password}'".format(
            email=email, password=password)
        rows = cursor.execute(query1)
        rows = rows.fetchall()
        if len(rows) == 1:
            user = User.query.filter_by(email=email).first
            if user and check_password_hash(user.password, password):
                load_user(user)

                next1 = request.args.get('next')
                redirect(next1)
            else:
                flash('Login or password is not correct')
        else:
            return redirect('/login')
    else:
        flash('Please fill login and password fields!')
    return render_template('login.html')


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        cmark = request.form["c_mark"]
        mark = request.form["mark"]
        cfname = request.form["c_fname"]
        csname = request.form["c_sname"]
        fname = request.form["fname"]
        sname = request.form["sname"]
        name_music = request.form["name_music"]
        link = request.form["link"]
        link_image = "https://i.ytimg.com/vi/" + link[32:] + "/mqdefault.jpg"
        age = request.form["age"]
        notes = request.form["notes"]
        article = Article(cfname=cfname, csname=csname, cmark=cmark, notes=notes, name_music=name_music)
        column = Columnes(sname=sname, fname=fname, link=link, link_image=link_image, age=age, mark=mark,
                          name_music=name_music)
        query = '''INSERT into  ''' + "Article" + '''(name_music,cfname,csname,note,cmark) VALUES (%s,%s,%s,%s,%s)'''
        data = (name_music, cfname, csname, notes, cmark)
        cursor.execute(query, data)
        query1 = "INSERT into Columnes values ('{fname}','{sname}','{mark}','{age}','{link}','{link_image}','{name_music}')".format(
            fname=fname, sname=sname, mark=mark, age=age, link=link, link_image=link_image, name_music=name_music)
        cursor.execute(query1)
        #db.session.add(article)
        #db.session.add(column)
        db.session.commit()
        return redirect('/home')
    else:
        return render_template('create-article.html')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('check_login') + '?next=' + request.url)
    return response


if __name__ == '__main__':
    app.run(debug=True)
