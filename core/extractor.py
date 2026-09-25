from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os
from dotenv import load_dotenv 
load_dotenv()

def get_model():
    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

def get_chain(system_prompt:str):
    llm=get_model()
    return (
        RunnablePassthrough()|
        RunnableLambda(lambda x: {"text": x})|
        ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{text}")
        ])|
        llm | StrOutputParser()
    )

def extract_action_items(transcript:str):
    chain=get_chain("You are an expert meeting analyst. From the meeting transcript, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Format as a numbered list. If none found say 'No action items found.'")
    return chain.invoke(transcript)

def extract_key_decisions(transcript: str) -> str:
    chain = get_chain(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'"
    )
    return chain.invoke(transcript)


def extract_questions(transcript: str) -> str:
    chain = get_chain(
        "From the meeting transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'"
    )
    return chain.invoke(transcript)