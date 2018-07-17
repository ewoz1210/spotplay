from flask_wtf import FlaskForm
from wtforms import SubmitField

class SpotPlay(FlaskForm):
    submit = SubmitField('Run Program')
