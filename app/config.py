import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
FAISS_DIR = os.getenv("FAISS_DIR", "./db/faiss_index")

if not OPENAI_API_KEY:
    raise ValueError("Falta OPENAI_API_KEY en el archivo .env")