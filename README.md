# legal-assist
#  Legal Contract Analyzer (RAG + FAISS)

## Descripción

Este proyecto implementa un sistema de Retrieval-Augmented Generation (RAG) para analizar contratos legales y compararlos con políticas internas de la empresa.

El sistema es capaz de:

 Procesar documentos PDF/DOCX
 Dividirlos en chunks semánticos
 Generar embeddings
 Realizar búsqueda semántica con FAISS
 Detectar riesgos contractuales
 Generar un informe estructurado
 Crear un borrador de email para el equipo legal



## Tecnologías utilizadas

Python 3.11
LangChain
OpenAI (embeddings + LLM)
FAISS (vector store)
PyPDF / Docx2txt



## Arquitectura

Documentos → Loaders → Chunking → Embeddings → FAISS → Retriever → LLM → Respuesta

## Estructura del proyecto

legal-assist/
│
├── app/
│   ├── config.py
│   ├── loaders.py
│   ├── splitter.py
│   └── vectorstore.py
│
├── data/
│   ├── contracts/
│   └── policies/
│
├── db/
│   └── faiss_index/
│
├── ingest.py
├── ask.py
├── analyze.py
├── requirements.txt
└── .env

## Instalación

### 1. Crear entorno virtual (Python 3.11 recomendado)

### 2. Instalar dependencias

### 3. Configurar variables

##  Uso

### 1. Indexar documentos
python ingest.py

### 2. Hacer preguntas
python ask.py

### 3. Analizar contrato

python analyze.py

## Ejemplo de uso

Pregunta:

¿Hay riesgos en el contrato respecto a la política interna?

Salida:

Lista de riesgos
Severidad (alta/media/baja)
Explicación
Recomendación
Email generado automáticamente



## Dificultades encontradas

Durante el desarrollo se encontraron problemas reales de compatibilidad:

###  Python 3.14

Algunas librerías (LangChain, Pydantic, Chroma) no son totalmente compatibles

Solución:
usar Python 3.11 para mayor estabilidad

### ChromaDB
Inicialmente se utilizó Chroma como vector store, pero se encontraron problemas:
errores de instalación en Windows
conflictos con SQLite
fallos en tiempo de ejecución
crashes inesperados
Solución:
reemplazar Chroma por FAISS
FAISS resultó más estable y fácil de usar en entorno local

