"""
Test CustomTkinter setup
"""

import customtkinter as ctk

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")  # or "green", "dark-blue"

class TestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Quill - Test Window")
        self.geometry("400x300")
        
        # Create test widgets
        self.label = ctk.CTkLabel(self, text="🪶 Quill is working!", font=ctk.CTkFont(size=20))
        self.label.pack(pady=20)
        
        self.button = ctk.CTkButton(self, text="Click me!", command=self.button_click)
        self.button.pack(pady=10)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Type something...")
        self.entry.pack(pady=10)
        
    def button_click(self):
        text = self.entry.get()
        self.label.configure(text=f"You typed: {text}")

if __name__ == "__main__":
    app = TestApp()
    app.mainloop()