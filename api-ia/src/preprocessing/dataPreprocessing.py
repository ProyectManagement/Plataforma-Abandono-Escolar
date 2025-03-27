import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def flatten_data(df: pd.DataFrame) -> pd.DataFrame:
    flat_data = []
    
    for _, row in df.iterrows():
        flat_row = {}
        
        # Campos planos
        flat_row['id_alumno'] = row.get('id_alumno', None)  # Mantener id_alumno
        flat_row['numero_hijos'] = row.get('numero_hijos', 0)
        flat_row['depende_economicamente'] = row.get('depende_economicamente', None)
        
        # Desanidar aspectos_socioeconomicos
        aspectos_soc = row.get('aspectos_socioeconomicos', {})
        if aspectos_soc is None:
            aspectos_soc = {}  # Asignar un diccionario vacío si es None
        
        flat_row['aspectos_socioeconomicos_trabaja'] = aspectos_soc.get('trabaja', 'No')  # Valor predeterminado
        flat_row['aspectos_socioeconomicos_horas_trabajo'] = aspectos_soc.get('horas_trabajo', 0)  # Valor predeterminado
        flat_row['aspectos_socioeconomicos_ingreso_mensual'] = aspectos_soc.get('ingreso_mensual', 0)  # Valor predeterminado
        
        # Desanidar condiciones_salud
        condiciones_salud = row.get('condiciones_salud', {})
        if condiciones_salud is None:
            condiciones_salud = {}  # Asignar un diccionario vacío si es None
        
        flat_row['condiciones_salud_padecimiento_cronico'] = condiciones_salud.get('padecimiento_cronico', False)
        flat_row['condiciones_salud_alergias'] = condiciones_salud.get('alergias', False)
        
        # Agregar fila al DataFrame plano
        flat_data.append(flat_row)
    
    # Convertir a DataFrame
    flat_df = pd.DataFrame(flat_data)
    return flat_df

def preprocess_data(df: pd.DataFrame):
    numeric_features = [
        'numero_hijos',
        'aspectos_socioeconomicos_ingreso_mensual'
    ]

    categorical_features = [
        'depende_economicamente',
        'aspectos_socioeconomicos_trabaja',
        'aspectos_socioeconomicos_horas_trabajo',
        'condiciones_salud_padecimiento_cronico',
        'condiciones_salud_alergias'
    ]
    
    # Filtrar características numéricas y categóricas para incluir solo las presentes en el DataFrame
    numeric_features = [col for col in numeric_features if col in df.columns]
    categorical_features = [col for col in categorical_features if col in df.columns]
    
    # Crear pipeline para características numéricas y categóricas
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    # Aplicar preprocesamiento
    processed_data = preprocessor.fit_transform(df)
    
    return processed_data, preprocessor