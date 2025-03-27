from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def test_mongo_connection():
    try:
        # Cargar variables de entorno
        mongo_uri = os.getenv('MONGO_URI')
        db_name = os.getenv('DB_NAME')
        collection_encuestas = os.getenv('COLLECTION_ENCUESTAS')
        collection_predicciones = os.getenv('COLLECTION_PREDICCIONES')
        
        # Conectar a MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        # Verificar colecciones
        encuestas_collection = db[collection_encuestas]
        predicciones_collection = db[collection_predicciones]
        
        print("Conexión exitosa a MongoDB.")
        print(f"Colección 'encuestas' encontrada: {encuestas_collection.name}")
        print(f"Colección 'predicciones' encontrada: {predicciones_collection.name}")
        
        # Mostrar algunos documentos de prueba
        print("Primeros documentos en 'encuestas':")
        for doc in encuestas_collection.find().limit(5):
            print(doc)
        
        print("Primeros documentos en 'predicciones':")
        for doc in predicciones_collection.find().limit(5):
            print(doc)
    
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    test_mongo_connection()