import requests


def sendEmailGo(data):
    try:
        send = requests.post('https://', data=data, headers={'Content-Type': 'application/json'})
        response = {
            "response":{
                send.text
            },
            "status_http": send.code
        }
    except Exception as e:
        response = {
            "response": {
                "error": str(e),
                "message": "Error al enviar email"
            },
            
            "status_http": 400
        }
        
    return response