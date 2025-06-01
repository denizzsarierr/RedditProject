import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog
from PIL import Image,ImageTk
import io
#Cursor to commit to database
session = Session()


class App(ctk.CTk):


    def __init__(self):
        super().__init__()
        self.title = "Reddit"
        #Windowed Fullscreen
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.resizable(False, False)
        self.user = None
        self.geometry(f"{self.width}x{self.height}")
        self.login_screen()


    def login_screen(self):
        self.clear()
        
        
        container = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
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
            
            if session.query(User).filter_by(username = username_entry.get()).first():

                messagebox.showerror("Error","User already exists.")

            with open("no_user.png","rb") as img:

                default_pic = img.read()

            user = User(username = username_entry.get(),password = password_entry.get(),profile_pic = default_pic)
            session.add(user)
            session.commit()
            messagebox.showinfo("Succesful","User Succesfully Created")
            self.login_screen()



        def login():

            user = session.query(User).filter_by(username = username_entry.get(),password = password_entry.get()).first()

            if user:
                self.user = user
                self.home_page()

            else:
                
                messagebox.showerror("AA","Yok")


        login_btn = ctk.CTkButton(container, text="Login", width=320, height=40, command= login ,fg_color="#EB6304",hover_color= "black")
        login_btn.pack(pady=10)

        register_btn = ctk.CTkButton(container,text = "Register", width = 320,height= 40,command = register,fg_color="#EB6304",hover_color= "black")
        register_btn.pack(pady= 10)

    def home_page(self):
        
        self.clear()
        header = ctk.CTkFrame(self)
        header.pack(fill="x")

        # Left Side of Side Bar
        ctk.CTkLabel(header,
                    text=f"Logged in as: {self.user.username}",
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
        

        image_str = io.BytesIO(self.user.profile_pic)
        pillow_image = Image.open(image_str)

        size = (50, 50)
        pillow_image = pillow_image.resize(size, Image.Resampling.LANCZOS)

        ctk_image = ctk.CTkImage(light_image=pillow_image,dark_image=pillow_image,size=size)
        



        profile_button = ctk.CTkButton(header,
                    command=self.profile_screen,
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
                    command=self.new_post,
                    fg_color="#EB6304",
                    hover_color= "black").pack(side="right", padx=10, pady=10)
        
        # ? Converting Profile Photo from Bytes to file-like object

       



        
        # Show the posts (Flow Page)
        post_container = ctk.CTkScrollableFrame(
        self,
        width=800,      
        height=600,
        corner_radius=12,
        fg_color="transparent"  
        )
        post_container.place(relx=0.5, rely=0.53, anchor="center")

        for post in session.query(Post).order_by(Post.id.desc()).all():

            post_frame = ctk.CTkFrame(post_container,corner_radius=10,fg_color='transparent')
            post_frame.pack(fill = 'x', padx = 20,pady = 10)
            

            ctk.CTkLabel(
            post_frame,
            text=f"r/{post.author.username}",
            font=ctk.CTkFont(size=10, weight="bold"),
            anchor="w"
            ).pack(fill="x", padx=10, pady=(10, 5))

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

         
    def profile_screen(self):

        self.clear()

        def upload():
            
            # Uploading Profile Picture by using Pillow

            file_path = filedialog.askopenfilename(
                filetypes=[("Image files","*.png *.jpg *.jpeg")]
            )

            if not file_path:
                
                return

            with open(file_path,"rb") as file:

                img_binary = file.read()

            self.user.profile_pic = img_binary
            session.commit()
            
            messagebox.showinfo("Succesfull","You have changed your profile photo succesfully.")
            self.home_page()

        button = ctk.CTkButton(self,text="",command = upload)
        button.pack()
        
    def new_post(self):

        self.clear()
        
        back_button = ctk.CTkButton(self, text="← Back", width=80, height=30, command=self.home_page,fg_color="#EB6304",hover_color= "black")
        back_button.place(x=20, y=20)


        hdf_label = ctk.CTkLabel(self, text="How do you feel today?", font=ctk.CTkFont(size=30,weight="bold"))
        hdf_label.pack(pady = 200)

        container = ctk.CTkFrame(self, width=800, height=300, corner_radius=15)
        container.place(relx=0.5, rely=0.5, anchor="center")


        title_entry = ctk.CTkEntry(container, width=640, height=35, placeholder_text="Title...")
        title_entry.pack(padx=40,pady = 10)

        text_entry = ctk.CTkEntry(container, width=640, height=200, placeholder_text="Content...")
        text_entry.pack(padx=40)


        def add_post():

            post = Post(title = title_entry.get(),text = text_entry.get(),author = self.user)

            session.add(post)
            session.commit()
            messagebox.showinfo("Succesfull","Post created succesfully.")
            self.home_page()

        add_post_btn = ctk.CTkButton(container,text="New Post",command=add_post,fg_color="#EB6304",hover_color= "black")
        add_post_btn.pack(padx = 10,pady= 10)

        
        


    

    

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()


# Login Required Decorator (If not logged in, can't post.)
def login_required(func):
    def wrapper(self, *args, **kwargs):
        if not self._user:
            messagebox.showerror("Error", "You must be logged in to do that.")
            return
        return func(self, *args, **kwargs)
    return wrapper

if __name__ == "__main__":

    app = App()

    app.mainloop()



