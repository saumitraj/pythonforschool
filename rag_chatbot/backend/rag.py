import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "PDFFiles")
CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

# Load models from environment variables, fallback to defaults
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
SEARCH_TYPE = os.getenv("SEARCH_TYPE", "similarity")


def load_documents(data_path=DATA_PATH):
    """Loads PDF documents and adds filename metadata."""
    print(f"Loading documents from {data_path}...")
    loader = DirectoryLoader(
        data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    documents = loader.load()
    # Ensure source metadata is just the filename for easy filtering
    for doc in documents:
        if "source" in doc.metadata:
            doc.metadata["source"] = os.path.basename(doc.metadata["source"])
            
    print(f"Loaded {len(documents)} page(s) from {data_path}")
    return documents

def split_documents(documents):
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=500,
        length_function=len,
        is_separator_regex=False,
    )
    all_splits = text_splitter.split_documents(documents)
    print(f"Split into {len(all_splits)} chunks")
    return all_splits

def get_embedding_function(model_name=EMBEDDING_MODEL):
    """Initializes the Ollama embedding function."""
    embeddings = OllamaEmbeddings(model=model_name)
    return embeddings

PARENT_STORE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "parent_store")

def get_parent_store():
    fs = LocalFileStore(PARENT_STORE_PATH)
    return create_kv_docstore(fs)

# Global store for parent documents
parent_store = get_parent_store()

def flush_db(persist_directory=CHROMA_PATH):
    """Deletes existing Chroma DB to allow a fresh index and clears query cache."""
    global rag_chain_instance, parent_store
    rag_chain_instance = None # clear chain so it releases the Chroma reference
    clear_cache() # Also clear the cache when flushing the DB
    
    if os.path.exists(persist_directory):
        print(f"Flushing existing database at {persist_directory}...")
        try:
            shutil.rmtree(persist_directory)
        except Exception as e:
            print(f"Error removing {persist_directory}: {e}")
            
    if os.path.exists(PARENT_STORE_PATH):
        print(f"Flushing existing parent store at {PARENT_STORE_PATH}...")
        try:
            shutil.rmtree(PARENT_STORE_PATH)
        except Exception as e:
            print(f"Error removing {PARENT_STORE_PATH}: {e}")
            
    parent_store = get_parent_store() # Reset the parent document store

def get_vector_store(embedding_function, persist_directory=CHROMA_PATH):
    """Initializes or loads the Chroma vector store."""
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    return vectorstore

def index_all_documents():
    """Flushes DB, creates a ParentDocumentRetriever, and indexes documents."""
    flush_db()
    docs = load_documents()
    if not docs:
        print("No documents found to index.")
        return 0
        
    embedding_function = get_embedding_function()
    vector_store = get_vector_store(embedding_function)
    
    # Create the splitters for Parent (large) and Child (small) chunks
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    
    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        docstore=parent_store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )
    
    print(f"Indexing {len(docs)} full pages into ParentDocumentRetriever...")
    retriever.add_documents(docs)
    print("Indexing complete.")
    return len(docs)

# Simple in-memory cache for queries
query_cache = {}

def get_cached_response(question: str):
    """Returns the cached response if it exists."""
    return query_cache.get(question.strip().lower())

def set_cached_response(question: str, response: str):
    """Saves a response to the cache."""
    query_cache[question.strip().lower()] = response
    
def clear_cache():
    """Clears the in-memory query cache."""
    query_cache.clear()

def create_rag_chain(source_file=None):
    """Builds and returns the conversational RAG chain with optional metadata filtering."""
    embedding_function = get_embedding_function()
    vector_store = get_vector_store(embedding_function)
    
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0, 
        num_ctx=8192 
    )
    
    search_kwargs = {'k': 5}
    if SEARCH_TYPE == "mmr":
        search_kwargs['fetch_k'] = 20
        
    # We use ParentDocumentRetriever instead of standard retriever
    # The child chunks are searched, but the parent document is returned
    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        docstore=parent_store,
        child_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100),
        search_type=SEARCH_TYPE,
        search_kwargs=search_kwargs
    )
    
    # Apply metadata filtering if a source_file is specified
    if source_file and source_file != "All Files":
        retriever.search_kwargs['filter'] = {"source": source_file}
        print(f"Applying metadata filter: source == {source_file}")

    
    template = """You are an expert legal document assistant. Use the following pieces of context to answer the question at the end.
If the answer is not contained in the context, say "I cannot answer this based on the provided context." Do not make up an answer.
Pay close attention to exact names, titles, and legal roles (e.g., Appellant, Respondent, Plaintiff, Defendant) mentioned in the text.

Context:
{context}

Question: {question}

Helpful Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# Global chain instance to be reused by the backend
rag_chain_instance = None
current_filter = None

def get_chain(source_file=None):
    global rag_chain_instance, current_filter
    # If the filter changed, we need to rebuild the chain
    if rag_chain_instance is None or current_filter != source_file:
        rag_chain_instance = create_rag_chain(source_file)
        current_filter = source_file
    return rag_chain_instance
