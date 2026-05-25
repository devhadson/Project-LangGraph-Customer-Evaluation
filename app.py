"""
MÓDULO: app.py
DESCRIPCIÓN: Definición del esquema de Estado, nodos de decisión y ensamble del Grafo con Checkpointer.
"""
from typing import TypedDict, List, Dict, Any, Literal
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. ESQUEMA DEL ESTADO CORPORATIVO (STATE SCHEMA)
class EvaluacionEstado(TypedDict):
    cliente_id: str
    nombre: str
    documento: str
    datos_extraidos: Dict[str, Any]
    resultado_listas: str
    score_riesgo: int
    decision: str
    eventos: List[str]

# 2. IMPLEMENTACIÓN DE NODOS LOGÍCOS
def recibir_datos(state: EvaluacionEstado) -> Dict[str, Any]:
    log = f"[{datetime.now().strftime('%H:%M:%S')}] Nodo 1: Datos cargados al flujo."
    return {"eventos": [log]}

def validar_documento(state: EvaluacionEstado) -> Dict[str, Any]:
    doc = state.get("documento", "")
    es_valido = len(doc) == 8 and doc.isdigit()
    log = f"[{datetime.now().strftime('%H:%M:%S')}] Nodo 2: Validación estructural de DNI concluida. Estado: {es_valido}."
    
    nuevos_datos = dict(state.get("datos_extraidos", {}))
    nuevos_datos["documento_valido"] = es_valido
    return {"datos_extraidos": nuevos_datos, "eventos": [log]}

def revisar_listas(state: EvaluacionEstado) -> Dict[str, Any]:
    alerta_previa = state.get("datos_extraidos", {}).get("alerta_antecedentes", False)
    resultado = "Alerta" if alerta_previa else "Limpio"
    log = f"[{datetime.now().strftime('%H:%M:%S')}] Nodo 3: Cruce con listas de cumplimiento finalizado ({resultado})."
    return {"resultado_listas": resultado, "eventos": [log]}

def calcular_riesgo(state: EvaluacionEstado) -> Dict[str, Any]:
    datos = state.get("datos_extraidos", {})
    ingresos = datos.get("ingresos_mensuales", 0)
    score_ext = datos.get("score_externo", 0)
    
    # Matriz de scoring algorítmico
    base_riesgo = 100
    if score_ext > 700: base_riesgo -= 40
    elif score_ext > 550: base_riesgo -= 20
        
    if ingresos > 10000: base_riesgo -= 30
    elif ingresos > 4000: base_riesgo -= 15
        
    if not datos.get("documento_valido", True): base_riesgo = 100
        
    score_final = max(0, min(100, base_riesgo))
    log = f"[{datetime.now().strftime('%H:%M:%S')}] Nodo 4: Score de Riesgo Interno calculado en: {score_final} pts."
    return {"score_riesgo": score_final, "eventos": [log]}

def decidir_aprobacion(state: EvaluacionEstado) -> Dict[str, Any]:
    listas = state.get("resultado_listas", "Limpio")
    riesgo = state.get("score_riesgo", 100)
    
    if listas == "Alerta" or riesgo >= 80:
        dictamen = "Rechazado"
    elif 40 <= riesgo < 80:
        dictamen = "Revisión Manual"
    else:
        dictamen = "Aprobado"
        
    log = f"[{datetime.now().strftime('%H:%M:%S')}] Nodo 5: Dictamen emitido por el motor: {dictamen}."
    return {"decision": dictamen, "eventos": [log]}

# 3. ENRUTADOR CONDICIONAL
def enrutar_tras_validacion(state: EvaluacionEstado) -> Literal["revisar_listas", "decidir_aprobacion"]:
    if not state.get("datos_extraidos", {}).get("documento_valido", True):
        return "decidir_aprobacion" # Bypass de optimización
    return "revisar_listas"

# 4. CONSTRUCCIÓN Y COMPILACIÓN DEL GRAFO CON PERSISTENCIA COMPARTIDA
builder = StateGraph(EvaluacionEstado)
builder.add_node("recibir_datos", recibir_datos)
builder.add_node("validar_documento", validar_documento)
builder.add_node("revisar_listas", revisar_listas)
builder.add_node("calcular_riesgo", calcular_riesgo)
builder.add_node("decidir_aprobacion", decidir_aprobacion)

builder.add_edge(START, "recibir_datos")
builder.add_edge("recibir_datos", "validar_documento")
builder.add_conditional_edges(
    "validar_documento",
    enrutar_tras_validacion,
    {"revisar_listas": "revisar_listas", "decidir_aprobacion": "decidir_aprobacion"}
)
builder.add_edge("revisar_listas", "calcular_riesgo")
builder.add_edge("calcular_riesgo", "decidir_aprobacion")
builder.add_edge("decidir_aprobacion", END)

# El checkpointer instanciado a nivel de módulo sobrevive en memoria durante la sesión de importación
memoria_compartida = MemorySaver()
app_evaluacion = builder.compile(checkpointer=memoria_compartida)