import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.config import CHAT_MODEL
from app.vectorstore import load_vectorstore


def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


def extract_json(text: str) -> dict:
    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No se encontró un JSON válido en la respuesta.")

    json_text = text[start:end + 1]
    return json.loads(json_text)


def main():
    question = "Analiza los riesgos del contrato respecto a la política interna"

    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)
    context = format_docs(docs)

    prompt = ChatPromptTemplate.from_template(
        """
Eres un experto legal.

Analiza el contrato comparándolo con la política interna.

Responde SOLO con JSON válido.
No escribas texto antes ni después del JSON.

Usa EXACTAMENTE esta estructura:

{{
  "summary": "resumen breve",
  "risks": [
    {{
      "name": "nombre del riesgo",
      "severity": "alta",
      "description": "explicación clara"
    }}
  ],
  "recommendation": "recomendación clara",
  "email": "borrador profesional para el equipo legal"
}}

Reglas:
- Usa solo el contexto proporcionado.
- No inventes información.
- severity solo puede ser: "alta", "media" o "baja".
- Si no hay riesgos, devuelve una lista vacía en "risks".

CONTEXTO:
{context}
"""
    )

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    chain = prompt | llm

    response = chain.invoke({
        "context": context
    })

    result = extract_json(response.content)

    print("\nJSON RESULTADO:\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()