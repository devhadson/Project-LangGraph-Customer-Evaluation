"""
CASO DE PRUEBA 1: case_original_error.py
DESCRIPCIÓN: Ejecución del flujo original. Captura un valor de ingresos distorsionado
             provocando un dictamen desfavorable de "Revisión Manual".
"""
from data_engine import obtener_cliente_por_id
from app import app_evaluacion

def ejecutar_ruta_original():
    print("=" * 75)
    print(" INICIANDO EJECUCIÓN DEL CASO 1: RUTA TRANSACCIONAL ORIGINAL CON ERRORES")
    print("=" * 75)
    
    # 1. Definimos la clave de aislamiento de la transacción (Thread ID)
    config_hilo = {"configurable": {"thread_id": "TRANSACCION_ANA_GOMEZ"}}
    
    # 2. Extraemos el estado inicial corrupto desde el motor de datos (Ingresos: S/. 1,200)
    estado_inicial = obtener_cliente_por_id("C002")
    
    print(f"\n[DATOS CAPTURADOS] Cliente: {estado_inicial['nombre']}")
    print(f"[DATOS CAPTURADOS] Ingresos Registrados: S/. {estado_inicial['datos_extraidos']['ingresos_mensuales']}")
    print(f"[DATOS CAPTURADOS] Score Externo: {estado_inicial['datos_extraidos']['score_externo']} pts.")
    
    # 3. Procesamiento síncrono del Grafo paso a paso
    print("\n--> Transmitiendo estados a los nodos de LangGraph...")
    for chunk in app_evaluacion.stream(estado_inicial, config_hilo):
        for nodo, datos in chunk.items():
            print(f"    [CHECKPOINT CAPTURADO] Nodo '{nodo}' procesado y congelado por MemorySaver.")
            
    # 4. Auditoría de resultados finales de la ruta 1
    estado_final = app_evaluacion.get_state(config_hilo)
    
    print("\n" + ">" * 40)
    print(" RESULTADOS FINALES DE LA RUTA ORIGINAL:")
    print(">" * 40)
    print(f"    Monto Procesado: S/. {estado_final.values['datos_extraidos']['ingresos_mensuales']}")
    print(f"    Riesgo Interno Asignado: {estado_final.values['score_riesgo']} puntos (Alto Penalizado)")
    print(f"    Dictamen del Sistema: {estado_final.values['decision']}")
    print("\n    Logs Históricos Consolidados:")
    for evt in estado_final.values['eventos']:
        print(f"      {evt}")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    ejecutar_ruta_original()