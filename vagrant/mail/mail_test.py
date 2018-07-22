from flask import Flask
from flask_mail import Mail, Message
from pass_file import mail_pass, mail_address, mail_recipient
# import os

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": mail_address,
    "MAIL_PASSWORD": mail_pass}

app.config.update(mail_settings)
mail = Mail(app)

mail_body = "Katarzyna,\nTo testowy mail wysłany bezpośrednio z Pythonowej aplikacji przy użyciu biblioteki Flask-Mail. " \
            "Jeśli dostałaś tego mail'a, proszę o potwierdzenie dostarczenia.\n" \
            "Pozdrawiam,\nPythArek"

if __name__ == '__main__':
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[mail_recipient], # replace with your email for testing
                      body=mail_body)
        mail.send(msg)
