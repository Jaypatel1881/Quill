"""
Configuration file for Quill - Local AI Document Analyzer
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
SRC_DIR = PROJECT_ROOT / "src"

# Create directories if they don't exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# AI Model settings
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document processing settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_DOCUMENT_SIZE_MB = 5

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
THEME = "dark"  # or "light"

# Document collections
DEFAULT_COLLECTIONS = [
    "Work Documents",
    "Research Papers", 
    "Personal Files",
    "Study Materials"
]

# Supported file types
SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx"]

print("✅ Configuration loaded successfully!")
