from flask import Flask, render_template, request, json, session, render_template
from flaskext.mysql import MySQL
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = Flask(__name__)

app.secret_key ='matangalachanga'

app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)
mysql.init_app(app)

def PDF(_n, _d, _p, _a, _s, _h, _f, _t):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        asp = cursor.execute('SELECT * FROM ASPIRANTS WHERE nombre = %s AND domicilio = %s AND puesto =%s AND area= %s AND sueldo = %s AND horas = %s AND fecha = %s AND tipo = %s;',  (_n, _d, _p, _a, _s, _h, _f, _t))
        
        doc = SimpleDocTemplate("/Users/jennieec/Desktop/gofaster/gofaster/Contrato.pdf", pagesize=letter,
                                rightMargin=60, leftMargin=60,
                                topMargin=40, bottomMargin=40)
        Story = []
        logotipo = "/Users/jennieec/Desktop/gofaster/gofaster/static/2.png"

        #datos del aspirante
        nombre = _n
        direccion = _d
        puesto = _p
        area = _a
        sueldo = _s
        horas = _h
        tipo = _t


        #datos de la foto 
        imagen = Image(logotipo, 2 * inch, 2 * inch)
        Story.append(imagen)

        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))


        # Se construye la dirección

        Story.append(Spacer(1, 12))
        texto = 'Estimado %s:' % nombre.split()[0].strip()
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))

        texto = 'Nos gustaría darle la bienvenida al aspirante %s  \
                Con la dirección %s que entrara en el puesto de %s en el area de %s \
                Con un sueldo de %s al mes en un horario de %s a la semana \
                definiendo que su contrato es de  %s.' % (nombre, direccion, puesto, area, sueldo, horas, tipo)
        Story.append(Paragraph(texto, estilos["Justify"]))
        Story.append(Spacer(1, 12))


        texto = 'Firma del director,'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 48))
        texto = 'Jennifer Enríquez'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))
        doc.build(Story)
        asp = cursor.fetchall()
    finally:
        cursor.close()   