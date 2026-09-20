# CivicGuide AI - AI Public Service Knowledge Assistant

CivicGuide AI is an NLP + RAG based public-service assistant that helps users retrieve information from uploaded government/public-service PDF documents.
It supports PDF upload, text extraction, document chunking, metadata storage, semantic search, and citation-backed retrieval.

## Features

- Upload public-service or government scheme PDF documents
- Extract text from PDFs using `pdfplumber`
- Split extracted text into searchable chunks
- Store document metadata in PostgreSQL
- Store and search document chunks using ChromaDB
- Perform semantic search on uploaded documents
- Retrieve source-based information for user queries
- Backend APIs built using FastAPI

## Tech Stack

- **Backend:** FastAPI, Python
- **Database:** PostgreSQL
- **Vector Database:** ChromaDB
- **PDF Processing:** pdfplumber
- **Frontend:** HTML, CSS, JavaScript
- **AI/RAG:** NLP, RAG, Groq API
- **Tools:** Git, GitHub, Postman, VS Code
