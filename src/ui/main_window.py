import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from pathlib import Path
import sys
import json
import uuid

# Import our config
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import *

# Create folder to store uploaded documents
UPLOAD_BASE_PATH = Path(__file__).parent.parent.parent / "uploaded_docs"
UPLOAD_BASE_PATH.mkdir(exist_ok=True)
for collection in DEFAULT_COLLECTIONS:
    (UPLOAD_BASE_PATH / collection).mkdir(parents=True, exist_ok=True)

# File to store document metadata
METADATA_FILE = UPLOAD_BASE_PATH / "document_metadata.json"

class QuillMainWindow(TkinterDnD.Tk):
    def __init__(self):
        ctk.set_appearance_mode(THEME)
        ctk.set_default_color_theme("blue")

        super().__init__()

        self.title("🪶 Quill - AI Document Analyzer")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(800, 600)

        self.current_collection = "Work Documents"
        self.uploaded_documents = []

        self.load_existing_documents()
        self.create_widgets()

        # Enable drag & drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_files)

    def load_existing_documents(self):
        try:
            if METADATA_FILE.exists():
                with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                    saved_docs = json.load(f)
                for doc in saved_docs:
                    if Path(doc['path']).exists():
                        self.uploaded_documents.append(doc)
        except Exception as e:
            print(f"Error loading metadata: {e}")

        for collection in DEFAULT_COLLECTIONS:
            for file_path in (UPLOAD_BASE_PATH / collection).glob("*"):
                if file_path.is_file() and not any(doc['path'] == str(file_path) for doc in self.uploaded_documents):
                    self.uploaded_documents.append({
                        'id': str(uuid.uuid4()),
                        'name': file_path.name,
                        'path': str(file_path),
                        'collection': collection
                    })
        self.save_metadata()

    def save_metadata(self):
        try:
            with open(METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.uploaded_documents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving metadata: {e}")

    def create_widgets(self):
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.main_container, width=250)
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        self.sidebar.pack_propagate(False)

        self.app_title = ctk.CTkLabel(self.sidebar, text="🪶 Quill", font=ctk.CTkFont(size=24, weight="bold"))
        self.app_title.pack(pady=(20, 30))

        self.collections_label = ctk.CTkLabel(self.sidebar, text="Document Collections", font=ctk.CTkFont(size=16, weight="bold"))
        self.collections_label.pack(pady=(0, 10))

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

        self.upload_btn = ctk.CTkButton(
            self.sidebar,
            text="📁 Upload Documents",
            command=self.upload_documents,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.upload_btn.pack(pady=(30, 10))

        self.settings_btn = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Settings",
            command=self.open_settings,
            width=200,
            height=35
        )
        self.settings_btn.pack(pady=(0, 20))

    def create_main_content(self):
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.content_frame)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.collection_title = ctk.CTkLabel(self.header_frame, text=f"📚 {self.current_collection}", font=ctk.CTkFont(size=20, weight="bold"))
        self.collection_title.pack(side="left", padx=20, pady=15)

        self.doc_list_frame = ctk.CTkScrollableFrame(self.content_frame, height=200)
        self.doc_list_frame.pack(fill="x", padx=20, pady=10)

        self.chat_frame = ctk.CTkFrame(self.content_frame)
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.chat_title = ctk.CTkLabel(self.chat_frame, text="💬 Ask questions about your documents", font=ctk.CTkFont(size=16, weight="bold"))
        self.chat_title.pack(pady=(15, 10))

        self.chat_display = ctk.CTkTextbox(self.chat_frame, height=300)
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.question_frame = ctk.CTkFrame(self.chat_frame)
        self.question_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.question_entry = ctk.CTkEntry(self.question_frame, placeholder_text="Type your question here...", font=ctk.CTkFont(size=14))
        self.question_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)

        self.ask_button = ctk.CTkButton(self.question_frame, text="Ask", command=self.ask_question, width=80, height=35)
        self.ask_button.pack(side="right", padx=(0, 10), pady=10)
        self.question_entry.bind("<Return>", lambda e: self.ask_question())

        self.update_document_list()

    def drop_files(self, event):
        files = self.tk.splitlist(event.data)
        self.upload_documents(files)

    def select_collection(self, collection_name):
        self.current_collection = collection_name
        self.collection_title.configure(text=f"📚 {collection_name}")
        self.update_document_list()

    def get_icon(self, filename):
        ext = Path(filename).suffix.lower()
        if ext == ".pdf": return "📕"
        if ext == ".txt": return "📝"
        if ext == ".docx": return "📘"
        return "📄"

    def delete_document(self, doc):
        confirm = messagebox.askyesno("Delete Document", f"Are you sure you want to delete '{doc['name']}'?")
        if confirm:
            try:
                Path(doc['path']).unlink(missing_ok=True)
                self.uploaded_documents = [d for d in self.uploaded_documents if d['id'] != doc['id']]
                self.save_metadata()
                self.update_document_list()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file: {e}")

    def upload_documents(self, files=None):
        if files is None:
            files = filedialog.askopenfilenames(title="Select documents", filetypes=[("Supported", "*.pdf *.txt *.docx")])

        for file_path in files:
            filename = os.path.basename(file_path)
            ext = Path(filename).suffix.lower()
            if ext not in ['.pdf', '.txt', '.docx']:
                continue
            dest = UPLOAD_BASE_PATH / self.current_collection / filename
            if dest.exists():
                dest = self.get_unique_filename(dest)
            shutil.copy2(file_path, dest)
            self.uploaded_documents.append({
                'id': str(uuid.uuid4()),
                'name': dest.name,
                'path': str(dest),
                'collection': self.current_collection
            })
        self.save_metadata()
        self.update_document_list()

    def get_unique_filename(self, file_path):
        path = Path(file_path)
        counter = 1
        while path.exists():
            path = path.with_name(f"{path.stem} ({counter}){path.suffix}")
            counter += 1
        return path

    def update_document_list(self):
        for widget in self.doc_list_frame.winfo_children():
            widget.destroy()

        docs = sorted([
            doc for doc in self.uploaded_documents if doc['collection'] == self.current_collection
        ], key=lambda d: d['name'].lower())

        if not docs:
            ctk.CTkLabel(self.doc_list_frame, text="No documents in this collection.", text_color="gray").pack(pady=20)
            return

        for doc in docs:
            frame = ctk.CTkFrame(self.doc_list_frame)
            frame.pack(fill="x", pady=5)

            icon = self.get_icon(doc['name'])
            name_label = ctk.CTkLabel(frame, text=f"{icon} {doc['name']}", font=ctk.CTkFont(size=12))
            name_label.pack(side="left", padx=10, pady=8)

            delete_btn = ctk.CTkButton(frame, text="🗑️", width=30, command=lambda d=doc: self.delete_document(d))
            delete_btn.pack(side="right", padx=10)

    def ask_question(self):
        q = self.question_entry.get().strip()
        if q:
            self.chat_display.insert("end", f"You: {q}\n\n")
            self.chat_display.insert("end", "Quill: (AI processing coming soon!)\n\n")
            self.chat_display.see("end")
            self.question_entry.delete(0, "end")

    def open_settings(self):
        messagebox.showinfo("Settings", "Settings panel coming soon!")

if __name__ == "__main__":
    app = QuillMainWindow()
    app.mainloop()
