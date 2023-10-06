# intalar pymongo, certifi, pymongo[srv]
# python -m pip install ...

from pymongo import MongoClient
    # intalar pymongo==3.12, certifi, pymongo[srv]

import certifi
from pymongo.collection import ReturnDocument
from pymongo import MongoClient

# Conexión con MongoDB
MONGO = 'mongodb+srv://Luis:Luis@cluster0.kivvm0e.mongodb.net/?retryWrites=true&w=majority'

# Utilización del certificado
certificado = certifi.where()

# Función para la conexión con la DB
def Conexion():
    try:
        client = MongoClient(MONGO, tlsCAFile = certificado)
        bd = client["bd_pruebasaber"]
    except ConnectionError:
        print("Error de Conexión")
    return bd