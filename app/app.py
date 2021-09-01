import os
import flask
from flask import request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from wtforms import Form, StringField, validators, TextAreaField

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

class FAQForm(Form):
    email = StringField('Your Email Address', [validators.InputRequired(), validators.Length(min=6, max=35)], render_kw={'class':'form-control'})
    name = StringField('Your Name', [validators.InputRequired(), validators.Length(min=4, max=25)], render_kw={'class':'form-control'})
    content = TextAreaField('Your Question', [validators.Length(max=500)], render_kw={'class':'form-control', 'rows': 5})

def send_mail_handler(email, name, questionContent):
    msg = Message(f'A Question from {name}')
    msg.body = (questionContent)
    msg.recipients = ['sci.mailtest@gmail.com']
    fromMail = os.environ.get('MAIL_DEFAULT_SENDER')
    msg.sender = f'E-staffing FAQ <{fromMail}>'
    msg.reply_to = email

    mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FAQForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            send_mail_handler(form.email.data, form.name.data, form.content.data)
        except:
            flash('Email sent failed!', 'error')
            return render_template('index.html', form=form)

        flash('An email was sent to sci.mailtest@gmail.com.')
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

app.run()