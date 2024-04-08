from multiprocessing import connection
import re
from flask import Flask, render_template, session, url_for, request, redirect, jsonify, flash, send_from_directory
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_mysqldb import MySQL
from datetime import datetime
from config import config
import smtplib
from smtplib import SMTPException
from threading import Thread
from flask_mail import Mail, Message
from email.message import EmailMessage
import os
# Models:
from models.modelUser import ModelUser

# Entities:
from models.entities.User import User

UNItemsApp = Flask(__name__)
UNItemsApp.config.from_object(config['development'])

# Objects: 
mail = Mail(UNItemsApp) 
csrf = CSRFProtect(UNItemsApp)
db = MySQL(UNItemsApp)
login_manager_app = LoginManager(UNItemsApp)
folder = os.path.join(os.path.dirname(__file__), 'uploads/profile')
UNItemsApp.config['folder'] = folder


    # ==============================
    # Rutas principales
    # ==============================
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@UNItemsApp.before_request
def before_request():
    print("Antes de la petición...")

@UNItemsApp.after_request
def after_request(response):
    print("Después de la petición")
    return response

@UNItemsApp.route('/uploads/profile/<imgprofile>')
def uploads(imgprofile):
    return send_from_directory(UNItemsApp.config['folder'], imgprofile)

@UNItemsApp.route('/')
def index():        
    return render_template('landing-home.html')
    
    
    # ==============================
    # Rutas administrador y modales
    # ==============================
@UNItemsApp.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@UNItemsApp.route('/admin-operations', methods = ['GET', 'POST'])
@login_required
def admin_operations():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    return render_template('admin-operations.html', user = data)

    # Agregar usuario - Ruta del botón --------->
@UNItemsApp.route('/register-admin-btn', methods = ['GET', 'POST'])
@login_required
def register_btn():
    return render_template('register-admin.html')

    # Agregar usuario - Ruta del formulario --------->
@UNItemsApp.route('/register-admin', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        auth = request.form['auth']
        hash = generate_password_hash(password) 
        img = request.files['img']
        now = datetime.now()
        time = now.strftime("%Y%H%M%S")

        if img.filename !='':
            newNameFoto=time+img.filename
            img.save(os.path.join(UNItemsApp.config['folder'], newNameFoto))
        regUser = db.connection.cursor()
        regUser.execute("INSERT INTO user (username, email, password, auth, imgprofile) VALUES (%s, %s, %s, %s, %s)", (username, email, hash, auth, newNameFoto))
        db.connection.commit()
        
        msg = Message(subject="Bienvenido a Number Six", recipients=[email], html=render_template ("mail-template.html"))
        mail.send(msg)
        
        flash('Usuario agregado exitosamente')
        return redirect(url_for('admin_operations'))
    else:
        flash('¡Algo salió mal!')
        return redirect(url_for('add-admin'))
    
    # Eliminar usuario - Ruta del botón --------->
@UNItemsApp.route('/delete-user/<int:id>')
def admin_delete(id):
        cursor = db.connection.cursor()
        cursor.execute("SELECT imgprofile FROM user WHERE id=%s", (id,))
        fila=cursor.fetchall()
        os.remove(os.path.join(UNItemsApp.config['folder'],fila[0][0]))
        cursor.execute("DELETE FROM user WHERE id=%s",(id,))
        db.connection.commit()
        flash('Usuario eliminado exitosamente')
        return redirect(url_for('admin_operations'))
    
    # Editar usuario - Ruta del botón --------->
@UNItemsApp.route('/update-admin-btn/<int:id>')
def admin_update_btn(id,):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE id=%s", (id,))
    data = cursor.fetchall()
    return render_template('edit-admin.html', user = data)

    # Editar - Actualización de los datos de usuario --------->
@UNItemsApp.route('/edit-user/<int:id>', methods = ['POST'])
def admin_update(id,):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        auth = request.form['auth']
        hash = generate_password_hash(password)
        img = request.files['img']    
        updateUser = db.connection.cursor()

        if request.files.get('img'):
            folder = '/Proyecto Aprender A/uploads/profile{}'.format(img)
            if os.path.exists(folder):
                os.remove(folder)
            img = request.files['img']
            filename = secure_filename(img.filename)
            img.save(os.path.join(UNItemsApp.config['folder'], filename))
            updateUser.execute("UPDATE user SET username = %s, email = %s, password = %s, auth = %s, imgprofile = %s WHERE id=%s", (username, email, hash, auth, filename, id,))
            db.connection.commit()
    flash("Actualización de datos completada")
    return redirect(url_for('admin_operations'))

  # Agregar comentario - Ruta del botón --------->
@UNItemsApp.route('/admin-add-comments', methods = ['GET', 'POST'])
@login_required
def admin_add_comments():
    if request.method == 'POST':
        date = request.form['date']
        contents = request.form['contents']

        addComments = db.connection.cursor()
        query = "INSERT INTO comments (date, contents) VALUES (%s, %s)"
        addComments.execute(query, (date, contents))
        db.connection.commit()
        flash("Comentario agregado")
        return redirect(url_for('admin-comments-operations'))
    else:
        flash('¡Algo salió mal!')
    return render_template('comments-operations.html')
    
    # Eliminar comentario - Ruta del botón --------->
@UNItemsApp.route('/delete-comments/<int:idc>')
def admin_delete_comments(idc):
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM comments WHERE idc = {0}".format(idc))
        db.connection.commit()
        flash('Comentario eliminado exitosamente')
        return redirect(url_for('admin_operations'))

    # Editar comentario ------->
@UNItemsApp.route('/admin-update-comments/<int:idc>', methods = ['GET', 'POST'])
def admin_update_comments(idc,):
    data_comments = addComments.fetchall()
    if request.method == 'POST':
        date = request.form['date']
        contents = request.form['contents']
        addComments = db.connection.cursor()
        addComments.execute("UPDATE comments SET date = %s, contents = %s WHERE idc=%s", (date, contents, idc,))
        db.connection.commit()
    flash("Actualización de datos completada")
    return render_template('articles-operations.html', comments = data_comments)

    # Editar comentario - Ruta del botón --------->
@UNItemsApp.route('/admin-comments-update/<int:idc>')
def admin_comments_update(idc):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM comments WHERE idc = {0}".format(idc))
    data = cursor.fetchall()
    return render_template('admin-edit-comments.html', comments = data)

@UNItemsApp.route('/admin-comments-operations', methods = ['GET', 'POST'])
@login_required
def comments_operations():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM comments")
    data = cursor.fetchall()
    return render_template('comments-operations.html', comments = data)


@UNItemsApp.route('/register')
def register():
    return render_template('register.html')

@UNItemsApp.route('/login')
def login():
    return render_template('login.html')



    # ==============================
    # Registro
    # ==============================
@UNItemsApp.route('/loginRegister', methods=['GET', 'POST'])
def loginRegister():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hash = generate_password_hash(password) 

        regUser = db.connection.cursor()
        query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
        regUser.execute(query, (username, email, hash))
        db.connection.commit()

        msg = Message(subject="Bienvenido a UNItems", recipients=[email], html=render_template ("mail-template.html"))
        mail.send(msg)
        return render_template('login.html')
    else:
        return render_template('register.html')

    # ==============================
    # Login
    # ==============================
@UNItemsApp.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        user = User(0, request.form['email'],  request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                if logged_user.auth == 'A':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta...")
                return render_template('login.html')
        else:
            flash("El usuario no se encuentra...")
            return render_template('login.html')
    else:
            return render_template('login.html')

# ========================
# Rutas de usuario ------>
# ========================
@UNItemsApp.route('/perfilUser')
@login_required
def perfilUser():
    return render_template('404.html')
    if not current_user.is_authenticated: # Definir current_user
        flash("Necesitas iniciar sesión para ver más")
        return render_template('login.html')
    else:
        return render_template('perfilUser.html')
            

@UNItemsApp.route('/edit-user', methods = ['GET', 'POST'])
@login_required
def edit_user():
    return render_template('edit-user.html')
# ========================
# Ruta del botón ------>
# ========================
@UNItemsApp.route('/edit-user-update/<int:id>', methods = ['POST'])
def update_user(id,):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        auth = request.form['auth']
        hash = generate_password_hash(password)
        img = request.files['img']    
        updateUser = db.connection.cursor()

        if request.files.get('img'):
            folder = '/UNItemsApp/uploads/profile{}'.format(img)
            if os.path.exists(folder):
                os.remove(folder)
            img = request.files['img']
            filename = secure_filename(img.filename)
            img.save(os.path.join(UNItemsApp.config['folder'], filename))
            updateUser.execute("UPDATE user SET username = %s, email = %s, password = %s, auth = %s, imgprofile = %s WHERE id=%s", (username, email, hash, filename, id,))
            db.connection.commit()
    flash("Actualización de datos completada")
    return redirect(url_for('perfilUser'))


# ========================
# Rutas de los comentarios ------>
# ========================
@UNItemsApp.route('/comments', methods = ['GET', 'POST'])
@login_required
def comments():
    return render_template('comments.html')

# ========================
# Ruta del botón ------>
# ========================
@UNItemsApp.route('/add-comments', methods = ['GET', 'POST'])
@login_required
def add_comments():
    if request.method == 'POST':
        date = request.form['date']
        contents = request.form['contents']

        addComments = db.connection.cursor()
        query = "INSERT INTO comments (date, contents) VALUES (%s, %s)"
        addComments.execute(query, (date, contents))
        db.connection.commit()
    flash("Comentario agregado")
    return redirect(url_for('perfilUser'))

@UNItemsApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@UNItemsApp.route('/passwordRecovery/<int:id>')
def passwordR(id,):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hash = generate_password_hash(password) 
        passwordchange = db.connection.cursor()
        passwordchange.execute("UPDATE user SET email = %s, password= %s WHERE id=%s", (email, hash, id,))
        db.connection.commit()
        flash('Contraseña actualizada')
        return redirect(url_for('admin_operations'))
    else:
        flash('¡Algo salió mal!')
    return render_template('passwordRecovery.html')

@UNItemsApp.errorhandler(404)
def errorhandler401(e):
    return render_template('Error401.html')

@UNItemsApp.route("/home")    
@login_required
def home():
    return render_template('home.html')


if __name__=='__main__':
    UNItemsApp.config.update(DEBUG=True, SECRET_KEY="secret_sauce")
    UNItemsApp.config['ALLOWED_IMAGE_EXTENSIONS'] = ['txt', 'pdf', 'JPEG','JPG','PNG','WEBP', 'GIF']
    UNItemsApp.run(debug=True, port=3300)
