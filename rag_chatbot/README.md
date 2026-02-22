# RAG Chatbot Service

This project provides a local Retrieval-Augmented Generation (RAG) chatbot using FastAPI for the backend and Streamlit for the frontend interface. It uses Ollama (`llama3.1:8b` for language generation and `nomic-embed-text` for embeddings) with ChromaDB for vector storage.

## Prerequisites

*   **Python 3.9 or 3.10** is strictly required (newer versions may have compatibility issues with ChromaDB).
*   **Ollama**: You must install Ollama from [ollama.com](https://ollama.com) and ensure it is running in the background.

Once Ollama is installed, you **must pull the required models** before running the application:
```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

## Setup Instructions

1. **Clone or Checkout the Code**
   Navigate to the project directory where this `rag_chatbot` folder resides.
   ```bash
   cd pythonforschool/rag_chatbot
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

You can change the models used by the chatbot by editing the `.env` file located in the `rag_chatbot` folder:
```env
LLM_MODEL=llama3.1:8b
EMBEDDING_MODEL=nomic-embed-text
```
Whenever you change the embedding model, remember you must click **Index Documents** again to re-vectorize the PDFs with the new embeddings!

## Running the Application

You need to run both the FastAPI backend and the Streamlit frontend. It is recommended to use two separate terminal windows.

### 1. Start the FastAPI Backend
Ensure you are in the `rag_chatbot` directory and your virtual environment is active.
```bash
# Add the parent directory to PYTHONPATH so `rag_chatbot.backend.rag` can be imported
export PYTHONPATH=..
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
The API documentation will be available at `http://localhost:8000/docs`.

### 2. Start the Streamlit Frontend
In a new terminal window, activate the virtual environment and navigate to the `rag_chatbot` directory.
```bash
streamlit run frontend/app.py
```
This will open the chatbot UI in your default web browser (usually at `http://localhost:8501`).

## Usage
1. Open the Streamlit frontend.
2. If this is your first time, or if you've added new PDFs to the `pythonforschool/PDFFiles/` directory, click the **Index Documents** button in the sidebar. This will flush the existing ChromaDB and re-index all available documents.
3. Start asking questions in the chat interface!
