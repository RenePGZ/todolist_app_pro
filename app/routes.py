from app import app
from app import db
from app.forms import RegisterForm, TaskForm, LoginForm
from app.models import User, Task
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash("Este correo ya está registrado. Intenta con otro.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Usuario registrado correctamente. Inicia sesión.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("tasks"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("tasks"))
    return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))

@app.route("/tasks")
@login_required
def tasks():
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template("tasks.html", tasks=user_tasks)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            completed=form.completed.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Tarea creada correctamente.", "success")
        return redirect(url_for("tasks"))
    return render_template("task_form.html", form=form, action="Agregar")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash("No tienes permiso para editar esta tarea.", "danger")
        return redirect(url_for("tasks"))

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.completed = form.completed.data
        db.session.commit()
        flash("Tarea actualizada.", "success")
        return redirect(url_for("tasks"))
    return render_template("task_form.html", form=form, action="Editar")

@app.route("/delete/<int:id>")
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash("No tienes permiso para eliminar esta tarea.", "danger")
        return redirect(url_for("tasks"))

    db.session.delete(task)
    db.session.commit()
    flash("Tarea eliminada.", "info")
    return redirect(url_for("tasks"))
