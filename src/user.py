# Crear y almacenar objetos en la base de datos

class User:
    def __init__(self, usuario, roll, password):
        self.usuario = usuario
        self.roll = roll
        self.password = password
    
    # Metodo para almacenar los documentos
    def formato_doc(self):
        return{
            'usuario': self.usuario,
            'roll': self.roll,
            'password': self.password    
        }