#-------------------->
#REQUIRED LIBRARIES
#-------------------->
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

#-------------------->
#DEFINE ALL THE VARIABLES
#-------------------->
CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

#-------------------->
#CREATE A MODEL FUNCTION
#-------------------->
import streamlit as st

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )
#-------------------->
'''
WRITE A FUNCTION TO 
BUILD A VECTOR STORE
'''
#-------------------->
def build_vector_store(transcript: str) -> Chroma:
    print("Building vector Store")

    # FIX: Ensure vector_db directory exists before Chroma tries to write to it
    os.makedirs(CHROMA_DIR, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(transcript)

    docs = [
        Document(page_content=chunk, metadata={'chunk_index': i})
        for i, chunk in enumerate(chunks)
    ]

    embeddings = get_embeddings()

    # FIX: Delete existing collection first to avoid stale data from previous runs
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )

    return vector_store

#-------------------->
'''
WRITE A FUNCTION TO 
LOAD A VECTOR STORE
'''
#-------------------->
def load_vector_store() -> Chroma:
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vector_store

#-------------------->
'''
WRITE A FUNCTION TO 
RETRIEVE DATA FROM
THE VECTOR STORE
'''
#-------------------->
def get_retriever(vector_store: Chroma, k: int = 4):
    return vector_store.as_retriever(
        search_type='similarity',
        search_kwargs={"k": k}
    )
