from multiprocessing import connection
import re
from flask import Flask, render_template, session, url_for, request, redirect, jsonify, flash, send_from_directory
import requests
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
from email.message import  EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# Models:
from models.modelUser import ModelUser
from models.modelFeed import ModelFeed

# Entities:
from models.entities.User import User
from models.entities.Feeds import Feeds

UNItemsApp = Flask(__name__)
UNItemsApp.config.from_object(config['development'])

# Objects: 
mail = Mail(UNItemsApp) 
csrf = CSRFProtect(UNItemsApp)
db = MySQL(UNItemsApp)
login_manager_app = LoginManager(UNItemsApp)
folder = os.path.join(os.path.dirname(__file__), 'uploads/profile')
UNItemsApp.config['folder'] = folder
folder_feeds = os.path.join(os.path.dirname(__file__), 'uploads/feeds')
UNItemsApp.config['folder_feeds'] = folder_feeds
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

@UNItemsApp.route('/', methods = ['GET', 'POST'])
def index():        
    if request.method == 'POST':
        date = request.form['date']
        content = request.form['content']

        addComments = db.connection.cursor()
        query = "INSERT INTO comments (date, content) VALUES (%s, %s)"
        addComments.execute(query, (date, content))
        db.connection.commit()
    flash("Comentario agregado")
    return render_template('landing-home.html')
    
    
# ==============================
# Rutas administrador y modales
# ==============================
@UNItemsApp.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@UNItemsApp.route('/admin-view', methods = ['GET', 'POST'])
@login_required
def admin_view():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    return render_template('admin-view.html', user = data)

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
        
        msg = Message(subject="Bienvenido a UNItems", recipients=[email], html=render_template ("mail-template.html"))
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

@UNItemsApp.route('/welcomeMail')
def welcomeMail():
    return render_template('welcomeMail.html')
@UNItemsApp.route('/register')
def register():
    return render_template('register.html')

@UNItemsApp.route('/login')
def login():
    return render_template('login.html')

    # ==============================
    # Registro
    # ==============================

@UNItemsApp.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hash = generate_password_hash(password) 

        # Validación
        existing_user = db.connection.execute("SELECT 1 FROM user WHERE username = %s OR email = %s LIMIT 1", (username, email)).fetchone()
        if existing_user:
            existing_username = db.connection.execute("SELECT username FROM user WHERE username = %s", (username,)).fetchone()
            existing_email = db.connection.execute("SELECT email FROM user WHERE email = %s", (email,)).fetchone()
            if existing_username:
                flash("El nombre de usuario ya está en uso.")
                return render_template("login.html", error="Nombre de usuario repetido")
            if existing_email:
                flash("El correo electrónico ya está en uso.")
                return render_template("login.html", error="Correo electrónico repetido")
        addUser = db.connection.cursor()
        query = "INSERT INTO user (fullname, username, email, password) VALUES (%s, %s, %s, %s)"
        addUser.execute(query, (fullname, username, email, hash))
        db.connection.commit()

        # Enviar correo de bienvenida
        msg = Message(subject="Bienvenido a UNItems, {}".format(fullname), recipients=[email], html=render_template("welcomeMail.html", fullname=fullname))
        mail.send(msg)
        return render_template('login.html')
    else:
        return render_template('login.html')

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
                session['username'] = logged_user.username
                session['email'] = logged_user.email
                session['auth'] = logged_user.auth
                
                if logged_user.auth == 'A':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
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
    return render_template('perfilUser.html')

@UNItemsApp.route('/notification', methods=['POST'])
def notification():
    """
    Esta función maneja la recepción de notificaciones de Telegram.
    
    Enviará un mensaje de respuesta en caso de que se reciba una notificación.
    """
    update = request.get_json()
    if 'message' in update:
        message_text = update['message']['text']
        chat_id = update['message']['chat']['id']
        response = "¡Hola! Has recibido el mensaje: {0}".format(message_text)
        data = {"chat_id": chat_id, "text": response}
        send_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(os.environ.get('TELEGRAM_BOT_TOKEN'))
        requests.post(send_message_url, json=data)
    return '', 200
    return render_template('perfilUser.html')


@UNItemsApp.route('/edit-user', methods = ['GET', 'POST'])
@login_required
def edit_user():
    return render_template('edit-user.html')
# ========================
# Ruta del botón ------>
# ========================

@UNItemsApp.route('/edit-user-update/<int:id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        fullname = request.form['fullname']
        age = request.form['age']
        schoolgrade = request.form['schoolgrade']
        user_resume = request.form['user_resume']

        # Chequeo de unicidad de username y email excepto si es el mismo usuario
        cursor = db.connection.cursor()
        query = ("SELECT COUNT(*) FROM user WHERE "
                 "username = %s AND id != %s OR "
                 "email = %s AND id != %s")
        data = (username, id, email, id)
        cursor.execute(query, data)
        count = cursor.fetchone()[0]
        cursor.close()  # Cerrar el cursor
        if count > 0:
            error = 'El nombre de usuario o el correo electrónico ya están en uso.'
            flash(error, 'error')
            return redirect(url_for('edit_user', id=id))

        # Actualizar datos
        updateUser = db.connection.cursor()
        query = "UPDATE user SET username = %s, email = %s, fullname = %s, age = %s, schoolgrade = %s, user_resume = %s WHERE id = %s"
        datos = (username, email, fullname, age, schoolgrade, user_resume, id)
        updateUser.execute(query, datos)
        db.connection.commit()
        # Actualizar imagen de perfil
        if 'img' in request.files:
            img = request.files['img']
            if img.filename != '':
                folder = '/UNItemsApp/uploads/profile{0}'.format(id)
                if os.path.exists(folder):
                    os.remove(folder)
                filename = secure_filename(img.filename)
                img.save(os.path.join(UNItemsApp.config['folder'], filename))
                updateUser.execute("UPDATE user SET imgprofile = %s WHERE id=%s", (filename, id))
                db.connection.commit()
    flash("Actualización de datos completada")
    return redirect(url_for('perfilUser'))


# ========================
# Rutas de los comentarios ------>
# ========================
@UNItemsApp.route('/comments', methods = ['GET', 'POST'])
@login_required
def comments():
    """
    A route decorator that handles the '/comments' endpoint. This function is used to display the 'comments.html' template.
    
    This route supports both GET and POST requests. The function is decorated with the '@login_required' decorator, which means that the user must be logged in to access this route.
    
    Returns:
        A rendered template of 'comments.html'.
    """
    return render_template('comments.html')

# ========================
# Ruta del botón ------>
# ========================
@UNItemsApp.route('/comming-soon')
def comming_soon():
    return render_template('comming-soon.html')

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


@UNItemsApp.route('/us', methods = ['GET', 'POST'])
def collab():
    return render_template('collab.html')

@UNItemsApp.route('/faqs', methods = ['GET', 'POST'])
def faqs():
    return render_template('faqs.html')

@UNItemsApp.route('/news', methods = ['GET', 'POST'])
def news():
    return render_template('news.html')

@UNItemsApp.route('/feed', methods = ['GET', 'POST'])
@login_required
def feed():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM feeds")
    data = cursor.fetchall()
    return render_template('feed.html', feeds = data)

@UNItemsApp.route('/send-feed', methods = ['GET', 'POST'])
@login_required
def send_feed():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        imgcontent = request.files['imgcontent']
        # Guardarimagen del post
        if imgcontent and allowed_file(imgcontent.filename, UNItemsApp.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(imgcontent.filename)
            imgcontent.save(os.path.join(UNItemsApp.config['folder'], filename))
            imgcontent = filename
        else:
            flash('El tipo de archivo no es permitido')
            return redirect(url_for('feed'))

        # current_user es un objeto que se encarga de la autenticacion de los usuarios
        author_id = current_user.get_id()

        try:
            sendFeed = db.connection.cursor()
            sendFeed.execute("INSERT INTO feeds (title, content, imgcontent, author_id) VALUES (%s, %s, %s, %s)", (title, content, imgcontent, author_id))
            db.connection.commit()
        except Exception as e:
            db.connection.rollback()
            flash('Ha ocurrido un error al guardar el post')
            return redirect(url_for('feed'))

        db.connection.commit()
        return redirect(url_for('feed'))
    return render_template('feed.html')

def allowed_file(filename, ALLOWED_EXTENSIONS):
    """
    Comprueba si un archivo tiene una extension valida
    """
    return '.' in filename and \
           filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@UNItemsApp.errorhandler(500)
def errorhandler500(e):
    return render_template('500.html')
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