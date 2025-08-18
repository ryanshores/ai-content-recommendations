from wtforms import Form, StringField, validators

class IndexForm(Form):
    input = StringField('Input', [validators.InputRequired()], render_kw={"placeholder": "Enter your name"})
    output = StringField('Output', [validators.Optional()])
