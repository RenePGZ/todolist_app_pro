from app import app
from app import db
from app.forms import RegisterForm, TaskForm, LoginForm, EditProfileForm, ChangePasswordForm
from app.models import User, Task
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import calendarific
from calendar_api import obtener_festivos

def admin_required(f):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            abort(403)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/admin")
@admin_required
def admin():
    users = User.query.all()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("admin/dashboard.html", users=users, tasks=tasks)

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    # ⚠️ Asegúrate de que el usuario sea admin (si tienes roles)
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)

    users = User.query.all()
    tasks = Task.query.all()
    return render_template("admin/dashboard.html", users=users, tasks=tasks)

@app.route("/admin/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_usuario_admin(id):
    if not current_user.is_admin:
        abort(403)
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado", "info")
    return redirect(url_for("admin_dashboard"))

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
    filtro = request.args.get("filtro", "todas")
    
    query = Task.query.filter_by(user_id=current_user.id)

    if filtro == "completadas":
        query = query.filter_by(completed=True)
    elif filtro == "pendientes":
        query = query.filter_by(completed=False)
    
    user_tasks = query.order_by(Task.created_at.desc()).all()
    return render_template("tasks.html", tasks=user_tasks, filtro=filtro)

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

@app.route("/dashboard")
@login_required
def dashboard():
    from datetime import datetime
    today = datetime.today().strftime("%A, %d de %B de %Y")
    holidays = obtener_festivos()
    return render_template("dashboard.html", today=today, holidays=holidays)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500

@app.route("/perfil")
@login_required
def perfil():
    return render_template("profile.html")

@app.route("/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Validar duplicados (otro usuario con el mismo correo o username)
        if User.query.filter(User.username == form.username.data, User.id != current_user.id).first():
            flash("Este nombre de usuario ya está en uso.", "danger")
            return redirect(url_for("editar_perfil"))

        if User.query.filter(User.email == form.email.data, User.id != current_user.id).first():
            flash("Este correo ya está registrado.", "danger")
            return redirect(url_for("editar_perfil"))

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Perfil actualizado.", "success")
        return redirect(url_for("perfil"))
    return render_template("edit_profile.html", form=form)

@app.route("/eliminar_cuenta", methods=["POST"])
@login_required
def eliminar_cuenta():
    user_id = current_user.id
    logout_user()
    Task.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash("Cuenta eliminada exitosamente.", "info")
    return redirect(url_for("login"))

@app.route("/cambiar_contraseña", methods=["GET", "POST"])
@login_required
def cambiar_contraseña():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash("La contraseña actual no es correcta.", "danger")
            return redirect(url_for("cambiar_contraseña"))

        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash("Contraseña actualizada correctamente.", "success")
        return redirect(url_for("perfil"))
    return render_template("change_password.html", form=form)
