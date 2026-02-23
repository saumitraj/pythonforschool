import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

FASTAPI_URL = "http://localhost:8000"

st.title("Local RAG Chatbot 🤖")
st.write("This chatbot uses LLaMA 3.1 and ChromaDB to answer questions based on your local PDF files.")

# Sidebar for indexing
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF file to add to the RAG database", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Upload File"):
            with st.spinner("Uploading..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    res = requests.post(f"{FASTAPI_URL}/upload", files=files)
                    if res.status_code == 200:
                        st.success(f"Uploaded {uploaded_file.name} successfully! Please click 'Index Documents' below.")
                    else:
                        st.error(f"Error {res.status_code}: {res.text}")
                except Exception as e:
                    st.error(f"Failed to connect to FastAPI backend: {e}")
    st.divider()

    st.header("Document Filter")
    # Fetch available files
    available_files = ["All Files"]
    try:
        files_res = requests.get(f"{FASTAPI_URL}/files", timeout=2)
        if files_res.status_code == 200:
            available_files = files_res.json().get("files", ["All Files"])
    except:
        pass
        
    selected_file = st.selectbox("Chat with specific file:", available_files)
    st.divider()
    
    st.header("Document Indexing")
    st.write("Click below to flush the existing database and re-index all PDFs in the `PDFFiles/` folder.")
    if st.button("Index Documents"):
        with st.spinner("Indexing documents... This may take a while."):
            try:
                response = requests.post(f"{FASTAPI_URL}/index")
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Success! {data.get('message')} - Chunks Indexed: {data.get('chunks_indexed')}")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to FastAPI backend: {e}")

    st.divider()
    
    st.header("Query Cache")
    st.write("Responses are cached to speed up repeated questions. Click below to clear the cache.")
    if st.button("Clear Cache"):
        with st.spinner("Clearing cache..."):
            try:
                response = requests.post(f"{FASTAPI_URL}/flush-cache")
                if response.status_code == 200:
                    st.success("Query cache cleared!")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to FastAPI backend: {e}")
                
    st.divider()
    
    st.header("Chat History")
    st.write("Click below to clear the current chat messages from the screen.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question based on your documents"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{FASTAPI_URL}/chat",
                    json={"question": prompt, "source_file": selected_file}
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer received.")
                    message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    message_placeholder.error(error_msg)
            except Exception as e:
                message_placeholder.error(f"Failed to connect to backend: {e}")
