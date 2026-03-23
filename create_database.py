import os
import shutil
from dotenv import load_dotenv
# from langchain.document_loaders import DirectoryLoader (legacy)
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings (legacy)
from langchain_openai import OpenAIEmbeddings
# import openai


# Load environment variables (assume that project contains .env file with API keys)
load_dotenv()

# Set OpenAI API key (unnecessary)
# openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma_transformers"
DATA_PATH = "data/hf_transformers_docs"

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Examine the 10th chunk
    document_f10 = chunks[10]
    print(document_f10.page_content)
    print(document_f10.metadata)
    # Examine the 10th chunk from the bottom
    document_l10 = chunks[-10]
    print(document_l10.page_content)
    print(document_l10.metadata)

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(model="text-embedding-3-small"), persist_directory=CHROMA_PATH
    )
    
    # Force to save DB (docs are automatically persisted actually)
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
