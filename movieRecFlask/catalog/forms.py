from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


class GetRecsForm(FlaskForm):

    movie_name = StringField('Pick a movie you love:', validators=[DataRequired()])
    submit = SubmitField('Get Recommendations!')