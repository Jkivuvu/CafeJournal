from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FloatField
from wtforms.validators import DataRequired, URL


class add_coffee_form(FlaskForm):
    name = StringField("Name of cafe", validators=[DataRequired()])
    map_url = StringField("Map url", validators=[DataRequired(), URL()])
    img_url = StringField("Image url", validators=[DataRequired(), URL()])
    location = StringField('City', validators=[DataRequired()])
    has_sockets = SelectField('Has sockets?', choices=[(0, 'No'), (1, 'Yes')])
    has_toilet = SelectField('Has toilet?', choices=[(0, 'No'), (1, 'Yes')])
    has_wifi = SelectField('Has wifi?', choices=[(0, 'No'), (1, 'Yes')])
    can_take_calls = SelectField('Can take calls?', choices=[(0, 'No'), (1, 'Yes')])
    seats = SelectField("How many seats?", choices=['0-10', '10-20', '20-30', '30-40', '40-50', '50+'])
    coffee_price = FloatField("Price of coffee", validators=[DataRequired()])
    submit = SubmitField("Submit")
