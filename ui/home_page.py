import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io
from ui.chat_page import ChatPage





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

    def search_by_string(self,event = None):
        
        # Clearing previous results.
        for widget in self.results_frame.winfo_children():
        
            widget.destroy()
        
        
        input_string = self.search_bar.get()
        if input_string:

            # searching from DATABASE.
            data = self.app.session.query(Post).filter(Post.title.ilike(f"{input_string}%")).all()
            
            if data:
                
                self.results_container.pack(side="top", anchor="center",pady=(0,10), padx=10)
                self.results_container.pack_propagate(False)

                self.results_frame.pack(fill="both", expand=True)

                for post in data:

                    #element = ctk.CTkLabel(self.results_frame,text = f"🔍  {title}",anchor="w")
                    
                    element = ctk.CTkButton(
                    self.results_frame,
                    text=f"🔍  {post.title}",
                    anchor="w",
                    fg_color="transparent",
                    hover_color="#333333",
                    text_color="white",
                    corner_radius=0,
                    command=lambda p=post: self.clicked_post(p))
                    element.pack(fill = "x",padx =5,pady =2)
                    hr = ctk.CTkFrame(self.results_frame, height=1, fg_color="white")
                    hr.pack(fill="x", padx=10, pady=4)
                    
            else:
                self.results_container.pack_forget()
        else:
            self.results_container.pack_forget()

    def render(self):
        from ui.new_post_screen import NewPostScreen

        self.app.clear()
        header = ctk.CTkFrame(self.app)
        header.pack(fill="x")

        # Left Side of Header
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", padx=10, pady=10)
        reddit_logo = Image.open("ui/reddit_logo.png")
        logo_size =(30,30)

        reddit_logo_resized = reddit_logo.resize(logo_size,Image.Resampling.LANCZOS)
        reddit_logo_ctk = ctk.CTkImage(light_image=reddit_logo_resized, dark_image=reddit_logo_resized, size=logo_size)
        
        ctk.CTkLabel(left_frame,
                     text = "",
                     image=reddit_logo_ctk,
                     width=30,
                     height=30).pack(side = 'left', padx =10 ,pady = 10)
        ctk.CTkLabel(left_frame,
                    text="reddit",
                    font=ctk.CTkFont(size=30,weight='bold'),
                    text_color='#EB6304').pack(side="left", padx=5, pady=10)
        
        # Search Bar - Center of Header
        center_frame = ctk.CTkFrame(header, fg_color="transparent")
        center_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        self.search_bar = ctk.CTkEntry(center_frame,placeholder_text="🔍 Search Reddit",width = 200)
        self.search_bar.pack(pady = 10,expand = True)
        self.search_bar.bind("<KeyRelease>",self.search_by_string)

        self.results_container = ctk.CTkFrame(self.app, width=400, height=400)
        self.results_frame = ctk.CTkScrollableFrame(self.results_container)
        
        
        
        # Right Side of Side Bar
        
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", padx=10, pady=10)

        # Reading Profile Pic 
        image_str = io.BytesIO(self.app.user.profile_pic)
        pillow_image = Image.open(image_str)

        size = (50, 50)
        pillow_image = pillow_image.resize(size, Image.Resampling.LANCZOS)

        ctk_image = ctk.CTkImage(light_image=pillow_image,dark_image=pillow_image,size=size)
        

        reddit_logo_resized = reddit_logo.resize(logo_size,Image.Resampling.LANCZOS)
        reddit_logo_ctk = ctk.CTkImage(light_image=reddit_logo_resized, dark_image=reddit_logo_resized, size=logo_size)
        
        # Reading Plus Pic
        plus_logo = Image.open("ui/plus.png")
        plus_logo_size =(50,50)
        plus_logo_resized = plus_logo.resize(logo_size,Image.Resampling.LANCZOS)
        plus_logo_ctk = ctk.CTkImage(light_image=plus_logo_resized, dark_image=plus_logo_resized, size=plus_logo_size)

        from ui.profile_screen import ProfileScreen
        profile_button = ctk.CTkButton(right_frame,
                    command=self.profile_options,
                    image = ctk_image,
                    text="",
                    width = 50,
                    height=50,
                    corner_radius=25,
                    fg_color='transparent',
                    hover = False)
        profile_button.pack(side="right", padx=10, pady=10)

        ctk.CTkButton(right_frame,
                    image = plus_logo_ctk,
                    text="",
                    width = 50,
                    height=50,
                    fg_color='transparent',
                    command=lambda: NewPostScreen(self.app).render(),
                    hover = False).pack(side="right", padx=10, pady=10)
        
        ctk.CTkButton(right_frame,
                      text = "RedditAI",
                      width = 50,
                      height=50,
                      fg_color='transparent',
                      command = lambda : ChatPage(self.app).render(),
                      hover = False).pack(side = "right",padx =10,pady = 10)
        
        # ? Converting Profile Photo from Bytes to file-like object


        # Show the posts (Flow Page)
        self.post_container = ctk.CTkScrollableFrame(
        self.app,
        width=800,      
        height=600,
        corner_radius=12,
        fg_color='transparent',
        bg_color='transparent')
        self.post_container.place(relx=0.5, rely=0.53, anchor="center")

        for post in self.app.session.query(Post).order_by(Post.id.desc()).all(): 

            self.post_frame = ctk.CTkFrame(self.post_container,corner_radius=10,fg_color="transparent",bg_color="transparent")
            self.post_frame.pack(fill = 'x', padx = 20,pady = 10)


            # Adding Profile Picture To Post
            self.user_frame = ctk.CTkFrame(self.post_frame,fg_color="transparent",bg_color='transparent')
            self.user_frame.pack(fill='x', padx=10, pady=(10, 5))

            author_image_b = io.BytesIO(post.author.profile_pic)
            author_image = Image.open(author_image_b).resize((20, 20), Image.Resampling.LANCZOS)
            author_img_circle = self.make_circle_image(author_image, (20, 20))

            ctk_image_post = ctk.CTkImage(light_image=author_img_circle,dark_image=author_img_circle,size=(20,20))


            profile_pic_label = ctk.CTkLabel(self.user_frame,image = ctk_image_post,text = "")
            profile_pic_label.pack(side = 'left', padx = (0,5))

            ctk.CTkLabel(
            self.user_frame,
            text=f"u/{post.author.username}",
            font=ctk.CTkFont(size=10, weight="bold"),
            anchor="w",
            bg_color='transparent'
            ).pack(side = 'left',pady = 2)
            # fill="x", padx=10, pady=(10, 5)

            ctk.CTkLabel(
            self.post_frame,
            text=post.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            bg_color='transparent'
            ).pack(fill="x", padx=10, pady=(10, 5))

        # Post content
            self.post_content = ctk.CTkLabel(
            self.post_frame,
            text=post.text,
            font=ctk.CTkFont(size=14),
            anchor="w",
            wraplength=760, 
            justify="left"
            )
            self.post_content.pack(fill="x", padx=10, pady=(0, 10))

        
        
        # Profile actions when clicked.
        self.profile_action_container = ctk.CTkFrame(self.app,width =200,height = 400)
        self.actions_frame = ctk.CTkFrame(self.profile_action_container)
        
        # Definin Actions
        
        # Close
        self.close = ctk.CTkButton(self.actions_frame,
                                   text = "← Back",
                                   bg_color='transparent',
                                   fg_color='transparent',
                                   hover = False,
                                   command= lambda : self.profile_action_container.pack_forget() )

        #Update Avatar
        self.update_avatar = ctk.CTkButton(self.actions_frame,
                                           text = "Update Avatar",
                                           bg_color='transparent',
                                           fg_color = 'transparent',
                                           hover = False,
                                           command = lambda : ProfileScreen(self.app).upload())
        
        # Dark-Light Mode
        self.switch_appearance = ctk.CTkSwitch(self.actions_frame,
                                               text = "☾ Dark Mode",
                                               onvalue=1,
                                               offvalue=0,
                                               command=self.switch_mode) 
        
        
        
    def profile_options(self):

        from ui.profile_screen import ProfileScreen

        self.profile_action_container.pack(side = "top", anchor = "ne")
        self.profile_action_container.pack_propagate(False)

        self.actions_frame.pack(fill="both", expand=True)

        
        self.close.pack(pady = 10)
        self.update_avatar.pack(pady = 10)
        self.switch_appearance.pack(pady = 10)

        
    def clicked_post(self,p):

        self.results_container.pack_forget()
        

        for widget in self.post_container.winfo_children():
            widget.destroy()

        self.post_frame = ctk.CTkFrame(self.post_container,corner_radius=10,fg_color="transparent",bg_color="transparent")
        self.post_frame.pack(fill = 'x', padx = 20,pady = 10)

        self.user_frame = ctk.CTkFrame(self.post_frame,fg_color="transparent",bg_color='transparent')
        self.user_frame.pack(fill='x', padx=10, pady=(10, 5))

        ctk.CTkLabel(
            self.user_frame,
            text=f"u/{p.author.username}",
            font=ctk.CTkFont(size=10, weight="bold"),
            anchor="w",
            bg_color='transparent'
            ).pack(side = 'left',pady = 2)
            # fill="x", padx=10, pady=(10, 5)

        ctk.CTkLabel(
            self.post_frame,
            text=p.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            bg_color='transparent'
            ).pack(fill="x", padx=10, pady=(10, 5))

        # Post content
        self.post_content = ctk.CTkLabel(
        self.post_frame,
        text=p.text,
        font=ctk.CTkFont(size=14),
        anchor="w",
        wraplength=760, 
        justify="left"
        )
        self.post_content.pack(fill="x", padx=10, pady=(0, 10))

        back_button = ctk.CTkButton(self.app, text="← Back", width=80, height=30, command=lambda : HomePage(self.app).render(),fg_color="#EB6304",hover_color= "black")
        back_button.place(x=175 , y=35)
    
    
        
    # Switching between dark and light mode.
    def switch_mode(self):
        condition = self.switch_appearance.get()

        if condition == 1:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        self.appearance_mode_change()
    

    # Additional changes for dark and light mode
    def appearance_mode_change(self):

        mode = ctk.get_appearance_mode()
        text_color = 'black' if mode == "Light" else 'white'

        self.update_avatar.configure(text_color = text_color)
        self.close.configure(text_color=text_color)
        
