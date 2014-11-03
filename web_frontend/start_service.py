import os
import StringIO
from flask import *
from wtforms import BooleanField, StringField, validators, TextAreaField
from flask_wtf import Form
from primer_select.run_process import PrimerSelect

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
config_handle = open("../config.cfg", 'rU')
with open ("../config.cfg", "r") as f:
    predefined_config = f.read()

class MyForm(Form):
    name = StringField('name', validators=[validators.Length(min=4, max=25)])

class InputForm(Form):
    input = TextAreaField('Input Sequences', validators=[validators.DataRequired()])
    predefined = TextAreaField('Predefined primers')
    configuration = TextAreaField('Configuration', default=predefined_config, validators=[validators.DataRequired()])

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = InputForm()
    if form.validate_on_submit():
        input = StringIO.StringIO(form.input)
        config = StringIO.StringIO(form.configuration)
        primer_sets = PrimerSelect.predict_primerset(input, None, config)
        opt_result = PrimerSelect.optimize(config, primer_sets)
        PrimerSelect.output(opt_result, primer_sets)
    return render_template('base.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")