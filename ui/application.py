import customtkinter as ctk
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io
from models import Session
from ui.login_page import LoginPage


class App(ctk.CTk):


    def __init__(self):
        super().__init__()
        self.title = "Reddit"
        #Windowed Fullscreen
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.resizable(False, False)

        self.session = Session()
        self.user = None
        self.geometry(f"{self.width}x{self.height}")
        LoginPage(self).render()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()