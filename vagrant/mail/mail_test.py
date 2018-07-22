from flask import Flask
from flask_mail import Mail, Message
# import os

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "swojak.a@gmail.com",
    "MAIL_PASSWORD": "Janomami*90"}

app.config.update(mail_settings)
mail = Mail(app)

mail_body = "Katarzyna,\nTo testowy mail wysłany bezpośrednio z Pythonowej aplikacji przy użyciu biblioteki Flask-Mail. " \
            "Jeśli dostałaś tego mail'a, proszę o potwierdzenie dostarczenia.\n" \
            "Pozdrawiam,\nPythArek"

if __name__ == '__main__':
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["grandujin@gmail.com"], # replace with your email for testing
                      body=mail_body)
        mail.send(msg)