import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from getpass import getpass
import re
import Modelo as Modelo
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

html = f"""
<html>
<body>
    <p>Buen dia, <br> 
    <p></p>
    Su solicitud para la generación del contrato del aspirante se ha mandado, en breve se le mandará el correo.<br>

    Llene el siguiente http://127.0.0.1:5000/
    <p></p>
    Excelente día!<br>
</body>
</html>
"""
parte_html = MIMEText(html,"html")

username = "s.cgrincon@gmail.com"
password = "Risas1998pip"

imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(username, password)

status, mensaje = imap.select("INBOX")

#print(mensaje)

N = 1
mensaje = int(mensaje[0])

def _textomail(from_):

    exp1 = r"<([a-zA-Z0-9]+.+)>"
    correoexp = re.findall(exp1, from_, re.MULTILINE)
    #correopos = (correoexp[0])
    correopos = (correoexp[0])
    print (correopos)
    return correopos


def _textobody(body):
    
    exp2 = (r"devolver: ([a-zA-Z0-9]+.+).\n"
	r"Porque: ([a-zA-Z0-9]+.+)")
    bodyexp = re.findall(exp2, body, re.MULTILINE)
    bodypos0 = (bodyexp[0])
    print(bodypos0)
    #print(bodypos2)
    return bodyexp


for i in range(mensaje, mensaje -N, -1):
    #print(f"vamos por el mensaje {i}")
    try:
        res, mensaje = imap.fetch(str(i), "(RFC822)")
    except:
        break
    for repuesta in mensaje:
        if isinstance(repuesta,tuple):
            mensaje=email.message_from_bytes(repuesta[1])
            subject=decode_header(mensaje["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject=subject.decode()
            from_ =mensaje.get("From")
            #print("Subject:", subject)
            #print("From: ", from_)

            if mensaje.is_multipart():
                for part in mensaje.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        correopos = _textomail(from_)
                        bodyexp = _textobody(body)
                        bodypos1 = (bodyexp[0][0]) 
                        bodypos2 = (bodyexp[0][1])                        
                        try:
                            _insert=Modelo.insertardatos(correopos,bodypos1,bodypos2)
                            print(_insert)
                            Modelo.pasos(_renitente,'ENVIO CORREO', 'EL CORREO FUE ENVIADO CORRECTAMENTE')
                            try:
                                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                server.login('s.cgrincon@gmail.com','Risas1998pip')
                                time.sleep(3)
                                _renitente = Modelo.Ultimomail()
                                time.sleep(3)
                                server.sendmail(username,_renitente,parte_html.as_string())
                                server.quit()
                                print("Correo enviado")
                                Modelo.pasos(_renitente,'RESPUESTA CORREO', 'LA RESPUESTA FUE ENVIADA CORRECTAMENTE')
                            except Exception as a:
                                pass

                        except Exception as e:
                            respuesta_re = 'El formato no es el correcto'
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.login('s.cgrincon@gmail.com','Risas1998pip')
                            time.sleep(3)
                            _renitente = Modelo.Ultimomail()
                            time.sleep(3)
                            server.sendmail(username,_renitente,parte_html.as_string())
                            server.quit()
                            print("Correo enviado")
                            Modelo.pasos(_renitente,'RESPUESTA CORREO', 'LA RESPUESTA FUE ENVIADA CORRECTAMENTE')

