from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from core.vector_store import get_vector_store, load_vector_store, get_retriever

from dotenv import load_dotenv

load_dotenv()


def get_model():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(transcript: str):
    vector_store = get_vector_store(transcript)
    retriever = get_retriever(vector_store, k=4)
    llm = get_model()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting assistant. Answer the user's question
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}"""
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context": (
                RunnableLambda(lambda x: x["question"])
                | retriever
                | RunnableLambda(format_docs)
            ),
            "question": RunnableLambda(lambda x: x["question"])
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store, k=4)
    llm = get_model()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting assistant. Answer the user's question
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}"""
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context": (
                RunnableLambda(lambda x: x["question"])
                | retriever
                | RunnableLambda(format_docs)
            ),
            "question": RunnableLambda(lambda x: x["question"])
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question: str):
    answer = rag_chain.invoke({
        "question": question
    })

    return answer