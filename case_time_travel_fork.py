"""
CASO DE PRUEBA 2: case_time_travel_fork.py
DESCRIPCIÓN: Recupera la historia del Thread del Caso 1, ejecuta el viaje en el tiempo,
             aplica una enmienda manual del estado y ejecuta el Forking hacia una ruta limpia.
"""
# Importamos la misma instancia de la app para conservar la persistencia en el backend
import case_original_error
from app import app_evaluacion

def ejecutar_time_travel_y_forking():
    # 1. Forzamos la ejecución previa de la ruta original para garantizar la existencia de la historia
    case_original_error.ejecutar_ruta_original()
    
    print("=" * 75)
    print(" INICIANDO EJECUCIÓN DEL CASO 2: TIME TRAVEL & FORKING (RAMA PARALELA)")
    print("=" * 75)
    
    # Usamos exactamente el mismo thread_id para auditar la historia de Ana Gomez
    config_hilo = {"configurable": {"thread_id": "TRANSACCION_ANA_GOMEZ"}}
    
    # 2. VIAJE EN EL TIEMPO: Recuperamos la historia cronológica de checkpoints del hilo
    historial_checkpoints = list(app_evaluacion.get_state_history(config_hilo))
    print(f"\n[AUDITORÍA] Checkpoints localizados en el clúster de memoria: {len(historial_checkpoints)}")
    
    checkpoint_objetivo = None
    # Localizamos el punto de restauración ideal: Estado listo para entrar a 'revisar_listas'
    for cp in historial_checkpoints:
        if cp.next and "revisar_listas" in cp.next:
            checkpoint_objetivo = cp
            break
            
    if not checkpoint_objetivo:
        print("[CRÍTICO] No se encontró un punto del tiempo válido para restaurar.")
        return
        
    print(f"\n[RESTORE] Punto de control seleccionado de forma exitosa:")
    print(f"    -> ID del Checkpoint Histórico: {checkpoint_objetivo.config['configurable']['checkpoint_id']}")
    print(f"    -> Nodos en cola de ejecución en este instante: {checkpoint_objetivo.next}")
    
    # 3. CONFIGURACIÓN DEL FORK: Clonamos los metadatos de direccionamiento temporal
    config_fork = checkpoint_objetivo.config
    valores_modificables = checkpoint_objetivo.values
    
    # 4. ENMIENDA DE DATOS (Mecanismo de Inyección)
    # Corregimos el valor de ingresos de S/. 1,200 al valor real auditado de S/. 12,000
    valores_modificables["datos_extraidos"]["ingresos_mensuales"] = 12000
    valores_modificables["eventos"].append(
        "--- BIFURCACIÓN EJECUTADA --- Enmienda salarial inyectada por el operador. Ajuste a S/. 12,000."
    )
    
    print("\n--> Aplicando 'update_state' para consolidar la enmienda en el Checkpoint...")
    app_evaluacion.update_state(
        config_fork,
        valores_modificables,
        as_node="validar_documento" # Informamos que sustituye las salidas de la validación de identidad
    )
    
    # 5. FORKING: Reanudamos el procesamiento de los nodos pendientes en una rama paralela limpia
    print("\n--> Reanudando procesamiento desde el punto intermedio (.stream alterno)...")
    for chunk in app_evaluacion.stream(None, config_fork):
        for nodo, datos in chunk.items():
            print(f"    [FORK-PROCESO] Nodo '{nodo}' calculado aisladamente sobre la nueva rama.")
            
    # 6. Evaluación de resultados finales de la bifurcación
    estado_final_fork = app_evaluacion.get_state(config_fork)
    
    print("\n" + ">" * 40)
    print(" RESULTADOS FINALES DE LA NUEVA RAMA (FORK):")
    print(">" * 40)
    print(f"    Cliente Evaluado: {estado_final_fork.values['nombre']}")
    print(f"    Monto Modificado Ejecutado: S/. {estado_final_fork.values['datos_extraidos']['ingresos_mensuales']}")
    print(f"    Nuevo Score de Riesgo Calculado: {estado_final_fork.values['score_riesgo']} puntos (Riesgo Bajo)")
    print(f"    Nueva Decisión Final del Grafo: {estado_final_fork.values['decision']}")
    
    print("\n    Trazabilidad de la Bitácora de Eventos de la Nueva Rama:")
    for evt in estado_final_fork.values['eventos']:
        print(f"      {evt}")
    print("=" * 75)

if __name__ == "__main__":
    ejecutar_time_travel_y_forking()