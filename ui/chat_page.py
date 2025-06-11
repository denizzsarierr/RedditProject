import customtkinter as ctk
from models import Session,User,Post
from tkinter import messagebox,filedialog,PhotoImage
from PIL import Image,ImageTk,ImageDraw
import io
import requests



class ChatPage():

    def __init__(self,app):
        
        self.app = app

    def render(self):
        self.app.clear()

        
        container = ctk.CTkFrame(self.app, width=800, height=600, corner_radius=12)
        container.place(relx=0.5, rely=0.5, anchor="center")

       
        self.chat_container = ctk.CTkScrollableFrame(container,
                                                    width=780,
                                                    height=520,
                                                    corner_radius=12,
                                                    fg_color="#1e1e1e")
        self.chat_container.pack(padx=10, pady=(10, 0), fill="both", expand=False)

        
        input_frame = ctk.CTkFrame(container, fg_color="transparent")
        input_frame.pack(fill="x", pady=10, padx=10)

        self.message_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message...")
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)

        send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_message)
        send_button.pack(side="right")

    def insert_message(self, sender, message):
        label = ctk.CTkLabel(self.chat_container,
                            text=f"{sender}: {message}",
                            anchor="w",
                            justify="left",
                            wraplength=750)
        
        if sender == "You":
            label.configure(anchor = "e",justify = 'right')

        else:
            label.configure(
                anchor="e",
                justify="left",
                text_color="green",
                font=("Helvetica",14,"bold")
            )

        label.pack(anchor="w", padx=10, pady=5)
        self.chat_container.update_idletasks()
        self.chat_container._parent_canvas.yview_moveto(1.0)


    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.message_entry.delete(0, 'end')
            self.insert_message("You", message)

            # Dummy AI response
            response = f"{self.ollama_chat(message)}"
            self.insert_message("RedditAI", response)


    def ollama_chat(self,prompt):

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
    


# while True:
#     user_input = input("Sen: ")
#     if user_input.lower() in ["çık", "exit", "quit"]:
#         break
#     cevap = ollama_chat(user_input)
#     print("AI:", cevap)