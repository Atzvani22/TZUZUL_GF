import os
from flask import Flask, render_template, redirect, request, url_for, session
from flaskext.mysql import MySQL
import urllib.request
import Modelo as Modelo


app = Flask(__name__)

app.secret_key ='007Rincon'

app.config['MYSQL_DATABASE_USER'] = 'sepherot_diego'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ywx1pqRn5y'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_diegoBD'
app.config['MYSQL_DATABASE_HOST'] = 'sepheroth.com'
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def Index():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        correo = request.form['correo']
        password = request.form['password']
        #print(correo)
        #print(password)
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM S_C_USER WHERE EMAIL=%s', (correo))
        user = cur.fetchone()
        #print(user)
        cur.close()
        if len(user)>0:
            if password == user[3]:                
                session['name']=user[1]
                #print(session['name'])
                session['correo'] =user[4]
                #print(session['correo'])
                Modelo.pasos(session['correo'],'LOGIN', 'LOGIN EXITOSO DEL USUARIO')
                return render_template('mis_pedidos.html')
        else:
            Modelo.pasos(correo,'LOGIN.FAIL', 'ERROR EN EL LOGIN DEL USUARIO')
            return 'Error en el correo o en la contraseña'
    else:
        return render_template('login.html')

@app.route('/mis_pedidos', methods=['GET', 'POST'])
def mis_pedidos():
    _username=Modelo.nomuser(session['name'])
    Modelo.pasos(session['name'],'P.PEDIDOS', 'USUARIO VE SUS PEDIDOS')
    return render_template('mis_pedidos.html', nomre = _username[0][0])

@app.route('/devoluciones_reembolsos')
def devoluciones_reembolsos():
    Modelo.pasos(session['name'],'P.DEVOLUCION', 'USUARIO VE SUS TICKETS')
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM S_C_REFUND1 WHERE STATUS_R in (1, 2) AND EMAIL_R = %s ',session['correo'])
    tickets = cur.fetchall()
    _ticketactivos=Modelo.Ttickets(session['correo'])
    _tickettotal=Modelo.Ttickett(session['correo'])
    _ticketfinal=Modelo.Tticketf(session['correo'])
    _username=Modelo.nomuser(session['name'])
    #print(session['correo'])
    #print(tickets)

    return render_template('devoluciones_reembolsos.html', tickets = tickets,tta= _ticketactivos[0][0],ttt= _tickettotal[0][0],ttf= _ticketfinal[0][0], nomre= _username[0][0]) 

@app.route('/ticket', methods=['GET','POST'])
def ticket():
    if request.method == 'POST':
        SERCHT = request.form['SERCHT']
        _SERCHT = Modelo.BUSTI(SERCHT)
        #print(_SERCHT)
        _username=Modelo.nomuser(session['name'])
        Modelo.pasos(session['name'],'P.PEDIDOS', 'USUARIO VE SUS PEDIDOS')
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM S_C_REFUND1 WHERE STATUS_R in (1, 2) AND EMAIL_R = %s ',session['correo'])
        tickets = cur.fetchall()
        _ticketactivos=Modelo.Ttickets(session['correo'])
        _tickettotal=Modelo.Ttickett(session['correo'])
        _ticketfinal=Modelo.Tticketf(session['correo'])
        _username=Modelo.nomuser(session['name'])
        _DATAUSER=Modelo.DATOUSER(session['correo'])
        

        return render_template('ticket.html', tickets = tickets,tta= _ticketactivos[0][0],ttt= _tickettotal[0][0],ttf= _ticketfinal[0][0], nomre= _username[0][0],SERCHTIK=_SERCHT[0][0],SERCHTIK1=_SERCHT[0][1],SERCHTIK2=_SERCHT[0][2],SERCHTIK3=_SERCHT[0][3],SERCHTIK4=_SERCHT[0][4],SERCHTIK5=_SERCHT[0][5],SERCHTIK6=_SERCHT[0][6], DU =_DATAUSER)

@app.route('/editar', methods=['GET','POST'])
def editar():
    if request.method == 'POST':
        
        editicket = request.form['editicket']
        ediestado = request.form['ediestado']
        ediproducto = request.form['ediproducto']
        edidireccion = request.form['edidireccion']
        edirazon = request.form['edirazon']
        _editarticket = Modelo.editart(editicket, ediestado, ediproducto, edidireccion, edirazon)

    return render_template('ticket.html')
    
@app.route('/borrar', methods=['GET','POST'])
def borrar():
    if request.method == 'POST':
        
        borrid = request.form['borrid']
        _borrarticket = Modelo.borrarticket(borrid)

    return render_template('ticket.html')

if __name__ == '__main__': 
    app.run(debug=True)
