from flask import Flask, render_template, request, json, url_for, session, redirect
import requests
from flaskext.mysql import MySQL
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import os
import Modelo as Modelo
import ModeloContrato as ModeloContrato
import imaplib
import email
import time
from bs4 import BeautifulSoup
import time

app = Flask(__name__)


app.secret_key ='matangalachanga'

app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL()
mysql.init_app(app)

app.config['UPLOAD_FOLDER'] ='gofaster'
app.config['UPLOAD_EXTENSIONS'] = '.pdf'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/")
def index():
    return render_template("login.html")
    
@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == "POST":
        _n = request.form['Name']
        _l = request.form['Lastname']
        _e = request.form['Email']
        _p = request.form['Password']
        #.encode('utf-8')
        #hash_p = bcrypt.hashpw(_p, bcrypt.gensalt())
        
        #insertar usurio
        if _n and _l and _e and _p:
                Modelo.registro(_n, _l, _e, _p)
                return redirect(url_for('login'))

        #validar que no exista
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM USERS WHERE email=%s', (_e))
        val = cur.fetchone()
        print(val)
        cur.close()

        #si el usuario existe
        if len(val) is not 0:
            if _e == val[3]:
                Modelo.entidades(_e,'REGISTER.FAIL', 'registro fallido')
                return 'Error: Usuario ya existente'
        #si el usuario no existe
        else:
            #insertar usurio
            Modelo.registro(_n, _l, _e, _p)
            session['name'] = val[1]
            print(session['name'])
            session['email'] = val[3]
            print(session['email'])
            Modelo.entidades(session['email'],'REGISTER', 'registro exitoso')
            return render_template('Login.html')      
    else:
        return render_template('Register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        _e = request.form['Email']
        _p = request.form['Password']
        #print(_e)
        #print(_p)

        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM USERS WHERE email=%s', (_e))
        user = cursor.fetchone()
        #print(user)
        cursor.close()
        #si el usuario existe
        if len(user) > 0:
            #si la contraseña es igual a la BD
            if _p == user[4]:                
                session['name'] = user[1]
                #print(session['name'])
                session['email'] = user[3]
                #print(session['email'])
                Modelo.entidades(session['email'],'LOGIN', 'login exitoso')
                return redirect(url_for('aspirantes'))
                time.sleep(.5)
        #si la contraseña es diferente
            else:
                Modelo.entidades(_e,'LOGIN.FAIL', 'login fallido')
                return redirect(url_for('error'))
                #regresar error
    else:
        return render_template('Login.html')
 
@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/recuperar")
def recuperar():
    return render_template("recuperar.html")

@app.route('/inicio', methods=['GET', 'POST'])
def aspirantes():
    try:
        #aqui se visualizan todos los aspirantes
        consulta = Modelo.select()
        return render_template("aspirants.html", eventos=consulta)
    except Exception as e:
        print(str(e))
        return json.dumps({'errooooooror':str(e)})        

@app.route('/aspirante', methods=['GET', 'POST'])
def aspirante():
    #aqui se muestra solo un aspirante
    if request.method == 'POST':
       _id = request.form['id']
       consulta = Modelo.buscarU(_id)
       return render_template("uno.html", eventos=consulta)
    else:
        return render_template('todos.html')

@app.route('/contrato', methods=['GET', 'POST'])
def contrato():
    if request.method == 'POST':
        _n = request.form['Nombre']
        _d = request.form['Domicilio']
        _p = request.form['Puesto']
        _a = request.form['Area']
        _s = request.form['Sueldo']
        _h = request.form['Horas']
        _f = request.form['Fecha']
        _t = request.form['Tipo']
         
        ModeloContrato.PDF(_n, _d, _p, _a, _s, _h, _f, _t)
        time.sleep(.5)
        return redirect(url_for('contrato2'))
        #ModeloContrato.Firma(_n)
        #return redirect(url_for('login'))
    else:
        return render_template('uno.html')

@app.route('/contrato2')
def contrato2():
    return render_template('error.html')

@app.route('/email')
def emaild():
    Modelo.Firma()
    return render_template('contratofirmado.html')

@app.route('/finalizar')
def finalizar():
    Modelo.Firma()
    return redirect(url_for('login'))
    
@app.route('/validar')
def validar():
    return render_template("validar.html")

@app.route("/verificados")
def verificados():
    return render_template("verificados.html")


if __name__ == "__main__":
    app.run(debug=True)
