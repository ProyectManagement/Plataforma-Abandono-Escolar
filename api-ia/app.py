from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.services.predictionService import PredictionService
from src.utils.helpers import get_mongo_collection
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI()
mongo_collection = get_mongo_collection(os.getenv('COLLECTION_PREDICCIONES'))

# Carga del servicio de predicción
prediction_service = PredictionService()

class AspectosSocioeconomicos(BaseModel):
    trabaja: str
    horas_trabajo: str
    nombre_trabajo: str
    direccion_trabajo: str
    dias_trabajo: str
    horario_trabajo: str
    ingreso_mensual: str
    dependencia_economica: str
    vive_con: str

class AportantesGastoFamiliar(BaseModel):
    padre: bool
    madre: bool
    hermanos: bool
    abuelos_maternos: bool
    abuelos_paternos: bool
    parientes: bool
    ingreso_familiar: str

class CondicionesSalud(BaseModel):
    condiciones: list
    otro: str
    padecimiento_cronico: bool
    nombre_padecimiento: str
    alergias: bool
    nombre_alergia: str
    toma_medicamentos: bool
    nombre_medicamento: str
    atencion_psicologica: bool
    motivo_atencion: str

class AnalisisAcademico(BaseModel):
    tipo_escuela_previa: str
    modalidad_previa: str
    institucion_previa: str
    especialidad_previa: str
    municipio_institucion: str
    estado_institucion: str

class ExpectativasEducativasOcupacionales(BaseModel):
    espacio_laboral_preferido: str
    posibilidades_trabajo: str

class StudentData(BaseModel):
    id_grupo: str
    id_carrera: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    numero_hijos: int
    depende_economicamente: str
    aspectos_socioeconomicos: AspectosSocioeconomicos
    aportantes_gasto_familiar: AportantesGastoFamiliar
    edad_integrantes_familia: list
    condiciones_salud: CondicionesSalud
    analisis_academico: AnalisisAcademico
    expectativas_educativas_ocupacionales: ExpectativasEducativasOcupacionales

@app.post("/predict")
async def predict(student: StudentData):
    try:
        # Realizar predicción
        prediction = prediction_service.predict(student.dict())
        
        # Guardar en MongoDB
        result = {
            "input_data": student.dict(),
            "prediction": prediction,
            "timestamp": datetime.now()
        }
        mongo_collection.insert_one(result)
        
        return {"prediction": prediction}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))