# -*- coding: utf-8 -*-
"""
MÓDULO: data_engine.py
DESCRIPCIÓN: Utilitario para la generación y consulta de datos sintéticos de clientes en formato CSV.
"""
import pandas as pd
import os

def generar_base_datos_sintetica():
    """Genera un archivo CSV con registros de prueba para el motor de evaluación."""
    data_clientes = {
        'cliente_id': ['C001', 'C002', 'C003'],
        'nombre': ['Carlos Mendoza', 'Ana Gomez', 'Roberto Torres'],
        'documento': ['12345678', '87654321', '11223344'],
        'ingresos_mensuales': [4500, 1200, 1500], # C002 tiene error (debió ser 12000)
        'score_externo': [450, 720, 310],
        'alerta_antecedentes': [False, False, True]
    }
    
    df = pd.DataFrame(data_clientes)
    path_csv = 'clientes_infraestructura.csv'
    df.to_csv(path_csv, index=False, encoding='utf-8')
    print(f"[DATA ENGINE] Base de datos sintética creada exitosamente en: '{path_csv}'")

def obtener_cliente_por_id(cliente_id: str) -> dict:
    """Busca un cliente en el CSV y lo retorna como un diccionario listo para el Estado."""
    path_csv = 'clientes_infraestructura.csv'
    if not os.path.exists(path_csv):
        generar_base_datos_sintetica()
        
    df = pd.DataFrame(pd.read_csv(path_csv))
    filtro = df[df['cliente_id'] == cliente_id]
    
    if filtro.empty:
        raise ValueError(f"Cliente con ID {cliente_id} no localizado.")
        
    row = filtro.iloc[0]
    return {
        "cliente_id": str(row['cliente_id']),
        "nombre": str(row['nombre']),
        "documento": str(row['documento']),
        "datos_extraidos": {
            "ingresos_mensuales": int(row['ingresos_mensuales']),
            "score_externo": int(row['score_externo']),
            "alerta_antecedentes": bool(row['alerta_antecedentes'])
        },
        "resultado_listas": "",
        "score_riesgo": 0,
        "decision": "",
        "eventos": []
    }

if __name__ == "__main__":
    generar_base_datos_sintetica()