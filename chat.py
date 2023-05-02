
import customtkinter as ctk
import tkinter as tk
import openai
from PIL import Image, ImageTk
import os

openai.api_key = "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"

#janela de config
class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__()

        # Set Configs for window
        self.title('Config Alibabot')

        self.minsize(300, 300)
        self.maxsize(300, 300)

        def apply():

            # Pega o valor escolhido nas caixas
            self.fonte = self.font_box.get()
            self.sans = self.checkbox.get()
            self.tema = self.temas_box.get()

            # Altera o valor que aparecerá como padrão na proxima
            self.font_box.set(self.fonte)
            self.checkbox.toggle()
            self.temas_box.set(self.tema)

            app.change_font(self.sans)
            app.change_font(self.fonte)

            app.config_window.destroy()

        # Labels 
        self.temas_label = ctk.CTkLabel(master=self, text="Temas:")
        self.temas_label.grid(row=0, column=0, padx=10)

        self.fonte_label = ctk.CTkLabel(master=self, text="Fonte:")
        self.fonte_label.grid(row=1, column=0, padx=10)

        self.sans_label = ctk.CTkLabel(master=self, text="Comic Sans?")
        self.sans_label.grid(row=2, column=0, padx=10)

        # Caixas de escolha----- -------------------------------<
        # Caixa dos temas
        self.temas_box = ctk.CTkOptionMenu(master=self,
                                       values=["Escuro (Padrão)", "Claro", 
                                               "Metal","Hello Kitty"])
        self.temas_box.grid(row=0, column=1, padx=10, pady=10)

        # Caixa da fonte
        self.font_box = ctk.CTkOptionMenu(master=self,
                                       values=["Pequena", "Média", "Grande"])
        self.font_box.grid(row=1, column=1, padx=10, pady=10)

        # Checkbox
        self.checkbox = ctk.CTkCheckBox(master=self, text="",
                                         onvalue="on", offvalue="off")
        self.checkbox.grid(row=2, column=1, padx=10, pady=10)
        # >---------------------------------- END CaixasEscolha

        self.apply_button = ctk.CTkButton(master=self, text="Aplicar.", width=5, command=apply)
        self.apply_button.grid(row=5, column=1, columnspan=3, sticky="S", pady=10)


# Criando a janela
class App(ctk.CTk):

    def fechar(self):
        root.quit()

    def call_config(self):
        if self.config_window is None or not self.config_window.winfo_exists():
            self.config_window = ConfigWindow(self)  # create window if its None or destroyed
            self.config_window.grab_set()


    def change_font(self, choice):

        print("Fonte Escolhida: " + choice)

        if choice == "on":
            print("sans")
            self.fonte = 'Comic Sans MS'

        if choice == "off":
            self.fonte = 'Segoe UI'

        match choice:
            case "Pequena":
                self.textbox.configure(state="disabled", font=(self.fonte, 13))
                print("trocada " + self.fonte)
            
            case "Média":
                self.textbox.configure(state="disabled", font=(self.fonte, 18))
                print("trocada " + self.fonte)

            case "Grande":
                self.textbox.configure(state="disabled", font=(self.fonte, 30))
                print("trocada " + self.fonte)

    def __init__(self):
        super().__init__()

        self.config_window = None

        # Modes: system (default), light, dark
        ctk.set_appearance_mode("Dark")
        # Themes: blue (default), dark-blue, green
        ctk.set_default_color_theme("dark-blue")

        # Configure the window
        self.title('Chat with Alibabot')

        self.minsize(300, 300)
        self.maxsize(750, 950)

        self.grid_rowconfigure((1,2), weight=1)  # configure grid system
        self.grid_columnconfigure((0, 1), weight=1)
        


        # Perguntas e Respostas Escritas <-------------------------------------------------------
        def resposta():
            #pega o que ta escrito na entrada
            entry = self.entry.get()
            # pega oq ta escrito na textbox
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": entry}
                ]
            )

            bot_msg = str('Alibabot: ' + completion.choices[0].message.content)
            self.textbox.configure(state="normal") # allow to edit it
            self.textbox.insert("end", bot_msg + '\n\n')
            self.textbox.configure(state="disabled", text_color='white') # not allow to edit it

        def pergunta(x):
            #pega o que ta escrito na entrada
            entry = self.entry.get()
            
            # Monta a mensagem
            user = 'Usuário' + ': '

            self.textbox.configure(state="normal") # not allow to edit it
            self.textbox.insert("end", f'{user} {entry} \n')

            self.textbox.configure(state="disabled", text_color='red') # not allow to edit it
            resposta()
        # --------------------------------------------------> END Perguntas e Respostas Escritas


        # Image Config ------------------------------------------------------------------------------------------------<
        # Import Location of the code for images
        self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\img\\"

        # Images of the GUI
        self.config_icon = ImageTk.PhotoImage(Image.open(self.location + "config.png").resize((30,30), Image.ANTIALIAS))

        self. off_mic_icon = ImageTk.PhotoImage(Image.open(self.location + "mic.png").resize((30,30), Image.ANTIALIAS))

        # >-------------------------------------------------------------------------------------------- END Image Config


        # Buttons and Entrys ------------------------------------------------------<
        # Create textbox and shows it
        self.textbox = ctk.CTkTextbox(master=self, 
                                      width=400, height=200, corner_radius=0)
        self.textbox.grid(row=1, column=0, 
                          columnspan=3, pady=15, padx=20, sticky="nsew")

        # Create and entry
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Fale algo... ",
                                width=240, corner_radius=10)
        
        self.entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Create an button and shows it
        self.send_button = ctk.CTkButton(master=self, text="Send", 
                                         corner_radius=10, width=15, 
                                         command=lambda: pergunta('x'))

        self.send_button.grid(row=2, column=2, pady=10, padx=10, sticky="ew")


        self.mic_button = ctk.CTkButton(master=self, text="",
                                           width=5, image=self.off_mic_icon, 
                                           fg_color="#282424", hover_color="gray",
                                           command=self.call_config)
        self.mic_button.grid(row=2, column=0)


        # Config Button
        self.config_button = ctk.CTkButton(master=self, text="", 
                                           width=10, image=self.config_icon, 
                                           fg_color="#282424", hover_color="gray",
                                           command=self.call_config)

        self.config_button.grid(row=0, column=0, sticky="W")

        # >------------------------------------------------- END Buttons and Entrys

        # bind keys -------------------<
        self.bind('<Return>', pergunta)
        self.bind('<Escape>', App.fechar)
        # >----------------END bind keys

if __name__ == "__main__":
    root = App()
    root.mainloop()