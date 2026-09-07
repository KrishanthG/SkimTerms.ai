import os
import io
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pypdf import PdfReader
from pydantic import BaseModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


app = FastAPI(title="SkimTerms.ai API", description="Offline-first, API-free RAG Legal Assistant with Ollama")

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for RAG storage and active document name
vector_store = None
current_document_name = "Terms of Service & Privacy Policy"

# Global embeddings model cached lazily
embeddings_model = None

def get_embeddings():
    global embeddings_model
    if embeddings_model is None:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception:
            embeddings_model = None
    return embeddings_model

# Default sample context to pre-initialize vector_store so queries work out-of-the-box
DEFAULT_LEGAL_TEXT = """
SkimTerms.ai Standard Sample Terms of Service and Privacy Policy:
1. User Data Rights: All document parsing, text extraction, and vector embedding operations are executed 100% locally on your device. No user content or document text is sent to third-party cloud servers.
2. Subscription & Cancellation: Users may cancel standard subscriptions at any time without penalty or auto-renewal lock-in.
3. Liability & Dispute Resolution: Disputes are subject to local jurisdiction and arbitration guidelines. SkimTerms.ai provides plain-English summaries for consumer reference and does not constitute formal legal representation.
"""

# Initialize Local Ollama LLM (Optimized for ultra-fast generation & streaming)
try:
    local_llm = ChatOllama(model="phi3", temperature=0.1, num_predict=128, num_thread=6)
except Exception as e:
    local_llm = None

def init_default_vector_store():
    global vector_store
    try:
        emb = get_embeddings()
        if emb:
            from langchain_community.vectorstores import FAISS
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_text(DEFAULT_LEGAL_TEXT)
            vector_store = FAISS.from_texts(chunks, emb)
    except Exception as e:
        print("Default vector store initialization warning:", e)


class TextUploadPayload(BaseModel):
    text: str
    filename: str

@app.get("/")
def home():
    return {"message": "SkimTerms.ai Local Ollama RAG Backend is Running Successfully!"}

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    global vector_store, current_document_name, embeddings_model
    try:
        current_document_name = file.filename
        content = await file.read()
        
        # Read PDF text in-memory using BytesIO (prevents file watcher auto-reloads)
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        # Chunking text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(text)
        
        # Use cached global embeddings model
        vector_store = FAISS.from_texts(chunks, embeddings_model)
        
        return {
            "status": "success", 
            "message": "Document processed and indexed locally with FAISS!",
            "filename": current_document_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-text/")
async def upload_text_document(payload: TextUploadPayload):
    global vector_store, current_document_name, embeddings_model
    try:
        current_document_name = payload.filename
        text = payload.text
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Provided text content is empty.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(text)
        
        vector_store = FAISS.from_texts(chunks, embeddings_model)
        
        return {
            "status": "success",
            "message": "Pasted text indexed locally with FAISS!",
            "filename": current_document_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/")
async def ask_question(query: dict):
    global vector_store, local_llm
    if not vector_store:
        init_default_vector_store()
    
    if not vector_store:
        raise HTTPException(status_code=400, detail="Please upload or analyze a document first.")
    
    question = query.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")
    
    # Fast similarity search (k=2 chunks for speed)
    docs = vector_store.similarity_search(question, k=2)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    if local_llm:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are SkimTerms.ai, an expert consumer legal assistant. Answer concisely in 2-3 bullet points based strictly on context. Be brief and direct."),
            ("human", "Context:\n{context}\n\nQuestion: {question}")
        ])
        prompt = prompt_template.format_messages(context=context, question=question)
        response = local_llm.invoke(prompt)
        answer_text = response.content
    else:
        answer_text = f"Local Ollama is offline. Context preview:\n{context[:300]}..."

    return {
        "question": question,
        "answer": answer_text,
        "citations": f"[{current_document_name}]"
    }

@app.post("/ask-stream/")
async def ask_question_stream(query: dict):
    global vector_store, local_llm
    if not vector_store:
        init_default_vector_store()
        
    question = query.get("question", "").strip()
    is_greeting = question.lower() in ["hi", "hello", "hey", "hi there", "hello there", "help"]

    if is_greeting:
        greeting_reply = f"Hello! 👋 I am SkimTerms.ai, your legal assistant for **{current_document_name}**. Ask me any specific question about data rights, cancellation policy, or legal risks in your document."
        async def greeting_generator():
            yield greeting_reply
        return StreamingResponse(greeting_generator(), media_type="text/plain")

    docs = vector_store.similarity_search(question, k=2) if vector_store else []
    context = "\n\n".join([doc.page_content for doc in docs]) if docs else DEFAULT_LEGAL_TEXT

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"You are an objective legal analyst summarizing the uploaded document titled '{current_document_name}'. Answer the user's question directly based strictly on the terms in the document context provided. Do not talk about SkimTerms.ai itself or refer to yourself as the service provider; state what the uploaded document or company policy specifies. Provide 2-3 concise bullet points."),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])
    prompt = prompt_template.format_messages(context=context, question=question)

    async def token_generator():
        if local_llm:
            try:
                for chunk in local_llm.stream(prompt):
                    yield chunk.content
            except Exception:
                yield f"Based on indexed context of **{current_document_name}**:\n\n• Document parsed and indexed locally.\n• Ask specific questions regarding cancellation, data rights, or legal risk."
        else:
            yield f"Hello! (Local Ollama LLM is currently offline). Indexed context for **{current_document_name}** is ready. Ask specific questions about clauses, data rights, or cancellation terms."

    return StreamingResponse(token_generator(), media_type="text/plain")

@app.get("/get-document-text/")
async def get_document_text():
    global vector_store, current_document_name
    if not vector_store:
        init_default_vector_store()
    
    docs = vector_store.similarity_search("terms privacy service policy cancellation liability data", k=5) if vector_store else []
    raw_text = "\n\n---\n\n".join([doc.page_content for doc in docs]) if docs else DEFAULT_LEGAL_TEXT
    
    return {
        "filename": current_document_name,
        "text": raw_text
    }