class Perfil:
    def __init__(self, cc, nombre, apellido, telefono ,cargo, sexo):
        self.cc= cc
        self.nombre= nombre
        self.apellido = apellido
        self.telefono = telefono
        self.cargo = cargo
        self.sexo= sexo
    
    # Metodo para almacenar los documentos
    def formato_doc(self):
        return{
            'cc':self.cc,
            'nombre': self.nombre,
            'apellido':self.apellido,
            'telefono':self.telefono,
            'cargo':self.cargo,
            'sexo': self.sexo
        }