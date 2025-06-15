from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[
        DataRequired(),
        Length(min=3, max=20, message="Debe tener entre 3 y 20 caracteres")
    ])
    email = StringField("Correo electrónico", validators=[
        DataRequired(),
        Email(message="Correo inválido")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(),
        Length(min=6, message="Mínimo 6 caracteres")
    ])
    confirm_password = PasswordField("Confirmar contraseña", validators=[
        DataRequired(),
        EqualTo("password", message="Las contraseñas deben coincidir")
    ])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[
        DataRequired(),
        Email(message="Correo inválido")
    ])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")

class TaskForm(FlaskForm):
    title = StringField("Título", validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    description = TextAreaField("Descripción", validators=[
        Length(max=300)
    ])
    completed = BooleanField("Completada")
    submit = SubmitField("Guardar")

class EditProfileForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[
        DataRequired(), Length(min=3, max=20)
    ])
    email = StringField("Correo electrónico", validators=[
        DataRequired(), Email()
    ])
    submit = SubmitField("Guardar cambios")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Contraseña actual", validators=[DataRequired()])
    new_password = PasswordField("Nueva contraseña", validators=[
        DataRequired(),
        Length(min=6, message="Mínimo 6 caracteres")
    ])
    confirm_new_password = PasswordField("Confirmar nueva contraseña", validators=[
        DataRequired(),
        EqualTo("new_password", message="Las contraseñas no coinciden")
    ])
    submit = SubmitField("Cambiar contraseña")
