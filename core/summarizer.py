from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os
from dotenv import load_dotenv
load_dotenv()

def get_model():
    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

def split_transcript(transcript:str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200)
    return splitter.split_text(transcript)

def summarize_transcript(transcript:str):
    llm=get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "Summarize the following transcript: {transcript}")
    ])
    chain= prompt_template|llm|StrOutputParser()
    chunks=split_transcript(transcript)
    summaries=[chain.invoke({"transcript": chunk}) for chunk in chunks]
    combined="\n\n".join(summaries)
    combined_prompt=ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "Combine the following summaries into a single coherent summary: {summaries}")
    ])
    combined_chain=(RunnablePassthrough()|RunnableLambda(lambda x: {"summaries": x})|combined_prompt|llm|StrOutputParser())
    final_summary=combined_chain.invoke(combined)
    return final_summary

def generate_title(transcript:str):
    llm=get_model()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "Generate a title for the following transcript (Max 8 words): {transcript}")
    ])
    chain= (RunnablePassthrough()|RunnableLambda(lambda x: {"transcript": x})|prompt_template|llm|StrOutputParser())
    title=chain.invoke({"transcript": transcript[:2000]})
    return title
