from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/lista_cumparaturi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Produs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(255), nullable=False)
    cumparat = db.Column(db.Boolean, nullable=False, default=False)

@app.route('/')
def lista_produse():
    produse = Produs.query.all()
    return render_template('lista.html', produse=produse)

@app.route('/adauga', methods=['GET', 'POST'])
def adauga_produs():
    if request.method == 'POST':
        nume = request.form['nume']
        produs_nou = Produs(nume=nume)
        db.session.add(produs_nou)
        db.session.commit()
        return redirect(url_for('lista_produse'))
    return render_template('adauga.html')

@app.route('/stergere/<int:id>', methods=['GET', 'POST'])
def sterge_produs(id):
    if request.method == 'POST':
        produs = Produs.query.get(id)
        db.session.delete(produs)
        db.session.commit()
        return redirect(url_for('lista_produse'))

    return render_template('stergere.html', produs_id=id)

if __name__ == '__main__':
    app.run(debug=True)
