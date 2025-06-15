# 📝 ToDoList App Pro

Aplicación web desarrollada en Flask que permite a los usuarios gestionar sus tareas personales con autenticación, validaciones y despliegue profesional.

## 🚀 Funcionalidades

- Registro e inicio de sesión seguro
- Crear, editar y eliminar tareas
- Ver tareas personales (protegidas por sesión)
- Interfaz limpia con Bootstrap 5
- Deploy en Render (100% online)
- Contenedor Docker listo para producción

## 🔧 Tecnologías usadas

- Python 3.11
- Flask
- Flask-Login / Flask-WTF / Flask-SQLAlchemy
- Bootstrap 5
- SQLite (local) / Render (cloud)
- Gunicorn + Docker
- Git + GitHub

## ▶️ Ejecutar localmente

```bash
git clone https://github.com/tu_usuario/todolist_app_pro.git
cd todolist_app_pro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
