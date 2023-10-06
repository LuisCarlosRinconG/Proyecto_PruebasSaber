from flask import Flask, redirect, render_template, request, url_for
from config import *
from user import User


# Instancias para realizar operaciones con la DB
con_bd = Conexion()

app = Flask(__name__)

@app.route('/')
def index():
    # Se modifica la vista index para poder hacer el muestreo de los datos
    usuarios = con_bd['Usuarios']
    UsuariosRegistradas=usuarios.find()
    return render_template('index.html', usuarios = UsuariosRegistradas)


# Ruta para guardar los datos de la DB
@app.route('/guardar_usuarios', methods = ['POST'])
def agregarUser():
    usuarios = con_bd['Usuarios']
    usuario = request.form['usuario']
    roll = request.form['roll']
    password = request.form['password']

    if usuario and roll and password:
        user = User(usuario, roll, password)
        #insert_one para crear un documento en Mongo
        usuarios.insert_one(user.formato_doc())
        return redirect(url_for('index'))
    else:
        return "Error"
    

# En este caso se eliminara atravez de la URL
# Ruta para eliminar datos en la DB donde la ruta se llama eliminar_persona y recibe un parametro llamado nombre_persona
@app.route('/eliminar_usuarios/<string:usuario_user>')
def eliminar(usuario_user):
    usuarios = con_bd['Usuarios']
    # Se hace uso de delete_one para borrar los datos de la DB personas donde el dato que se elimina es el que se para como argumento para nombre
    usuarios.delete_one({ 'usuario': usuario_user})
    # Creamos un redireccionamiento que redirija a la vista index
    return redirect(url_for('index'))

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
        return redirect(url_for('index'))
    else:
        return "Error de actualización"
    


#Validación 
@app.route('/validar', methods = ['POST'])
def validar():
    usuarios = con_bd['Usuarios']
    # Se realiza el mismo proceso de inserción y extracción para poder actualizar los datos
    usuario = request.form['usuario']
    roll = request.form['roll']
    password = request.form['password']
    
    # Obtén una referencia a la colección "usuarios"
    usuarios = con_bd.Usuarios

    # Define una proyección para obtener solo la columna "nombre"
    proyeccion = {"usuario": 1, "_id": 0}  # El valor 1 indica que deseas incluir este campo, el valor 0 indica que no deseas incluir el campo "_id"

    # Realiza la búsqueda y obtén el cursor
    vusuario = usuarios.find({}, proyeccion)

    # Itera a través del cursor para obtener los documentos
    for usuario in vusuario:
        nombre = usuario.get("usuario", "Nombre no encontrado")
        print(nombre)

    if usuario==vusuario:
        return render_template('login.html')
    else:
        return "Error de actualización"


if __name__ == '__main__':
    app.run(debug = True, port = 2001)