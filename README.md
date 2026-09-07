<div align="center">

# 📜 SkimTerms.ai

### *Understand Legal Contracts & Privacy Policies in Seconds*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/AI_Engine-Ollama_--_phi3-black?logo=ollama&logoColor=white)](https://ollama.ai/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Developer](https://img.shields.io/badge/Developed%20By-Krishanth%20G-005BFF?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/krishanth-g)

<p align="center">
  <b>100% Offline, Privacy-First RAG Engine for Plain-English Legal Simplification</b>
</p>

---

</div>

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Screenshots & Demo Video](#-screenshots--demo-video)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Quick Start Guide](#-quick-start-guide)
- [Environment Variables](#-environment-variables)
- [Usage Examples](#-usage-examples)
- [Contributing & PR Template](#-contributing--pr-template)
- [Changelog](#-changelog)
- [License](#-license)
- [Author & Acknowledgments](#-author--acknowledgments)

---

## 🌟 Overview

**SkimTerms.ai** is an offline-first, API-free Retrieval-Augmented Generation (RAG) legal assistant. It empowers consumers and developers to instantly parse, simplify, and chat with legal agreements, Terms of Service (ToS), and Privacy Policies **without sending sensitive data to third-party cloud servers**.

Powered by local LLMs via **Ollama** (`phi3`) and **FAISS** vector embeddings, SkimTerms.ai transforms dense legalese into actionable insights, risk highlights, and plain-English summaries right on your local machine.

---

## ✨ Key Features

- 🔒 **100% Local & Privacy-Guaranteed**: Document text, vector embeddings, and LLM inferences remain strictly on localhost. No API keys required.
- 📄 **PDF & Raw Text Parsing**: In-memory PDF text extraction (`pypdf`) and direct text paste support.
- ⚡ **Ultra-Fast Vector Search**: Sentence-Transformer embeddings (`all-MiniLM-L6-v2`) with in-memory FAISS indexing.
- 💬 **Interactive AI Chat & Streaming**: Real-time response streaming for answering questions about clauses, user data rights, cancellation terms, and liabilities.
- 🎨 **Modern Responsive UI**: Clean glassmorphism layout, light/dark mode support, preset sample policy loader, and visual risk indicators.

---

## 📸 Screenshots & Demo Video

### 🖼️ Screenshots

| 1. Landing Page | 2. Upload Document | 3. AI Chat Dashboard |
| :---: | :---: | :---: |
| ![Landing Page](Docs/Image%201.png) | ![Upload Interface](Docs/Image%202.png) | ![AI Dashboard](Docs/Image%203.png) |

### 🎬 Demo Video

<video src="https://raw.githubusercontent.com/krishanthg/SkimTerms.ai/main/Docs/New%20Demo.mp4" controls="controls" muted="muted" style="max-width: 100%;">
</video>

> 💡 **For native inline video player rendering on GitHub web interface:**
> Drag and drop `Docs/New Demo.mp4` directly into the README editor on GitHub to generate a native `https://github.com/user-attachments/assets/...` video player link.
https://github.com/KrishanthG/SkimTerms.ai/blob/main/Docs/New%20Demo.mp4
Alternatively, view or download the demo file directly:
🎥 **[Watch / Download Demo Video (Docs/New Demo.mp4)](Docs/New%20Demo.mp4)**

## 🛠 Architecture & Tech Stack

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser Frontend                     │
│  (HTML5 / Vanilla JS / Tailwind CSS / Material Symbols) │
└────────────────────────────┬────────────────────────────┘
                             │ REST & Streaming API
┌────────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                      │
│             (Python 3.10+ / Async Endpoints)            │
└──────────────┬───────────────────────────┬──────────────┘
               │                           │
               ▼                           ▼
  ┌─────────────────────────┐  ┌─────────────────────────┐
  │  LangChain + FAISS Store│  │ Local Ollama (`phi3`)   │
  │ (all-MiniLM-L6-v2 Embed)│  │ (LLM Generation Engine) │
  └─────────────────────────┘  └─────────────────────────┘
```

### Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, Vanilla JavaScript, Tailwind CSS (CDN), Material Symbols, Inter Font |
| **Backend Framework** | Python 3.10+, FastAPI, Uvicorn |
| **RAG & AI** | LangChain, `langchain-ollama`, FAISS (`faiss-cpu`), HuggingFace Embeddings (`all-MiniLM-L6-v2`) |
| **Parsing & Storage** | PyPDF (`pypdf`), In-memory BytesIO streams |
| **Local LLM Server** | Ollama running `phi3` (or `llama3`) |

---

## 🚀 Quick Start Guide

Follow these simple steps to run **SkimTerms.ai** on your computer:

1. **Install Ollama**: Download and install [Ollama](https://ollama.ai/).
2. **Run local LLM model**:
   ```bash
   ollama run phi3
   ```
3. **Open Command Prompt (CMD)** in the project root folder.
4. **Navigate to Backend** and start the server:
   ```bash
   cd Backend
   uvicorn app:app --reload
   ```
5. **Open the HTML files** (e.g. `Frontend/index.html` or `Frontend/upload.html`) in your web browser and start testing!

---

## ⚙️ Environment Variables

Create a `.env` file in the `Backend` directory if customizing default ports or model names (see [.env.example](.env.example)):

```env
HOST=127.0.0.1
PORT=8000
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## 💡 Usage Examples

### 1. Uploading a PDF Document via API

```bash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/sample_policy.pdf"
```

**Response:**
```json
{
  "status": "success",
  "message": "Document processed and indexed locally with FAISS!",
  "filename": "sample_policy.pdf"
}
```

### 2. Asking Questions via Streaming API

```bash
curl -X POST "http://127.0.0.1:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Can I cancel my subscription at any time?"}'
```

---

## 🤝 Contributing & PR Template

Contributions are welcome! We provide pre-configured GitHub templates for issues and pull requests:

- 📋 **Contributing Guidelines**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 **Bug Report Template**: [.github/ISSUE_TEMPLATE/bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)
- ✨ **Feature Request Template**: [.github/ISSUE_TEMPLATE/feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)
- 🔀 **Pull Request Template**: [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 👨‍💻 Author & Acknowledgments

**Developed by Krishanth G**
- 💼 **LinkedIn**: [krishanth-g](https://www.linkedin.com/in/krishanth-g)
- 🌐 **Project Repository**: [SkimTerms.ai](https://github.com/krishanthg/SkimTerms.ai)

---

<div align="center">
  <sub>Built with ❤️ for privacy, transparency, and consumer protection.</sub>
</div>
