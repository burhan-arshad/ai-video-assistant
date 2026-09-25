import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
CHROMA_DIR="chroma_db"
COLLECTION_NAME="meeting_transcripts"
EMBEDDING_MODEL="all-MiniLM-L6-v2"

def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"device": "cpu"})

def get_vector_store(transcripts:str):
    embeddings=get_embeddings_model()
    splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks=splitter.split_text(transcripts)
    docs=[Document(page_content=chunk, metadata={'chunk_index': i}) for i, chunk in enumerate(chunks)]
    vector_store=Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=CHROMA_DIR, collection_name=COLLECTION_NAME)
    return vector_store

def load_vector_store():
    embeddings=get_embeddings_model()
    vector_store=Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings, collection_name=COLLECTION_NAME)
    return vector_store

def get_retriever(vector_store:Chroma , k:int =4):
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})