from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange


class AddPetForm(FlaskForm):
    """ Add Pet """

    name = StringField('Pet Name', validators=[InputRequired()])
    species = SelectField('Species', choices=[
                                        ('cat', 'Cat'),
                                        ('dog', 'Dog'),
                                        ('porcupine', 'Porcupine')])
    photo_url = StringField('Photo URL', validators=[
                                        Optional(),
                                        URL()])
    age = IntegerField('Age', validators=[
                                    Optional(),
                                    NumberRange(min=0,max=30)])
    notes = TextAreaField('Notes')


class EditPetForm(FlaskForm):
    """ Edit Pet. """

    photo_url = StringField('Photo URL', validators=[
                                        Optional(),
                                        URL()])
    notes = StringField('Notes')
    available = BooleanField('Available?')
