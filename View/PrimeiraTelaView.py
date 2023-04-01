import tkinter as tk
import customtkinter as ctk
import ViewModel.RequisitionViewModel as VM

#Criando janela

# Modes: system (default), light, dark
ctk.set_appearance_mode("Dark")

# Themes: blue (default), dark-blue, green
ctk.set_default_color_theme("dark-blue")


root = ctk.CTk()
root.title('Caio e foda')
root.geometry('300x300')


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure((0, 1, 2), weight=1)

button = ctk.CTkButton(master=root, text="teste", command=VM.heloWorld)
button.pack()

root.mainloop()