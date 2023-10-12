from flask import Flask, redirect, render_template, request, url_for
from config import *
from user import User
from admin import Admin

# Instancias para realizar operaciones con la DB
con_bd = Conexion()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

#Ruta sobre nosotros
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

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

# Validación de usuario
@app.route('/validar', methods=['POST'])
def validar():
    # Obtener datos del formulario
    email = request.form['email']
    password = request.form['password']
    roll = 'admin'
    roll2 = 'usuario'

    # Realizar la búsqueda en la base de datos para verificar la autenticación
    usuarios = con_bd['Usuarios']
    user_Admin = usuarios.find_one({"email": email, "password": password, "roll": roll})
    user_Usuario = usuarios.find_one({"email": email, "password": password, "roll": roll2})

    if user_Admin:
        actividades = con_bd['Actividades']
        ActividadesRegistradas = actividades.find()
        return render_template('admin.html', actividades=ActividadesRegistradas)
    elif user_Usuario:
        return redirect(url_for('usuario', email=email, password=password))

    else:
        # Autenticación fallida, mostrar un mensaje de error
        return "Error de autenticación, Contraseña o usuario incorrectos o espere que se le sea delegado un rol"

# Ruta de usuario
@app.route('/usuario')
def usuario():
    # Obtener los parámetros de la URL usando request.args
    email = request.args.get('email')
    password = request.args.get('password')

    roll = 'admin'
    roll2 = 'usuario'
    # Equipo correspondiente a user_Usuario
    usuarios = con_bd['Usuarios']
    user_Usuario = usuarios.find_one({"email": email, "password": password, "roll": roll2})
    if user_Usuario:
        equipo_usuario = user_Usuario.get("departamento", "")
        if equipo_usuario:
            actividades = con_bd['Actividades']
            AcividadesRegistradas = actividades.find({"equipo": equipo_usuario, "estado": "activo"})
            url_for('historial', email=email, password=password)
            return render_template('usuario.html', actividades=AcividadesRegistradas)
    return "Error de ingreso"

# Ruta de Historail
@app.route('/historial')
def historial():
    actividades = con_bd['Actividades']
    ActividadesRegistradas=actividades.find({"estado": {"$in": ["finalizado", "cancelado"]}
            })
    return render_template('historial.html', actividades = ActividadesRegistradas)

#Actualizar el comentario de usuario
@app.route('/editar_Comentario/<string:actividad_buscada>', methods = ['POST'])
def editar_Comentario(actividad_buscada):
    acividades = con_bd['Actividades']
    comentarios=request.form['comentarios']
    # Utilizaremos la función update_one()
    if comentarios:
        acividades.update_one({'actividad': actividad_buscada}, 
                            {'$set': {'comentarios': comentarios}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('historial'))
    else:
        return "Error de actualización"

# Ruta de editar aacividad
@app.route('/usuarioBusqueda/<string:actividad_buscada>', methods = ['POST'])
def usuarioBusqueda(actividad_buscada):

    acividades = con_bd['Actividades']
    actividad= request.form['actividad']
    descripcion = request.form['descripcion']
    equipo = request.form['equipo']
    fechaI = request.form['fechaI']
    fechaF = request.form['fechaF']
    estado = request.form['estado']
    comentarios=request.form['comentarios']

    if actividad and descripcion and equipo and fechaI and fechaF and estado and comentarios:
        admin = Admin(actividad, descripcion, equipo, fechaI, fechaF, estado, comentarios)
        #insert_one para crear un documento en Mongo
        acividades.update_one({'actividad': actividad_buscada}, 
                            {'$set': {'actividad' : actividad, 'descripcion': descripcion, 'equipo': equipo,'fechaI' : fechaI, 'fechaF': fechaF, 'estado': estado, 'comentarios': comentarios}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('usuario'))
    else:
        return "Error"
    
# Ruta de error 404
def error_404(error):
    return render_template('error_404.html'), 404


# Ruta de administrador
@app.route('/admin')
def admin():
    actividades = con_bd['Actividades']
    ActividadesRegistradas=actividades.find()
    return render_template('admin.html', actividades = ActividadesRegistradas)

# Ruta para guardar los datos de la actividades de la DB
@app.route('/agregarActividad', methods = ['POST'])
def agregarActividad():
    acividades = con_bd['Actividades']
    actividad= request.form['actividad']
    descripcion = request.form['descripcion']
    equipo = request.form['equipo']
    fechaI = request.form['fechaI']
    fechaF = request.form['fechaF']
    estado = request.form['estado']
    comentarios=request.form['comentarios']

    if actividad and descripcion and equipo and fechaI and fechaF and estado and comentarios:
        admin = Admin(actividad, descripcion, equipo, fechaI, fechaF, estado, comentarios)
        #insert_one para crear un documento en Mongo
        acividades.insert_one(admin.formato_doc())
        return redirect(url_for('admin'))
    else:
        return "Error"

#Ruta para la pantalla de datos donde se muestra la data consultada
@app.route('/fechaBuscada',methods = ['POST'])
def Read():
    actividades = con_bd['Actividades']
    fechabuscada = request.form['fechaI']
    query={"fechaI":fechabuscada}
    AcividadesRegistradas=actividades.find(query)
    return render_template('datos.html', actividades = AcividadesRegistradas)

@app.route('/eliminar_Actividad/<string:ActividadElimin>')
def eliminar_Actividad(ActividadElimin):
    acividades = con_bd['Actividades']
    acividades.delete_one({ 'actividad': ActividadElimin})
    return redirect(url_for('admin'))

#Editar o actualizar el contenido de la actividad
@app.route('/editar_actividad/<string:actividad_buscada>', methods = ['POST'])
def editar(actividad_buscada):
    acividades = con_bd['Actividades']
    actividad= request.form['actividad']
    descripcion = request.form['descripcion']
    equipo = request.form['equipo']
    fechaI = request.form['fechaI']
    fechaF = request.form['fechaF']
    estado = request.form['estado']
    comentarios=request.form['comentarios']
    # Utilizaremos la función update_one()
    if actividad and descripcion and equipo and fechaI and fechaF and estado and comentarios:
        acividades.update_one({'actividad': actividad_buscada}, 
                            {'$set': {'actividad' : actividad, 'descripcion': descripcion, 'equipo': equipo,'fechaI' : fechaI, 'fechaF': fechaF, 'estado': estado, 'comentarios': comentarios}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('admin'))
    else:
        return "Error de actualización"

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