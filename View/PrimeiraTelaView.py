
import customtkinter as ctk
import tkinter as tk
import sys

sys.path.append(
    'D:\Área de Trabalho do hd\estudos\programação\python\zPython-ChatGPT')

from ViewModel import RequisitionViewModel as VM


# Criando a janela

# define App como uma classe
class App(ctk.CTk):
    def __init__(self):
        # Modes: system (default), light, dark
        ctk.set_appearance_mode("Dark")

        # Themes: blue (default), dark-blue, green
        ctk.set_default_color_theme("dark-blue")

        super().__init__()
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # Create textbox and shows it
        self.textbox = ctk.CTkTextbox(master=self, width=300, corner_radius=0)
        self.textbox.grid(row=0, column=0, columnspan=2, pady=15, padx=20, sticky="nsew")
        self.textbox.configure(state="disabled") # not allow to edit it

        # Create and entry
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Fale algo... ",
                                width=180, corner_radius=10)
        self.entry.grid(row=1, column=0, padx=10, pady=5)

        # Create an button and shows it
        self.button = ctk.CTkButton(master=self, text="Send", command=lambda: VM.resposta(self.entry.get()))
        self.button.grid(row=1, column=1, pady=10, padx=10)

if __name__ == "__main__":
    root = App()
    root.mainloop()