import imaplib
import email


user = 'j.consultora.a@gmail.com'
password = 'Consulta2.ja'
imap_url = 'imap.gmail.com'
con = imaplib.IMAP4_SSL(imap_url) 
con.login(user, password)
con.select('Inbox')

def get_body(msg): 
	if msg.is_multipart(): 
		return get_body(msg.get_payload(0)) 
	else: 
		return msg.get_payload(None, True)  

# Function to search for a key value pair 
def search(key, value, con): 
	result, data = con.search(None, key, '"{}"'.format(value)) 
	return data 

# Function to get the list of emails under this label 
def get_emails(result_bytes): 
	msgs = [] # all the email data are pushed inside an array 
	for num in result_bytes[0].split(): 
		typ, data = con.fetch(num, '(RFC822)') 
		msgs.append(data) 

	return msgs 

msgs = get_emails(search('FROM', 'jennieec98@gmail.com', con)) 

for msg in msgs:
    for sent in msg:
        if type(sent) is tuple:
            content = str(sent[1], 'utf-8')
            data = str(content)
            try:
                #Nombre del aspirtante
                a = data.find("Nombre:")
                a2 = data.find("Domicilio:")
                _a3 = data[a+7:a2]
                print (_a3)

                #Domicilio del aspirtante
                b = data.find("Domicilio:")
                b2 = data.find("Correo:")
                _b3 = data[b+10:b2]
                print (_b3)

                #Correo del aspirante
                c = data.find("Correo:")
                c2 = data.find("Puesto:")
                _c3 = data[c+7:c2]
                print (_c3)

                #Puesto del aspirante
                d = data.find("Puesto:")
                d2 = data.find("Area:")
                _d3 = data[d+7:d2]
                print (_d3)

                #Area del aspirante
                e = data.find("Area:")
                e2 = data.find("Sueldo:")
                _e3 = data[e+5:e2]
                print (_e3)

                #Sueldo del aspirante
                f = data.find("Sueldo:")
                f2 = data.find("Horas de trabajo:")
                _f3 = data[f+7:f2]
                print (_f3)

                #Horas de trabajo del aspirante
                g = data.find("Horas de trabajo:")
                g2 = data.find("Fecha de ingreso:")
                _g3 = data[g+17:g2]
                print (_g3)

                #Fecha de ingreso del aspirante
                h = data.find("Fecha de ingreso:")
                h2 = data.find("Tipo de contrato:")
                _h3 = data[h+17:h2]
                print (_h3)

                #Tipo de contrato del aspirante
                i = data.find("Tipo de contrato:")
                i2 = data.find("*Espero respuesta")
                _i3 = data[i+17:i2]
                print (_i3)
                

            except UnicodeEncodeError as e: 
                pass


con.close()
con.logout()