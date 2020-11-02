from flask import Flask, render_template, request, json, url_for, redirect,send_from_directory
import os
import smtplib

import getpass
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
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_roberto'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Fe2zrCW7b3'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_robertoBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)



def EnviarCorreo(_name,_email):
    nombre=_name
    destinatario=_email
    usuraio='ekkoscorp@gmail.com'
    archivo= '.\Contrato_Ekkos.pdf'
    #message ='Bienvenido al Sistema de puntos Ekkos!'
    Asunto = 'Inscripción Ekkos Points'
    mensaje = MIMEMultipart("plain")#estandar
    mensaje["Subject"]=Asunto
    mensaje["From"]=usuraio
    mensaje["To"]=destinatario
    
    html=f"""
    <html>
    <body>
        Hola <i>{nombre}</i> <i>{destinatario}</i></br>
        Bienvenido a <b>Ekkos Points System</b>
        Ingresa al link siguiente e inicia sesión para subir tu contrato.
        En caso de que algún dato esté errorneo en la misma pantalla podrás encontrar un apartado para corregir tus datos
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
    server.login(usuraio,'EkkosC0rp')

    #print("Inicio seción")
    #server.sendmail('ekkoscorp@gmail.com','robertoxd27@gmail.com', message)
    server.sendmail(usuraio,destinatario,mensaje_final)
    server.quit()
    #print("Correo enviado exitosamente!")

def insertarEventoP(_name,_password,_rfc, _email,_direccion,_fechanacimiento,_estadocivil):
    try:
       
        if _name and _password and _rfc and _email and _direccion and _fechanacimiento and _estadocivil:
            conn = mysql.connect()
            cursor = conn.cursor()
            print("paso 1")
            _TABLA="T_UserPoints"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertUsers;"
            print("paso 2")
            cursor.execute(sqlDropProcedure)
            print("paso 3")
            sqlCreateSP="CREATE PROCEDURE InsertUsers(IN UName VARCHAR(50), IN UEmail VARCHAR(50), IN UPass VARCHAR(50), IN UAdd VARCHAR(50), IN UDate DATE, IN URFC VARCHAR(50), IN CStatus VARCHAR(50), IN UStatus INT(20)) INSERT INTO "+_TABLA+"(UName, UEmail, UPass, UAdd, UDate, URFC, CStatus, UStatus) VALUES (UName, UEmail, UPass, UAdd, UDate, URFC, CStatus, UStatus)"
            print("paso 4")
            cursor.execute(sqlCreateSP)
            print("paso 5")
            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_robertoBD`.`"+_TABLA+"` (`UName` VARCHAR(50) NOT NULL, `UEmail` VARCHAR(50) NOT NULL , `UPass` VARCHAR(50) NOT NULL ,`UAdd` VARCHAR(50) NOT NULL,`UDATE` DATE NOT NULL,`URFC` VARCHAR(50) NOT NULL,`CStatus` VARCHAR(50) NOT NULL,`UStatus` INT(20),`Tiempo` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`IdUsers`)) ENGINE = InnoDB;")                    
            #cursor.execute("INSERT INTO `T_UserPoints` (`UName`,`UEmail`,`UPass`,`UAdd`,`UDATE`,`URFC`,`CStatus`) VALUES (%s, %s, %s, %s)",(_n, _l, _e, _p))
            print("paso 6")
            cursor.callproc('InsertUsers',(_name, _email , _password, _direccion, _fechanacimiento, _rfc, _estadocivil,1))
            print("paso 7")
            data = cursor.fetchall()
            

            if len(data)==0:
                conn.commit()
                print("se registro?")
                return json.dumps({'message':'Evento registrado correctamente !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            print("error")
            return json.dumps({'html':'<span>Datos faltantes</span>'})

    except Exception as e:
        print("error 2")
        print(json.dumps({'error':str(e)}))
        return json.dumps({'error':str(e)})
    finally:
       cursor.close() 
       print("cierre")
       conn.close()

def validarUsuario( _email, _password):
    try:
        if _email and _password:
            conn=mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * FROM T_UserPoints WHERE UEmail = %s"
            try:
                cursor.execute(query,(_email))
                data= cursor.fetchall()
                print(data)
                if data and data [0][3] == _password:
                    return True 
                else: 
                    return False
            except Exception as e:
                return e 
            cursor.close()
            conn.close()
        else:
            return json.dumps ({'html': '<span> Te faltan datos </span>'})            
    except Exception as e:
        return json.dumps ({'error': str(e)})

def entities(user, stage, info):
    try:
       
        conn=mysql.connect()
        cursor=conn.cursor()
        sql="INSERT INTO Entities (user, stage, stageinfo) values (%s, %s, %s)"
        query = cursor.execute(sql,(user, stage, info))
        conn.commit()
        if query:
            return True
        else:
            return False
    except Exception as e:
        print (str(e))
        return False
    conn.close()
    cursor.close()     

def buscarU(_user):
    if _user:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM T_UserPoints WHERE UEmail = %s"
        try: 
            cursor.execute(query,(_user))
            data = cursor.fetchall()
            if data:
                return data[0][2]
            else:
                return False
        except Exception as e:
            return e
            cursor.close()
            conn.close()
    else: 
            return json.dumps ({'html': '<span> Te faltan datos </span>'})    

def actualizarM(_name,_password,_rfc, _email,_direccion,_fechanacimiento,_estadocivil):
    try:
        #   _usuario = request.args.get('Usuario')
        #   _evento = request.args.get('Evento')
        if _name and _password and _rfc and _email and _direccion and _fechanacimiento and _estadocivil:            
            print("paso 1")
            conn = mysql.connect()
            print("paso 2")
            cursor = conn.cursor()
            print("paso 3")
            _TABLA="T_UserPoints"
            print("paso 4")
            #sqlDropProcedure="DROP PROCEDURE IF EXISTS actualizarPost;"
            # #cursor.execute(sqlDropProcedure)
            sqlCreateSP="UPDATE "+ _TABLA +" SET UName ='"+ _name +"',  UPass ='"+ _password +"', UAdd ='"+ _direccion +"',  UDate ='"+ _fechanacimiento +"',  URFC ='"+ _rfc +"',  CStatus ='"+ _estadocivil +"', UStatus = '2' WHERE UEmail = '"+_email+"'"
            print("paso 5")
            cursor.execute(sqlCreateSP)
            print("paso 6")
            #cursor.execute("INSERT INTO "+_TABLA+"(Usuario, Evento) VALUES (%s, %s)", (_usuario, _evento))            #cursor.callproc('actualizarPost',(_postulante))            data = cursor.fetchall()
            data=cursor.fetchall()
            if len(data)==0:
                conn.commit()
                return redirect(url_for('logeado'))
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})
    except Exception as e:
        print(json.dumps({'error':str(e)}))
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def CrearPDF(_name,_password,_rfc, _email,_direccion,_fechanacimiento,_estadocivil):
    try:
       os.remove(".\Contrato_Ekkos.pdf")
       if _name and _password and _rfc and _email and _direccion and _fechanacimiento and _estadocivil:
           conn = mysql.connect()
           cursor = conn.cursor()
           print("paso 1")
           _Nombre= _name
           _NombreArchivo="Contrato_Ekkos.pdf" 
           _TituloDocumento="Contrato Ekkos"
           _SubtituloDocumento=_Nombre
           _RFC=_rfc
           _FechaNacimiento=_fechanacimiento
           _EstadoCivil=_estadocivil
           _Dirección=_direccion
           _Email=_email
           print("paso 2")
           c=canvas.Canvas(_NombreArchivo)
           c.setTitle(_TituloDocumento)
           c.setLineWidth(.3)
           c.setFont('Helvetica',36)
           print("paso 3")
           textLines = [
               'Este es el contrato de: ', _Nombre ,'Quien poseé el RFC: ', _RFC ,
               'Su fecha de nacimiento es: ', _FechaNacimiento ,'Su estado civil es; ', _EstadoCivil ,
               'Su dirección es: ', _Dirección,'Correo electrónico:',_Email,' ' ,
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto',
               'textotextotextotextotextotextotextotextotextotexto'
               ]
           
           print("paso 4")
           c.drawCentredString(300,760,_TituloDocumento)
           c.setFont('Helvetica',20)
           c. drawCentredString(290,720,_SubtituloDocumento)
           print("paso 5")
           text = c.beginText(100,680)
           text.setFont("Helvetica", 18)
           for line in textLines:
               text.textLine(line)
           print("paso 6")
           c.drawText(text)
           c.drawCentredString(300,80,_Nombre)
           c.line(200,100,400,100)
           print("paso 7")
           c.save()
           data = cursor.fetchall()
       else:
            print("error")
            return json.dumps({'html':'<span>Datos faltantes</span>'})
    except Exception as e:
        print("error 2")
        print(json.dumps({'error':str(e)}))
        return json.dumps({'error':str(e)})
    finally:
        
        print("cierre")
        conn.close()
        
    #_Imagen="./static/ekko.jpg"



    #c.drawInlineImage(_Imagen, 130, 400)

    #drawMyRuler(c)

