import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io
from ui.home_page import HomePage



class NewPostScreen():

    def __init__(self,app):

        self.app = app

    def render(self):

        self.app.clear()
        
        back_button = ctk.CTkButton(self.app, text="← Back", width=80, height=30, command=lambda : HomePage(self.app).render(),fg_color="#EB6304",hover_color= "black")
        back_button.place(x=20, y=20)


        hdf_label = ctk.CTkLabel(self.app, text="How do you feel today?", font=ctk.CTkFont(size=30,weight="bold"))
        hdf_label.pack(pady = 200)

        container = ctk.CTkFrame(self.app, width=800, height=300, corner_radius=15)
        container.place(relx=0.5, rely=0.5, anchor="center")


        title_entry = ctk.CTkEntry(container, width=640, height=35, placeholder_text="Title...")
        title_entry.pack(padx=40,pady = 10)

        text_entry = ctk.CTkEntry(container, width=640, height=200, placeholder_text="Content...")
        text_entry.pack(padx=40)


        def add_post():

            post = Post(title = title_entry.get(),text = text_entry.get(),author = self.app.user)

            self.app.session.add(post)
            self.app.session.commit()
            messagebox.showinfo("Succesfull","Post created succesfully.")
            HomePage(self.app).render()

        add_post_btn = ctk.CTkButton(container,text="New Post",command=add_post,fg_color="#EB6304",hover_color= "black")
        add_post_btn.pack(padx = 10,pady= 10)