from flask import Flask, render_template, request, json, session, render_template
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import imaplib
import urllib.request
import smtplib
import getpass
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64 
from flaskext.mysql import MySQL
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

app = Flask(__name__)

app.secret_key ='matangalachanga'

app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)
mysql.init_app(app)

def entidades(_user, _stage, _stageinfo):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('Insert into ENTITY (user, stage, stage_info) VALUES (%s,%s,%s)', (_user,_stage,_stageinfo))
    conn.commit()

def registro(_n, _l, _e, _p):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        ins=cursor.execute("INSERT INTO USERS (name, last_name, email, password) VALUES (%s, %s, %s, %s)", (_n, _l, _e, _p))
        conn.commit()
        if ins:
            return True
        else:
            return False
        
        cursor.close()
    except Exception as e:
        return e

def inAspirantes(_nombre, _domicilio, _correo, _puesto, _area, _sueldo, _horas, _fecha, _tipo, correopos):
    try:
        estatus = 1
        conn = mysql.connect()
        cursor = conn.cursor()
        ins=cursor.execute('INSERT INTO ASPIRANTS (nombre, domicilio, correo, puesto, area, sueldo, horas, fecha, tipo, reclutador, estatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)', (_nombre, _domicilio, _correo, _puesto, _area, _sueldo, _horas, _fecha, _tipo, correopos,estatus))
        conn.commit()
        if ins:
            return True
        else:
            return False
        
        cursor.close()
    except Exception as e:
        return e

def Ultimomail():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT reclutador FROM ASPIRANTS ORDER BY id DESC LIMIT 1')
    ultima = cursor.fetchall()
    return ultima

def select():
    cur1 = mysql.get_db().cursor()
    cur1.execute('SELECT * FROM ASPIRANTS')
    aspirantes = cur1.fetchall()
    #print (aspirantes)
    return aspirantes

def buscarU(_id):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM ASPIRANTS WHERE id = %s',_id)
    aspirante = cur.fetchall()
    return aspirante
    
"""def contrato(_nombre, _domicilio, _puesto, _area, _sueldo, _horas, _fecha, _tipo):
    cur2 = mysql.get_db().cursor()
    cur2.execute('SELECT * FROM ASPIRANTS WHERE nombre = %s AND domicilio = %s AND puesto =%s AND area= %s AND sueldo = %s AND horas = %s AND fecha = %s AND tipo = %s;',  (_nombre, _domicilio, _puesto, _area, _sueldo, _horas, _fecha, _tipo))
    aspirante = cur2.fetchall()
    return aspirante"""

def Firma():
    nombre= 'juancho'
    destinatario= 'jennieec98@gmail.com'

    usuraio='j.consultora.a@gmail.com'
    archivo= "Contrato.pdf"
    #message ='Bienvenido al Sistema de puntos Ekkos!'
    Asunto = 'Firma de Contrato'
    mensaje = MIMEMultipart("plain")#estandar
    mensaje["Subject"]=Asunto
    mensaje["From"]=usuraio
    mensaje["To"]=destinatario
    
    html=f"""
    <html>
    <body>
        Hola <i>{destinatario}</i> te hago llegar el contrato de <i>{nombre}</i></br>
        Firma por favor
        http://127.0.0.1:5000/login

    </body>
    </html>
    """
    parte_html=MIMEText(html,"html")
    
    mensaje.attach(parte_html)
    
    
    adjunto=MIMEBase("application","octect-stream")
    adjunto.set_payload(open(archivo,"rb").read())
    #print("Lo encontré")
    encode_base64(adjunto)

    adjunto.add_header("content-Disposition",f"attachment; filename={archivo}")
    mensaje.attach(adjunto)
    mensaje_final= mensaje.as_string()
    server =smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login(usuraio,'Consulta2.ja')

    #print("Inicio seción")
    #server.sendmail('ekkoscorp@gmail.com','robertoxd27@gmail.com', message)
    server.sendmail(usuraio,destinatario,mensaje_final)
    server.quit()
    #print("Correo enviado exitosamente!")


def CrearPDF(_n, _d, _p, _a, _s, _h, _f, _t):
    os.remove("/Users/jennieec/Desktop/gofaster/gofaster/Contrato.pdf")
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        asp = cursor.execute('SELECT * FROM ASPIRANTS WHERE nombre = %s AND domicilio = %s AND puesto =%s AND area= %s AND sueldo = %s AND horas = %s AND fecha = %s AND tipo = %s;',  (_n, _d, _p, _a, _s, _h, _f, _t))
        #conn.commit()
        #asp = cursor.fetchall()
        print("paso1")
            
        #if _n and _d and _p and _a and _s and _h and _f and _t:
            #conn = mysql.connect()
            #cursor = conn.cursor()
            #print("paso 1")
            
            #os.remove("Archivos/Contrato.pdf")
        _no = _n
        _TituloDocumento="Contrato de ingreso"
        _di = _d
        _pu = _p
        _ar = _a
        _su = _s
        _ho = _h
        _ti = _t
        #print("paso 2")
        c=canvas.Canvas("Contrato.pdf")
        c.setTitle(_TituloDocumento)
        c.setLineWidth(.3)
        c.setFont('Helvetica',36)
        #print("paso 3")
        textLines = [
            'Este es el contrato de: ', (_n) ,'Quien poseé el RFC: ', _d ,
            'Su fecha de nacimiento es: ', _a ,'Su estado civil es; ', _s ,
            'Su dirección es: ', _p ,'Correo electrónico:',_h ,
            'Su dirección es:', _t ,'extotextotextotextotextotexto'
            ]
        #print("paso 4")
        c.drawCentredString(300,760,_TituloDocumento)
        c.setFont('Helvetica',20)
        #print("paso 5")
        text = c.beginText(100,680)    
        text.setFont("Helvetica", 18)
        for line in textLines:
            text.textLine(line)
            #print("paso 6")
            c.drawText(text)
            c.drawCentredString(300,80,_no)
            c.line(200,100,400,100)
            #print("paso 7")
            
            c.save()
            #print("cierre")
            asp = cursor.fetchall()
    finally:
        cursor.close()   