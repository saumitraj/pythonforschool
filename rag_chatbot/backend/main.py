from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import backend.rag as rag_module

app = FastAPI(title="RAG Chatbot API", description="API for a Local RAG system using Ollama and ChromaDB")

class QueryRequest(BaseModel):
    question: str
    source_file: str = "All Files"

class QueryResponse(BaseModel):
    answer: str

class IndexResponse(BaseModel):
    message: str
    chunks_indexed: int

class CacheResponse(BaseModel):
    message: str

@app.get("/files")
def list_files():
    """Returns a list of PDF files available in the PDFFiles directory."""
    import os
    try:
        files = ["All Files"]
        if os.path.exists(rag_module.DATA_PATH):
            files.extend([f for f in os.listdir(rag_module.DATA_PATH) if f.endswith(".pdf")])
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index", response_model=IndexResponse)
def index_documents():
    """
    Flushes the existing Chroma vector store and re-indexes all PDF documents from the PDFFiles directory.
    """
    try:
        chunks_indexed = rag_module.index_all_documents()
        
        # Reset the global chain instance so it picks up the new vector store if needed
        rag_module.rag_chain_instance = None 
        
        return IndexResponse(
            message="Documents indexed successfully.", 
            chunks_indexed=chunks_indexed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@app.post("/chat", response_model=QueryResponse)
def chat_with_rag(request: QueryRequest):
    """
    Takes a question and returns answering using the RAG chain.
    """
    try:
        # Check cache first (incorporate source_file so cache doesn't mix files)
        cache_key = f"{request.source_file}:{request.question}"
        cached_answer = rag_module.get_cached_response(cache_key)
        if cached_answer:
            print(f"Cache hit for query: {cache_key}")
            return QueryResponse(answer=cached_answer)
            
        print(f"Cache miss. Querying LLM for: {request.question} (Filter: {request.source_file})")
        chain = rag_module.get_chain(request.source_file)
        # Querying the RAG chain
        answer = chain.invoke(request.question)
        
        # Save to cache
        rag_module.set_cached_response(cache_key, answer)
        
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    Accepts a PDF file and saves it to the PDFFiles directory.
    """
    import os
    import shutil
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
    os.makedirs(rag_module.DATA_PATH, exist_ok=True)
    file_path = os.path.join(rag_module.DATA_PATH, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": f"Successfully uploaded {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

@app.post("/flush-cache", response_model=CacheResponse)
def flush_cache():
    """
    Clears the in-memory query cache.
    """
    try:
        rag_module.clear_cache()
        return CacheResponse(message="Query cache cleared successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
