
import customtkinter as ctk
import tkinter as tk
import openai

openai.api_key = "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"

# Criando a janela

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Modes: system (default), light, dark
        ctk.set_appearance_mode("Dark")
        # Themes: blue (default), dark-blue, green
        ctk.set_default_color_theme("dark-blue")

        # Configure the window
        self.title('Chat with Alibabot')

        self.minsize(300, 300)
        self.maxsize(700, 750)

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure((0, 1), weight=1)
        

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
            self.textbox.configure(state="normal") # not allow to edit it
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

        def fechar(ss):
            self.quit()

        # Create textbox and shows it
        self.textbox = ctk.CTkTextbox(master=self, width=400, height=200, corner_radius=0)
        self.textbox.grid(row=0, column=0, columnspan=3, pady=15, padx=20, sticky="nsew")

        # Create and entry
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Fale algo... ",
                                width=240, corner_radius=10)
        self.entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Create an button and shows it
        self.button = ctk.CTkButton(master=self, text="Send", command=lambda: pergunta('x'), corner_radius=10, width=10)
        self.button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        # bind keys
        self.bind('<Return>', pergunta)
        self.bind('<Escape>', fechar)

if __name__ == "__main__":
    root = App()
    root.mainloop()