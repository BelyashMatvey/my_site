from flask import Flask,render_template,url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/user/<string:name>/<int:id>')
def index2(name,id):
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)
