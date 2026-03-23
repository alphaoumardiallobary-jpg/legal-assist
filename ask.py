from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.config import CHAT_MODEL
from app.vectorstore import load_vectorstore


def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("filename", "desconocido")
        doc_type = doc.metadata.get("document_type", "unknown")
        content = doc.page_content
        formatted.append(
            f"[Documento {i}] Tipo: {doc_type} | Archivo: {source}\n{content}"
        )
    return "\n\n".join(formatted)


def main():
    question = input("Haz tu pregunta legal: ").strip()

    if not question:
        print("[ERROR] Debes escribir una pregunta.")
        return

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    retrieved_docs = retriever.invoke(question)
    context = format_docs(retrieved_docs)

    prompt = ChatPromptTemplate.from_template(
        """
Eres un asistente legal interno.

Tu tarea es responder preguntas sobre contratos y políticas internas usando solo el contexto proporcionado.

Reglas:
- No inventes información.
- Si no hay suficiente evidencia, dilo claramente.
- Señala riesgos contractuales cuando existan.
- Diferencia entre lo que viene del contrato y lo que viene de la política.
- Responde de forma clara y profesional.

Pregunta:
{question}

Contexto:
{context}
"""
    )

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)

    chain = prompt | llm
    response = chain.invoke({
        "question": question,
        "context": context
    })

    print("\n" + "=" * 80)
    print("RESPUESTA:\n")
    print(response.content)
    print("=" * 80)

    print("\nFRAGMENTOS RECUPERADOS:\n")
    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"--- Fragmento {i} ---")
        print(f"Archivo: {doc.metadata.get('filename')}")
        print(f"Tipo: {doc.metadata.get('document_type')}")
        print(doc.page_content[:500])
        print()


if __name__ == "__main__":
    main()