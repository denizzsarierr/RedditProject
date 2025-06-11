import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io
from ui.home_page import HomePage


class ProfileScreen():

    def __init__(self,app):

        self.app = app
        

    def upload(self):
            
            # Uploading Profile Picture by using Pillow

            file_path = filedialog.askopenfilename(
                filetypes=[("Image files","*.png *.jpg *.jpeg")]
            )

            if not file_path:
                
                return

            with open(file_path,"rb") as file:

                img_binary = file.read()

            self.app.user.profile_pic = img_binary
            self.app.session.commit()
            
            messagebox.showinfo("Succesfull","You have changed your profile photo succesfully.")
            HomePage(self.app).render()
        
        



        