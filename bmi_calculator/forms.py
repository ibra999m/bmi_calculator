from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BMIForm(FlaskForm):
    fullname = StringField('ФИО', validators=[DataRequired(message="Введите ФИО")])
    weight = FloatField('Вес (кг)', validators=[
        DataRequired(message="Введите вес"),
        NumberRange(min=1, max=300, message="Вес должен быть от 1 до 300 кг")
    ])
    height = FloatField('Рост (см)', validators=[
        DataRequired(message="Введите рост"),
        NumberRange(min=50, max=250, message="Рост должен быть от 50 до 250 см")
    ])
    submit = SubmitField('Рассчитать ИМТ')