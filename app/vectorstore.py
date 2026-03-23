import os

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import EMBEDDING_MODEL, FAISS_DIR


def get_embedding_model():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


def create_vectorstore(documents):
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(documents, embeddings)

    os.makedirs(FAISS_DIR, exist_ok=True)
    vectorstore.save_local(FAISS_DIR)

    print(f"[OK] Índice FAISS guardado en: {FAISS_DIR}")
    return vectorstore


def load_vectorstore():
    embeddings = get_embedding_model()

    vectorstore = FAISS.load_local(
        FAISS_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print(f"[OK] Índice FAISS cargado desde: {FAISS_DIR}")
    return vectorstore