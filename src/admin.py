# Crear y almacenar objetos en la base de datos

class Admin:
    def __init__(self, actividad, descripcion, equipo, fechaI, fechaF, estado, comentarios):
        self.actividad= actividad
        self.descripcion= descripcion
        self.equipo = equipo
        self.fechaI = fechaI
        self.fechaF = fechaF
        self.estado=estado
        self.comentarios=comentarios
    
    # Metodo para almacenar los documentos
    def formato_doc(self):
        return{
            'actividad':self.actividad,
            'descripcion': self.descripcion,
            'equipo':self.equipo,
            'fechaI':self.fechaI,
            'fechaF': self.fechaF,
            'estado':self.estado,
            'comentarios':self.comentarios
        }
