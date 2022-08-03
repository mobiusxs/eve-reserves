from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class LogbookForm(FlaskForm):
    first = StringField('First', validators=[DataRequired()], render_kw={"placeholder": "First"})
    last = StringField('Last', validators=[DataRequired()], render_kw={"placeholder": "Last"})
