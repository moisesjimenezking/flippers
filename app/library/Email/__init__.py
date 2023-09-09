import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import jsonify, render_template
 
def sendEmail(code, emailUser):
    try:
        # Configuración del servidor SMTP de Gmail
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        # email: brunoapp.cop@gmail.com pass: Bruno-01?
        # Tu dirección de correo electrónico y contraseña de Gmail
        email = 'jimenezsmoises27@gmail.com'
        password = 'Moises-27-'

        # Dirección de correo electrónico del destinatario
        to_email = emailUser

        # Crear el objeto de mensaje
        message = MIMEMultipart()
        message['From'] = email
        message['To'] = to_email
        message['Subject'] = 'Prueba'

        # Cuerpo del mensaje en formato HTML
        html_body = "<h1>Code: {temp_code}</h1>".format(temp_code = code)

        # Adjuntar el cuerpo del mensaje como parte HTML
        message.attach(MIMEText(html_body, 'html'))

        # Conectar al servidor SMTP de Gmail
        smtp_server = smtplib.SMTP(smtp_host, smtp_port)
        smtp_server.starttls()
        smtp_server.login(email, password)

        # Enviar el correo electrónico
        smtp_server.sendmail(email, to_email, message.as_string())
        smtp_server.quit()

        response = {"response": {"Send": "success"}, "status_http": 200}
    except Exception as e:
        # Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response': {
                'message': e.args[0] if len(e.args) > 0 else str(e)
            },
            'status_http': e.args[1] if len(e.args) > 1 else 404
        }

    return response

# import requests


# def sendEmailGo(data):
#     try:
#         send = requests.post(
#             'http://127.0.0.1:3000/sendmail', 
#             data=data, 
#             headers={'Content-Type':'application/x-www-form-urlencoded'}
#         )
        
#         response = {
#             "response":{
#                 send.text
#             },
#             "status_http": send.code
#         }
#     except Exception as e:
#         response = {
#             "response": {
#                 "error": str(e),
#                 "message": "Error al enviar email"
#             },
            
#             "status_http": 400
#         }
        
#     return response