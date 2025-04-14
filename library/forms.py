from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from library.models import Reader

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Reader.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = Reader.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
        
    username = StringField(label='USER NAME', validators=[Length(min=2, max=30), DataRequired()])
    role = RadioField(label='ROLE', choices=[('Student','Student'),('Admin','Admin')], validators=[DataRequired()])
    roll_number = StringField(label='ROLL NUMBER', validators=[Length(min=8, max=8), DataRequired()])
    email_address = StringField(label='INSTITUTE EMAIL-ID', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='PASSWORD', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='CONFIRM PASSWORD', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='CREATE ACCOUNT')

class LoginForm(FlaskForm):
    username = StringField(label='USER NAME', validators=[DataRequired()])
    password = PasswordField(label='PASSWORD', validators=[DataRequired()])
    submit = SubmitField(label='LOGIN')

class PostForm(FlaskForm):
    post_title = StringField(label='POST TITLE', validators=[DataRequired()])
    post_body = TextAreaField(label="POST BODY")
    submit = SubmitField(label = 'CREATE POST')

class BookForm(FlaskForm):
    title = StringField(label='TITLE OF THE BOOK', validators=[Length(min=2, max=75), DataRequired()])
    author = StringField(label='AUTHOR', validators=[Length(min=2, max=50), DataRequired()])
    publisher = StringField(label='PUBLISHER', validators=[Length(min=2, max=50), DataRequired()])
    isbn =  StringField(label='ISBN NUMBER', validators=[Length(min=6, max=15), DataRequired()])
    quantity = IntegerField(label='QUANTITY', validators = [DataRequired()])
    publication_year = IntegerField(label='QUANTITY', validators = [DataRequired()])
    image_url = StringField(label='IMAGE URL', validators=[Length(min=10, max=400), DataRequired()])
    submit = SubmitField(label = 'ADD BOOK')