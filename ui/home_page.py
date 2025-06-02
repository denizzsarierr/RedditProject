import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io



class HomePage():

    def __init__(self,app):

        self.app = app

    def make_circle_image(self,image: Image.Image, size=(20, 20)) -> Image.Image:

        image = image.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = Image.new("RGBA", size)
        result.paste(image, (0, 0), mask=mask)
        return result
    
    def render(self):
        from ui.new_post_screen import NewPostScreen

        self.app.clear()
        header = ctk.CTkFrame(self.app)
        header.pack(fill="x")

        # Left Side of Side Bar
        ctk.CTkLabel(header,
                    text=f"Logged in as: {self.app.user.username}",
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=10, pady=10)
        
        # Right Side of Side Bar
        
        # def switch_mode():
        #     condition = mode_switch.get()

        #     if condition:
        #         self._set_appearance_mode("light")
        #     else:
        #         self._set_appearance_mode("dark")

        # mode_switch = ctk.CTkSwitch(header,text = "",onvalue= 1,offvalue=0,command = switch_mode)
        
        # mode_switch.pack()
        

        image_str = io.BytesIO(self.app.user.profile_pic)
        pillow_image = Image.open(image_str)

        size = (50, 50)
        pillow_image = pillow_image.resize(size, Image.Resampling.LANCZOS)

        ctk_image = ctk.CTkImage(light_image=pillow_image,dark_image=pillow_image,size=size)
        


        from ui.profile_screen import ProfileScreen
        profile_button = ctk.CTkButton(header,
                    command=lambda: ProfileScreen(self.app).render(),
                    image = ctk_image,
                    text="",
                    width = 50,
                    height=50,
                    corner_radius=25,
                    fg_color='transparent',
                    hover = False)
        profile_button.pack(side="right", padx=10, pady=10)

        ctk.CTkButton(header,
                    text="New Post",
                    command=lambda: NewPostScreen(self.app).render(),
                    fg_color="#EB6304",
                    hover_color= "black").pack(side="right", padx=10, pady=10)
        
        # ? Converting Profile Photo from Bytes to file-like object

       



        
        # Show the posts (Flow Page)
        post_container = ctk.CTkScrollableFrame(
        self.app,
        width=800,      
        height=600,
        corner_radius=12,
        fg_color="transparent"  
        )
        post_container.place(relx=0.5, rely=0.53, anchor="center")

        for post in self.app.session.query(Post).order_by(Post.id.desc()).all():

            post_frame = ctk.CTkFrame(post_container,corner_radius=10,fg_color='transparent')
            post_frame.pack(fill = 'x', padx = 20,pady = 10)


            # Adding Profile Picture To Post
            user_frame = ctk.CTkFrame(post_frame,fg_color="transparent")
            user_frame.pack(fill='x', padx=10, pady=(10, 5))

            pillow_image_size = (20,20)
            pillow_image_post = self.make_circle_image(pillow_image,pillow_image_size)
            

            ctk_image_post = ctk.CTkImage(light_image=pillow_image_post,dark_image=pillow_image_post,size=pillow_image_size)


            profile_pic_label = ctk.CTkLabel(user_frame,image = ctk_image_post,text = "")
            profile_pic_label.pack(side = 'left', padx = (0,5))

            ctk.CTkLabel(
            user_frame,
            text=f"r/{post.author.username}",
            font=ctk.CTkFont(size=10, weight="bold"),
            anchor="w"
            ).pack(side = 'left',pady = 2)
            # fill="x", padx=10, pady=(10, 5)

            ctk.CTkLabel(
            post_frame,
            text=post.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
            ).pack(fill="x", padx=10, pady=(10, 5))

        # Post content
            ctk.CTkLabel(
            post_frame,
            text=post.text,
            font=ctk.CTkFont(size=14),
            anchor="w",
            wraplength=760, 
            justify="left"
            ).pack(fill="x", padx=10, pady=(0, 10))