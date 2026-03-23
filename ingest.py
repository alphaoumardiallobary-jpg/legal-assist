from app.loaders import load_all_legal_documents
from app.splitter import split_documents
from app.vectorstore import create_vectorstore


def main():
    documents = load_all_legal_documents()

    if not documents:
        print("[ERROR] No se cargaron documentos.")
        return

    split_docs = split_documents(documents)
    create_vectorstore(split_docs)

    print("[OK] Ingesta completada correctamente.")


if __name__ == "__main__":
    main()