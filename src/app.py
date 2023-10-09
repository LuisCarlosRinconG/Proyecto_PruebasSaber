from flask import Flask, redirect, render_template, request, url_for
from config import *
from user import User


# Instancias para realizar operaciones con la DB
con_bd = Conexion()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Crear usuario
@app.route('/registro')
def registro():
    # Se modifica la vista index para poder hacer el muestreo de los datos
    usuarios = con_bd['Usuarios']
    UsuariosRegistradas=usuarios.find()
    return render_template('registro.html', usuarios = UsuariosRegistradas)


# Ruta para guardar los datos de la DB
@app.route('/guardar_usuarios', methods = ['POST'])
def agregarUser():
    usuarios = con_bd['Usuarios']
    nombre = request.form['nombre']
    email = request.form['email']
    departamento = request.form['departamento']
    cumple = request.form['cumple']
    password = request.form['password']
    roll=' '

    if nombre and email and departamento and cumple and password and roll:
        user = User(nombre, email, departamento, cumple, password, roll)
        #insert_one para crear un documento en Mongo
        usuarios.insert_one(user.formato_doc())
        return redirect(url_for('registro'))
    else:
        return "Error"

@app.route('/login')
def login():
    # Lógica para mostrar la página de inicio de sesión
    return render_template('login.html')

#Validación de usuario
@app.route('/validar', methods = ['POST'])
def validar():
    # Obtener datos del formulario
    email = request.form['email']
    password = request.form['password']
    roll='Admin'
    roll2='Usuario'
    
    # Realizar la búsqueda en la base de datos para verificar la autenticación
    usuarios = con_bd['Usuarios']
    user_Admin = usuarios.find_one({"email": email,"password": password,"roll":roll})
    user_Usuario = usuarios.find_one({"email": email,"password": password,"roll":roll2})
    
    if user_Admin:

        return render_template('admin.html', email=email)
    elif user_Usuario:

        return render_template('usuario.html', email=email)
    else:
        # Autenticación fallida, mostrar un mensaje de error
        return "Error de autenticación, Contraseña incorrecta"

# Ruta de usuario
@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

# Ruta de administrador
@app.route('/admin')
def admin():
    return render_template('admin.html') 

# Ruta de error 404
def error_404(error):
    return render_template('error_404.html'), 404

if __name__ == '__main__':
    app.register_error_handler(404, error_404)
    app.run(debug = True, port = 2001)
















    
'''
# En este caso se eliminara atravez de la URL
# Ruta para eliminar datos en la DB donde la ruta se llama eliminar_persona y recibe un parametro llamado nombre_persona
@app.route('/eliminar_usuarios/<string:usuario_user>')
def eliminar(usuario_user):
    usuarios = con_bd['Usuarios']
    # Se hace uso de delete_one para borrar los datos de la DB personas donde el dato que se elimina es el que se para como argumento para nombre
    usuarios.delete_one({ 'usuario': usuario_user})
    # Creamos un redireccionamiento que redirija a la vista index
    return redirect(url_for('registro'))

#Editar o actualizar el contenido 
@app.route('/editar_usuarios/<string:usuario_user>', methods = ['POST'])
def editar(usuario_user):
    usuarios = con_bd['Usuarios']
    # Se realiza el mismo proceso de inserción y extracción para poder actualizar los datos
    usuario = request.form['usuario']
    roll = request.form['roll']
    password = request.form['password']
    # Utilizaremos la función update_one()
    if usuario and roll and password:
        usuarios.update_one({'usuario': usuario_user}, 
                            {'$set': {'usuario' : usuario , 'roll': roll, 'password': password}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('registro'))
    else:
        return "Error de actualización"

'''