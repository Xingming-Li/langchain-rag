# Langchain RAG Application

Here holds an example project about building my own RAG system with OpenAI inspired by [Pixegami](https://github.com/pixegami/langchain-rag-tutorial/).

## Data Source

The main data are taken from [Firebolt Analytics](https://github.com/firebolt-db/rag_dataset/). They contain documentation in Markdown for Hugging Face Transformers. To learn more about the original data, see this [Hugging Face Dataset](https://huggingface.co/datasets/philschmid/markdown-documentation-transformers). In the `data` directory, all the Markdown files are put under the `hf_transformers_docs` folder. There is a `books` folder under the `data` repository as well, which only contains a book for validation (Alice's Adventures in Wonderland).

## Project Structure

    .
    ├── data/
    │   ├── hf_transformers_docs/
    │   └── books/
    ├── chroma_transformers/      # Persisted vector database (to be generated)
    ├── create_database.py        # Script to build the vector store
    ├── query_data.py             # Script to query the RAG system
    ├── compare_embeddings.py     # Script to compare word vectors
    ├── .env                      # Store your API key
    ├── requirements.txt
    └── README.md

## How It Works

This project implements a simple **Retrieval-Augmented Generation (RAG)** pipeline:

### 1. Data Ingestion & Chunking
- Markdown documents are loaded using `DirectoryLoader`
- Documents are split into chunks using `RecursiveCharacterTextSplitter`
  - chunk_size = 1000
  - chunk_overlap = 500

### 2. Embedding & Storage
- Each chunk is embedded using OpenAI's `text-embedding-3-small`
- Embeddings are stored in a Chroma vector database
- The database is persisted locally in `chroma_transformers`

### 3. Retrieval & Querying
- User query is embedded using the same embedding model
- Top-3 most relevant chunks are retrieved using similarity search
- A relevance threshold (score >= 0.3) is applied

### 4. Generation
- Retrieved context is injected into a prompt template
- The prompt is sent to the default OpenAI chat model (`ChatOpenAI()`)
- The model generates a grounded response based on retrieved context

## Setup Instructions

### 1. Clone the Repository

```
git clone <repo-url>
cd <repo-name>
```

### 2. Install Dependencies

Read the instructions in `requirements.txt` carefully before running the following command:

```
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Step 1: Create the Vector Database

```
python create_database.py
```

This will:
- Load documents
- Split them into chunks
- Generate embeddings
- Store them in `chroma_transformers`

### Step 2: Query the System

```
python query_data.py "Your question here"
```

Example:

```
python query_data.py "What is a transformer model?"
```

## Example Output

Answer the question based only on the following context:

`retrieved chunks`

Answer the question based on the above context: What is a transformer model?

Response: `generated answer`

Sources: ['data/hf_transformers_docs/xxx.md', 'data/hf_transformers_docs/yyy.md', ...]
