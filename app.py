from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu"

userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1"
dbname = "/company"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telp = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, telp, address):
        self.name = name
        self.email = email
        self.telp = telp
        self.address = address

@app.route('/')
def index():
    data_employe = db.session.query(Employes)
    return render_template('index.html', data=data_employe)

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telp = request.form['telp']
        address = request.form['address']

        add_data = Employes(name, email, telp, address)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('index'))

    return render_template('input.html')

@app.route('/edit/<int:id>')
def edit_data(id):
    data_employes = Employes.query.get(id)
    return render_template('edit.html', data=data_employes)

@app.route('/proses_edit', methods=['POST', 'GET'])
def proses_edit():
    data_employes = Employes.query.get(request.form.get('id'))

    data_employes.name = request.form['name']
    data_employes.email = request.form['email']
    data_employes.telp = request.form['telp']
    data_employes.address = request.form['address']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    data_employe = Employes.query.get(id)
    db.session.delete(data_employe)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('index'))