import os
import pickle
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.preprocessing.dataPreprocessing import preprocess_data

# Cargar variables de entorno
load_dotenv()

def load_and_merge_data():
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('DB_NAME')]
    
    # Cargar datos de encuestas
    encuestas_collection = db[os.getenv('COLLECTION_ENCUESTAS')]
    encuestas_data = list(encuestas_collection.find({}, {
        '_id': 1,
        'id_alumno': 1,
        'numero_hijos': 1,
        'depende_economicamente': 1,
        'aspectos_socioeconomicos': 1,
        'condiciones_salud': 1
    }))
    print("Datos brutos de Encuestas:")
    for doc in encuestas_data[:5]:
        print(doc)
    
    encuestas_df = pd.DataFrame(encuestas_data)
    encuestas_df.rename(columns={'_id': 'clave_unica'}, inplace=True)
    
    return encuestas_df

def train_model():
    print("Iniciando el proceso de entrenamiento...")
    
    # Cargar datos
    df = load_and_merge_data()
    print("Datos cargados:")
    print(df.head())
    
    # Separar características
    X = df.drop(columns=['id_alumno', 'clave_unica'])  # Excluir id_alumno y clave_unica
    
    # Preprocesar datos
    X_processed, preprocessor = preprocess_data(X)
    print("Características procesadas:")
    print(X_processed)
    
    # Verificar si existe un modelo entrenado
    model_path = os.getenv('MODEL_PATH')
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print("Modelo cargado desde archivo.")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            raise ValueError("No se pudo cargar el modelo. Entrena el modelo nuevamente.")
    else:
        # Entrenar un nuevo modelo
        print("Entrenando un nuevo modelo...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Generar predicciones simuladas (sin etiquetas reales)
        y = [0] * len(X_processed)  # Etiquetas ficticias para entrenamiento inicial
        model.fit(X_processed, y)
        
        # Guardar el modelo y el preprocesador
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Modelo guardado en: {model_path}")
        
        with open(os.getenv('PREPROCESSOR_PATH'), 'wb') as f:
            pickle.dump(preprocessor, f)
        print(f"Preprocesador guardado en: {os.getenv('PREPROCESSOR_PATH')}")
    
    # Generar predicciones
    predictions = model.predict(X_processed)
    df['prediccion'] = predictions
    print("Predicciones generadas:")
    print(df[['id_alumno', 'clave_unica', 'prediccion']])
    
    # Almacenar predicciones en MongoDB
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('DB_NAME')]
    predicciones_collection = db[os.getenv('COLLECTION_PREDICCIONES')]
    
    for _, row in df.iterrows():
        prediccion_data = {
            'id_encuesta': row['clave_unica'],  # Referencia al _id de la encuesta
            'id_alumno': row['id_alumno'],  # Identificador del alumno
            'riesgo': ['Bajo', 'Medio', 'Alto'][row['prediccion']]  # Mapear números a etiquetas
        }
        predicciones_collection.insert_one(prediccion_data)
    
    print("Predicciones almacenadas en MongoDB.")

if __name__ == "__main__":
    train_model()