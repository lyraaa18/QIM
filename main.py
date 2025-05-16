import tkinter as tk
from tkinter import ttk
from pages.home import HomePage
from pages.create_invoice import CreateInvoicePage
from pages.verify_invoice import VerifyInvoicePage
from pages.history import HistoryPage
from pages.about import AboutPage
import sv_ttk

class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SealPay")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        self.colors = {
            "primary": "#4F46E5",      
            "primary_light": "#6366F1", 
            "secondary": "#10B981",     
            "accent": "#F59E0B",      
            "background": "#F9FAFB",   
            "text_light": "#FFFFFF",
            "text_dark": "#1F2937",
            "card_bg": "#FFFFFF",
            "hover": "#374151"       
        }

        sv_ttk.set_theme("light")
        self.style = ttk.Style()
        self.configure_modern_style()

        main_frame = tk.Frame(self, bg=self.colors["background"])
        main_frame.pack(fill="both", expand=True)
        
        self.create_modern_navbar(main_frame)
        
        container = ttk.Frame(main_frame, style="Card.TFrame")
        container.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.pages = {}
        self.current_page = None
        self.page_history = []
        
        for Page in (HomePage, CreateInvoicePage, VerifyInvoicePage, HistoryPage, AboutPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_page("HomePage")
    
    def configure_modern_style(self):
        self.style.configure("Card.TFrame", background=self.colors["card_bg"])
        self.style.configure("Nav.TFrame", background=self.colors["primary"])
        
        self.style.configure("Nav.TButton",
            foreground=self.colors["text_dark"],
            background=self.colors["primary"],
            font=('Segoe UI', 10),
            borderwidth=0,
            focuscolor=self.colors["primary"]
        )
        self.style.map("Nav.TButton",
            background=[("active", self.colors["hover"]), ("pressed", self.colors["hover"])],
            foreground=[("active", self.colors["primary"]), ("pressed", self.colors["text_light"])]
        )
        
        self.style.configure("Accent.TButton",
            foreground=self.colors["text_light"],
            background=self.colors["primary"],
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            focuscolor=self.colors["primary"]
        )
        self.style.map("Accent.TButton",
            background=[("active", self.colors["primary_light"]), ("pressed", self.colors["primary_light"])],
            foreground=[("active", self.colors["text_light"]), ("pressed", self.colors["text_light"])]
        )
        
        self.style.configure("Modern.TEntry",
            fieldbackground=self.colors["card_bg"],
            foreground=self.colors["text_dark"],
            insertcolor=self.colors["primary"],
            bordercolor=self.colors["primary_light"],
            lightcolor=self.colors["primary_light"],
            darkcolor=self.colors["primary_light"]
        )
    
    def create_modern_navbar(self, parent):
        self.nav_bar = ttk.Frame(parent, style="Nav.TFrame", height=60)
        self.nav_bar.pack(side="top", fill="x", pady=0, padx=0)
        self.nav_bar.pack_propagate(False)
        
        title_frame = ttk.Frame(self.nav_bar, style="Nav.TFrame")
        title_frame.pack(side="left", padx=20)
        
        logo_label = ttk.Label(
            title_frame,
            text="SealPay ",
            font=('Segoe UI', 14, 'bold'),
            foreground=self.colors["text_light"],
            background=self.colors["primary"]
        )
        logo_label.pack(side="left", padx=(0, 10))
        
        nav_buttons = [
            ("Home", "HomePage"),
            ("Create Invoice", "CreateInvoicePage"),
            ("Verify Invoice", "VerifyInvoicePage"),
            ("History", "HistoryPage"),
            ("About", "AboutPage")
        ]
        
        button_frame = ttk.Frame(self.nav_bar, style="Nav.TFrame")
        button_frame.pack(side="left", fill="x", expand=True)
        
        for text, page in nav_buttons:
            btn = ttk.Button(
                button_frame,
                text=text,
                command=lambda p=page: self.show_page(p),
                style="Nav.TButton"
            )
            btn.pack(side="left", padx=5)
    
    def show_page(self, page_name):
        if self.current_page and self.current_page != page_name:
            self.page_history.append(self.current_page)
        
        frame = self.pages[page_name]
        frame.tkraise()
        
        if hasattr(frame, 'on_show_frame'):
            frame.on_show_frame()
            
        self.current_page = page_name
        title = page_name.replace('Page', '')
        self.title(f"SealPay  - {title}")
        
        for widget in self.nav_bar.winfo_children():
            if isinstance(widget, ttk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, ttk.Button):
                        if page_name in str(btn.cget("command")):
                            btn.state(['active'])
                        else:
                            btn.state(['!active'])
    
    def show_previous_page(self):
        if self.page_history:
            previous_page = self.page_history.pop()
            self.show_page(previous_page)
        else:
            self.show_page("HomePage")

if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()