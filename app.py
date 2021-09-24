from flask import Flask,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    name_music=db.Column(db.String(100),primary_key=True,nullable=False)
    name=db.Column(db.String(50),primary_key=True,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    mark=db.Column(db.Float,nullable=False)
    number=db.Column(db.Integer,primary_key=True,nullable=False)
    def __repr__(self):
        return '<Article %r>'%self.id
@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('index.html')
@app.route('/create-article')
def create_article():
    return render_template('create-article.html')
if __name__ == '__main__':
    app.run(debug=True)
