# ESTRUCTURA DEL PROYECTO

Recomiendo organizar los archivos en el mismo directorio de trabajo de la siguiente manera:

```text
├── data_engine.py          # Utilitario de datos sintéticos (Genera el CSV)
├── app.py                  # Definición del Estado, Nodos, Aristas y Compilación con Checkpointer
├── case_original_error.py  # CASO 1: Ejecución completa del flujo con error de digitación
└── case_time_travel_fork.py# CASO 2: Viaje en el tiempo, enmienda de datos y bifurcación (Fork)

```

## Manual Técnico de Ejecución paso a paso

Para ver en funcionamiento la demostración matemática de la trazabilidad y la inmutabilidad de los logs, sigue estos pasos desde tu terminal de comandos:


### 📂 1. Archivo de Dependencias (`requirements.txt`)

Crea un archivo llamado `requirements.txt` en la raíz de tu directorio de proyecto y pega el siguiente bloque de texto. Estas son las versiones estables recomendadas para garantizar la compatibilidad del Grafo de Estados y el manejo de datos:

```text
# Core de Orquestación de Agentes y Grafos de Estado
langgraph==0.0.60

# Estructuras de Datos y Generación del Motor Sintético
pandas==2.2.2

# Dependencia base obligatoria para la gestión de hilos y decoradores en LangGraph
typing-extensions>=4.10.0

```

---

### 🚀 2. Instrucciones para la Ejecución de los Casos de Prueba

Para ejecutar la solución de forma correcta, asegurar la persistencia en memoria del backend compartido y auditar el **Análisis de Trazabilidad Demostrativa**, sigue detalladamente esta guía paso a paso desde la terminal de tu sistema operativo.

#### Paso 2.1: Preparación del Entorno de Trabajo

Antes de correr los scripts, es una buena práctica aislar las librerías para evitar conflictos globales en tu máquina.

1. **Abrir la terminal** (o prompt de comandos) y navegar hasta la carpeta donde guardaste los 4 archivos (`data_engine.py`, `graph_architecture.py`, `case_original_error.py`, `case_time_travel_fork.py` y `requirements.txt`).
2. **Crear un entorno virtual de Python** (Opcional pero altamente recomendado):
```bash
python -m venv venv

```


3. **Activar el entorno virtual**:
* En Windows (Command Prompt): `venv\Scripts\activate`
* En Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
* En macOS/Linux: `source venv/bin/activate`


4. **Instalar las dependencias del proyecto**:
```bash
pip install -r requirements.txt

```



---

#### Paso 2.2: Inicialización del Motor de Datos Sintéticos

Este paso creará el archivo CSV local que simula la base de datos central del banco **"HT Perú"**.

* Ejecuta el comando:
```bash
python data_engine.py

```


* **Resultado esperado:** Verás en la consola el mensaje `[DATA ENGINE] Base de datos sintética creada exitosamente en: 'clientes_infraestructura.csv'`. Si revisas tu carpeta, habrá aparecido dicho archivo conteniendo el registro de Ana Gómez con el error original (`1200`).

---

#### Paso 2.3: Ejecución del Caso 1 (La Ruta Original con Error)

Simularemos el flujo de Onboarding inicial donde el analista comete el error material de digitación.

* Ejecuta el comando:
```bash
python case_original_error.py

```


* **Resultado y Auditoría en Consola:**
1. El sistema imprimirá los datos capturados mostrando: `Ingresos Registrados: S/. 1200`.
2. Verás el procesamiento secuencial de los nodos (`recibir_datos`, `validar_documento`, etc.) siendo congelados uno a uno por el `MemorySaver`.
3. En la sección de **Resultados Finales**, verificarás matemáticamente que el Score de Riesgo Interno fue penalizado con **60 puntos** (Riesgo Moderado-Alto) debido al bajo salario, concluyendo de manera estricta en un dictamen de: **🛑 Revisión Manual**.



---

#### Paso 2.4: Ejecución del Caso 2 (Time Travel - Viaje en el Tiempo y Forking)

Este es el core de la demostración. Correremos el script que inspecciona la historia del hilo anterior, congela el tiempo, inyecta la corrección a `S/. 12,000` y abre la bifurcación.

* Ejecuta el comando:
```bash
python case_time_travel_fork.py

```


*(Nota: Este script invoca automáticamente al Caso 1 al inicio para asegurar que la memoria tenga un historial fresco que leer).*
* **Resultado y Auditoría en Consola:**
1. Tras terminar la simulación del error, verás el tag `INICIANDO EJECUCIÓN DEL CASO 2`.
2. El sistema listará los checkpoints e informará que ha localizado con éxito el **`Checkpoint 2 (CP2)`** (el hito de restauración justo después de validar el documento).
3. Verás la alerta `Aplicando 'update_state' para consolidar la enmienda...`. Aquí es donde se inyectan los `S/. 12,000` reales.
4. El motor reanudará la ejecución con `.stream()` **pero notarás que no vuelve a pasar por el Nodo 1**, optimizando los recursos.
5. En la sección de **Resultados Finales de la Nueva Rama (Fork)**, verificarás que el Score de Riesgo bajó drásticamente a **30 puntos** y el dictamen mutó exitosamente a: **✅ Aprobado**.
6. **Prueba de Inmutabilidad:** En la Bitácora de Eventos consolidada del final del log, verás convivir el pasado original con el mensaje inyectado: `--- BIFURCACIÓN EJECUTADA --- Enmienda salarial inyectada por el operador. Ajuste a S/. 12,000.`, demostrando que el historial no se destruyó, cumpliendo con las normativas de auditoría de la SBS.

---

*Documentación elaborado por [Hadson Paredes](https://www.linkedin.com/in/hadson-paredes/) - 2026*
- Repositorio [Project-LangGraph-Customer-Evaluation](https://github.com/devhadson/Project-LangGraph-Customer-Evaluation)
- Disponible como recurso públicos en [Hadson.Tech](https://hadson.tech/public-resources/project-agentic-ai/project-langgraph-customer-evaluation)

<hr>
<h4 align="center"> Publicaciones en mis redes sociales y repositorio GitHub</h4>

<div align="center">
  <h3>Sígueme en mis redes sociales</h3>
  <a href="https://github.com/devhadson">
    <img src="https://img.shields.io/badge/GitHub-devhadson-black?logo=GitHub&style=flat-square" target="_blank" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/hadson-paredes/">
    <img src="https://img.shields.io/badge/LinkedIn-Hadson%20Paredes-blue?logo=linkedin&style=flat-square" target="_blank" alt="LinkedIn">
  </a>
  <a href="https://www.facebook.com/hadson.paredescordova/">
    <img src="https://img.shields.io/badge/Facebook-Hadson%20Paredes%20Cordova-Gree?logo=facebook&style=flat-square" target="_blank" alt="Facebook">
  </a>
  <a href="https://x.com/hadson_paredes">
    <img src="https://img.shields.io/badge/Hadson%20Paredes-black?logo=x&style=flat-square" target="_blank" alt="X">
  </a>
</div>