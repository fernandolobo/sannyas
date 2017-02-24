from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    name_male = StringField('Male Name')
    script_male = StringField('Male Script')
    name_female = StringField('Female Name')
    script_female = StringField('Female Script')
    meaning = StringField('Meaning', validators=[DataRequired()])
    first_name = BooleanField('1st Name', default=False)
    second_name = BooleanField('2nd Name', default=False)
    language = StringField('Language')
    source = StringField('Source')
    confirmation = StringField('Confirmation')
    popularity = StringField('Popularity')
    note = StringField('Notes')
    submit = SubmitField('Submit')
