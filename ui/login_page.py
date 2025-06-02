import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io

class LoginPage():

    def __init__(self, app):

        self.app = app

    def render(self):

        self.app.clear()
        
        
        container = ctk.CTkFrame(self.app, width=400, height=300, corner_radius=15)
        container.place(relx=0.5, rely=0.5, anchor="center")


        title = ctk.CTkLabel(container, text="Welcome Back", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(30, 15))

        # Username Block Design
        username_label = ctk.CTkLabel(container, text="Username", font=ctk.CTkFont(size=14))
        username_label.pack(anchor="w", padx=40, pady=(10, 5))
        username_entry = ctk.CTkEntry(container, width=320, height=35, placeholder_text="Enter your username")
        username_entry.pack(padx=40)

        # Username Block Design
        password_label = ctk.CTkLabel(container, text="Password", font=ctk.CTkFont(size=14))
        password_label.pack(anchor="w", padx=40, pady=(20, 5))
        password_entry = ctk.CTkEntry(container, width=320, height=35, placeholder_text="Enter your password", show="*")
        password_entry.pack(padx=40)

        
        def register():
            
            if self.app.session.query(User).filter_by(username = username_entry.get()).first():

                messagebox.showerror("Error","User already exists.")

            with open("no_user.png","rb") as img:

                default_pic = img.read()

            user = User(username = username_entry.get(),password = password_entry.get(),profile_pic = default_pic)
            self.app.session.add(user)
            self.app.session.commit()
            messagebox.showinfo("Succesful","User Succesfully Created")
            self.render()



        def login():
            
            from ui.home_page import HomePage
            user = self.app.session.query(User).filter_by(username = username_entry.get(),password = password_entry.get()).first()

            if user:
                self.app.user = user
                HomePage(self.app).render()

            else:
                
                messagebox.showerror("AA","Yok")


        login_btn = ctk.CTkButton(container, text="Login", width=320, height=40, command= login ,fg_color="#EB6304",hover_color= "black")
        login_btn.pack(pady=10)

        register_btn = ctk.CTkButton(container,text = "Register", width = 320,height= 40,command = register,fg_color="#EB6304",hover_color= "black")
        register_btn.pack(pady= 10)
