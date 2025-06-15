from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[InputRequired(), Length(min=4, max=25)])
    email = StringField("Correo electrónico", validators=[InputRequired(), Email()])
    password = PasswordField("Contraseña", validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[InputRequired(), Email()])
    password = PasswordField("Contraseña", validators=[InputRequired()])
    submit = SubmitField("Iniciar sesión")

class TaskForm(FlaskForm):
    title = StringField("Título", validators=[InputRequired(), Length(max=150)])
    description = TextAreaField("Descripción")
    completed = BooleanField("¿Completada?")
    submit = SubmitField("Guardar")
