from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, TextAreaField


class KontaktaOssForm(FlaskForm):
    name = StringField(
        label="Ditt namn", 
        validators=[
            validators.Length(min=2,max=8, message='Gör om och gör rätt!'),
            validators.DataRequired(message='Du måste fylla i')
            ])
    
    email = StringField("Epost")
    text = TextAreaField("Meddelande")