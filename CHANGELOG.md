# Changelog

All notable changes to **SkimTerms.ai** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-09-07

### Added
- **100% Offline RAG Engine**: Integrated LangChain and FAISS with local HuggingFace embeddings (`all-MiniLM-L6-v2`).
- **Local Ollama Integration**: ChatOllama integration with `phi3` model for fast streaming response generation.
- **FastAPI Endpoints**:
  - `GET /`: Health check endpoint.
  - `POST /upload/`: PDF document extraction and vector indexing.
  - `POST /upload-text/`: Raw text / Terms of Service payload indexing.
  - `POST /chat/`: Streaming chat endpoint for legal Q&A.
- **Modern Responsive Frontend**:
  - Glassmorphic UI design system built with Tailwind CSS.
  - Dark/Light mode theme switcher with system preference persistence.
  - Drag-and-drop PDF upload zone and sample legal policy presets (Spotify, GitHub, Cloud Storage).
  - Real-time interactive AI chat dashboard with clause inspection and risk indicators.
- **Developer Credit & Branding**: Embedded developer credit for Krishanth G ([LinkedIn](https://www.linkedin.com/in/krishanth-g)) across landing, upload, and dashboard footers.
