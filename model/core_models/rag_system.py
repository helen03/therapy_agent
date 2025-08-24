"""
RAG (Retrieval-Augmented Generation) System for Psychology Documents
Provides document upload, vector storage, and retrieval capabilities
"""

import os
import logging
import json
import tempfile
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process and extract text from various document formats"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.md']
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """Extract text from supported document formats"""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                return self._extract_from_pdf(file_path)
            elif ext == '.docx':
                return self._extract_from_docx(file_path)
            elif ext in ['.txt', '.md']:
                return self._extract_from_text(file_path)
            else:
                logger.error(f"Unsupported file format: {ext}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return None
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF files"""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX files"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_from_text(self, file_path: str) -> str:
        """Extract text from plain text files"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

class VectorStore:
    """Simple vector store for document chunks using TF-IDF"""
    
    def __init__(self):
        self.documents = []
        self.metadata = []
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.vectors = None
    
    def add_document(self, text: str, metadata: Dict) -> None:
        """Add document to vector store"""
        # Split into chunks (sentences or paragraphs)
        chunks = self._chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_id'] = f"{metadata['doc_id']}_chunk_{i}"
                chunk_metadata['chunk_index'] = i
                
                self.documents.append(chunk)
                self.metadata.append(chunk_metadata)
    
    def _chunk_text(self, text: str, chunk_size: int = 200) -> List[str]:
        """Split text into meaningful chunks"""
        # Simple sentence-based chunking
        sentences = text.split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def build_index(self) -> None:
        """Build TF-IDF index"""
        if self.documents:
            self.vectors = self.vectorizer.fit_transform(self.documents)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant document chunks"""
        if not self.documents or self.vectors is None:
            return []
        
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.vectors).flatten()
        
        # Get top-k results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'text': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'similarity': float(similarities[idx])
                })
        
        return results

class RAGSystem:
    """Main RAG system for psychology document retrieval"""
    
    def __init__(self):
        self.processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.documents = {}
        self.is_index_built = False
    
    def upload_document(self, file_path: str, user_id: str, title: str = None) -> Optional[str]:
        """Upload and process a psychology document"""
        try:
            text = self.processor.extract_text(file_path)
            if not text:
                return None
            
            doc_id = f"doc_{user_id}_{datetime.now().timestamp()}"
            metadata = {
                'doc_id': doc_id,
                'user_id': user_id,
                'title': title or os.path.basename(file_path),
                'upload_date': datetime.now().isoformat(),
                'file_path': file_path
            }
            
            self.vector_store.add_document(text, metadata)
            self.documents[doc_id] = metadata
            self.is_index_built = False
            
            logger.info(f"Document uploaded: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to upload document: {e}")
            return None
    
    def build_index(self) -> None:
        """Build search index"""
        self.vector_store.build_index()
        self.is_index_built = True
        logger.info("RAG index built successfully")
    
    def retrieve_relevant_content(self, query: str, user_id: str = None, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant content from psychology documents"""
        if not self.is_index_built:
            self.build_index()
        
        results = self.vector_store.search(query, top_k=top_k)
        
        # Filter by user if specified
        if user_id:
            results = [r for r in results if r['metadata'].get('user_id') == user_id]
        
        return results
    
    def enhance_prompt_with_context(self, user_prompt: str, user_id: str = None) -> str:
        """Enhance user prompt with relevant document context"""
        relevant_content = self.retrieve_relevant_content(user_prompt, user_id)
        
        if not relevant_content:
            return user_prompt
        
        context_parts = []
        for i, result in enumerate(relevant_content[:2]):  # Use top 2 results
            context_parts.append(f"Relevant psychology knowledge [{i+1}]: {result['text']}")
        
        context_text = "\n\n".join(context_parts)
        enhanced_prompt = f"""Based on the following psychology knowledge:

{context_text}

Please respond to the user's query: {user_prompt}

Remember to be empathetic, supportive, and therapeutic in your response."""
        
        return enhanced_prompt
    
    def get_user_documents(self, user_id: str) -> List[Dict]:
        """Get all documents uploaded by a user"""
        return [doc for doc in self.documents.values() if doc.get('user_id') == user_id]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            # Rebuild index to remove document chunks
            self.build_index()
            return True
        return False

# Global RAG instance
rag_system = RAGSystem()