import sqlite3

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True)
    fname = db.Column(db.String(50), primary_key=True, nullable=False)
    sname = db.Column(db.String(50), primary_key=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Article(db.Model):
    id = db.Column(db.Integer, autoincrement=True)
    name_music = db.Column(db.String(100), primary_key=True, nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    sname = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    link_image = db.Column(db.String(100), nullable=False)
    mark = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


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
        if len(password)>6 and password == rep_password:
            user = User(fname=fname, sname=sname, age=age, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/home')
        else:
            return render_template('sign-up.html')
    else:
        return render_template('sign-up.html')


@app.route('/home')
def home():  # put application's code here
    articles = Article.query.order_by(Article.mark.desc()).all()
    return render_template('index.html', articles=articles)

@app.route('/login',methods=['POST','GET'])
def check_login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        sqlconnection=sqlite3.Connection("site.db")
        cursor=sqlconnection.cursor()
        query1="SELECT email , password from User WHERE email='{email}' AND password='{password}'".format(email=email,password=password)
        rows=cursor.execute(query1)
        rows=rows.fetchall()
        if len(rows)==1:
            return redirect('/home')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        mark = request.form["mark"]
        number = request.form["number"]
        fname = request.form["fname"]
        sname = request.form["sname"]
        name_music = request.form["name_music"]
        link = request.form["link"]
        link_image = "https://i.ytimg.com/vi/" + link[17:] + "/mqdefault.jpg"
        age = request.form["age"]
        article = Article(mark=mark, number=number, fname=fname, name_music=name_music, sname=sname, link=link,
                          link_image=link_image, age=age)
        db.session.add(article)
        db.session.commit()
        print(link_image)
        return redirect('/home')
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    app.run(debug=True)
