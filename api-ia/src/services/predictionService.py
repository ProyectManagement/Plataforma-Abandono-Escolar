import pandas as pd
import pickle
from src.utils.helpers import get_mongo_collection
import os
from dotenv import load_dotenv
from src.preprocessing.dataPreprocessing import preprocess_data

load_dotenv()

class PredictionService:
    def __init__(self):
        # Cargar modelo y preprocesador
        self.model_path = os.getenv('MODEL_PATH')
        self.preprocessor_path = os.getenv('PREPROCESSOR_PATH')
        
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(self.preprocessor_path, 'rb') as f:
            self.preprocessor = pickle.load(f)
    
    def predict(self, data: dict) -> str:
        # Convertir datos a DataFrame
        df = pd.DataFrame([data])
        
        # Preprocesar datos
        X_processed, _ = preprocess_data(df)
        
        # Realizar predicción
        prediction = self.model.predict(X_processed)[0]
        
        # Mapear clases
        return {
            0: 'bajo',
            1: 'medio',
            2: 'alto'
        }.get(prediction, 'desconocido')