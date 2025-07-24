"""
Main window for Quill - Local AI Document Analyzer
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path

# Import our config
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import *

class QuillMainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("🪶 Quill - AI Document Analyzer")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(800, 600)
        
        # Set theme
        ctk.set_appearance_mode(THEME)
        ctk.set_default_color_theme("blue")
        
        # Initialize variables
        self.current_collection = "Work Documents"
        self.uploaded_documents = []
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Create main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.main_container, width=250)
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        self.sidebar.pack_propagate(False)
        
        # App title
        self.app_title = ctk.CTkLabel(
            self.sidebar, 
            text="🪶 Quill", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.app_title.pack(pady=(20, 30))
        
        # Collections section
        self.collections_label = ctk.CTkLabel(
            self.sidebar, 
            text="Document Collections", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.collections_label.pack(pady=(0, 10))
        
        # Collection buttons
        self.collection_buttons = []
        for collection in DEFAULT_COLLECTIONS:
            btn = ctk.CTkButton(
                self.sidebar,
                text=collection,
                command=lambda c=collection: self.select_collection(c),
                width=200,
                height=35
            )
            btn.pack(pady=5)
            self.collection_buttons.append(btn)
        
        # Upload button
        self.upload_btn = ctk.CTkButton(
            self.sidebar,
            text="📁 Upload Documents",
            command=self.upload_documents,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.upload_btn.pack(pady=(30, 10))
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Settings",
            command=self.open_settings,
            width=200,
            height=35
        )
        self.settings_btn.pack(pady=(0, 20))
        
    def create_main_content(self):
        # Main content frame
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.content_frame)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.collection_title = ctk.CTkLabel(
            self.header_frame,
            text=f"📚 {self.current_collection}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.collection_title.pack(side="left", padx=20, pady=15)
        
        # Document list area
        self.doc_list_frame = ctk.CTkScrollableFrame(self.content_frame, height=200)
        self.doc_list_frame.pack(fill="x", padx=20, pady=10)
        
        # Chat area
        self.chat_frame = ctk.CTkFrame(self.content_frame)
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Chat title
        self.chat_title = ctk.CTkLabel(
            self.chat_frame,
            text="💬 Ask questions about your documents",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.chat_title.pack(pady=(15, 10))
        
        # Chat display
        self.chat_display = ctk.CTkTextbox(self.chat_frame, height=300)
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Question input
        self.question_frame = ctk.CTkFrame(self.chat_frame)
        self.question_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.question_entry = ctk.CTkEntry(
            self.question_frame,
            placeholder_text="Type your question here...",
            font=ctk.CTkFont(size=14)
        )
        self.question_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        
        self.ask_button = ctk.CTkButton(
            self.question_frame,
            text="Ask",
            command=self.ask_question,
            width=80,
            height=35
        )
        self.ask_button.pack(side="right", padx=(0, 10), pady=10)
        
        # Bind Enter key to ask question
        self.question_entry.bind("<Return>", lambda e: self.ask_question())
        
    def select_collection(self, collection_name):
        self.current_collection = collection_name
        self.collection_title.configure(text=f"📚 {collection_name}")
        self.update_document_list()
        
    def upload_documents(self):
        filetypes = [
            ("All supported", "*.pdf *.txt *.docx"),
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt"), 
            ("Word documents", "*.docx"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select documents to upload",
            filetypes=filetypes
        )
        
        if files:
            for file_path in files:
                # Here we'll add document processing logic
                filename = os.path.basename(file_path)
                self.uploaded_documents.append({
                    'name': filename,
                    'path': file_path,
                    'collection': self.current_collection
                })
            
            self.update_document_list()
            messagebox.showinfo("Success", f"Uploaded {len(files)} document(s)")
    
    def update_document_list(self):
        # Clear existing document widgets
        for widget in self.doc_list_frame.winfo_children():
            widget.destroy()
        
        # Add document cards
        collection_docs = [doc for doc in self.uploaded_documents 
                          if doc['collection'] == self.current_collection]
        
        if not collection_docs:
            no_docs_label = ctk.CTkLabel(
                self.doc_list_frame,
                text="No documents in this collection. Click 'Upload Documents' to add some!",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_docs_label.pack(pady=20)
        else:
            for doc in collection_docs:
                doc_frame = ctk.CTkFrame(self.doc_list_frame)
                doc_frame.pack(fill="x", pady=5)
                
                doc_label = ctk.CTkLabel(
                    doc_frame,
                    text=f"📄 {doc['name']}",
                    font=ctk.CTkFont(size=12)
                )
                doc_label.pack(side="left", padx=10, pady=8)
    
    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            return
            
        # Add question to chat
        self.chat_display.insert("end", f"You: {question}\n\n")
        self.question_entry.delete(0, "end")
        
        # Here we'll add AI processing logic
        # For now, just show a placeholder response
        self.chat_display.insert("end", "Quill: I'm processing your question... (AI integration coming soon!)\n\n")
        self.chat_display.see("end")
    
    def open_settings(self):
        messagebox.showinfo("Settings", "Settings panel coming soon!")

if __name__ == "__main__":
    app = QuillMainWindow()
    app.mainloop()