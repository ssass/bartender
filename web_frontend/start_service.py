from flask import *
from wtforms import StringField, BooleanField, Form
from flask_wtf import Form, RecaptchaField
from wtforms import TextField
import logging
import sys

# Defaults to stdout
logging.basicConfig(level=logging.INFO)

# get the logger for the current Python module
log = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class SignupForm(Form):
    username = TextField('Username')
    recaptcha = RecaptchaField()

@app.route('/')
def main():
    return "Welcome to the python service!"

@app.route('/primerselect/')
def start(name=None):
    return render_template('base.html', name=name)

@app.route('/primerselect/run', methods=['GET', 'POST'])
def start_process(name=None):
    return render_template('base.html', name=name)


@app.route('/hello/')
def hello():
    form = SignupForm()
    return render_template('hello.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")