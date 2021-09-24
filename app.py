from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS']=False
db=SQLAlchemy(app)
class Article(db.Model):
    id=db.Column(db.Integer,autoincrement=True)
    name_music=db.Column(db.String(100),primary_key=True,nullable=False)
    fname=db.Column(db.String(50),primary_key=True,nullable=False)
    sname=db.Column(db.String(50),primary_key=True,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow())
    mark=db.Column(db.Float,nullable=False)
    number=db.Column(db.Integer,primary_key=True,nullable=False)
    def __repr__(self):
        return '<Article %r>' % self.id
@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('index.html')
@app.route('/create-article',methods=['POST','GET'])
def create_article():
    if request.method=="POST":
        mark=request.form["mark"]
        number = request.form["number"]
        fname = request.form["fname"]
        sname = request.form["sname"]
        name_music= request.form["name_music"]
        article=Article(mark=mark,number=number,fname=fname,name_music=name_music,sname=sname)
        db.session.add(article)
        print("норм")
        db.session.commit()
        print("норм")
        return redirect('/home')
    else:
        return render_template('create-article.html')
if __name__ == '__main__':
    app.run(debug=True)
