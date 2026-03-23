from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def clean_text(text: str) -> str:
    return " ".join(text.split())


def load_documents_from_folder(folder_path: str, document_type: str) -> List[Document]:
    folder = Path(folder_path)
    documents: List[Document] = []

    if not folder.exists():
        print(f"[WARN] La carpeta no existe: {folder}")
        return documents

    if not folder.is_dir():
        print(f"[ERROR] La ruta existe pero no es una carpeta: {folder}")
        return documents

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(f"[INFO] Archivo ignorado: {file_path.name}")
            continue

        try:
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
                loaded_docs = loader.load()
            else:
                loader = Docx2txtLoader(str(file_path))
                loaded_docs = loader.load()

            for i, doc in enumerate(loaded_docs):
                doc.page_content = clean_text(doc.page_content)
                doc.metadata["source"] = str(file_path)
                doc.metadata["filename"] = file_path.name
                doc.metadata["document_type"] = document_type
                doc.metadata["page_chunk_index"] = i

            documents.extend(loaded_docs)
            print(f"[OK] Cargado: {file_path.name} ({len(loaded_docs)} partes)")

        except Exception as e:
            print(f"[ERROR] No se pudo cargar {file_path.name}: {e}")

    return documents


def load_all_legal_documents() -> List[Document]:
    contracts = load_documents_from_folder("data/contracts", "contract")
    policies = load_documents_from_folder("data/policies", "policy")
    all_docs = contracts + policies

    print(f"[OK] Total documentos cargados: {len(all_docs)}")
    return all_docs