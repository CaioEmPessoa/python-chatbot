import customtkinter as ctk

class FirstUI(ctk.CTkToplevel): # After testing, change to "ctk.CTkToplevel"

    def send_info(self, app):
        app.api_key = self.api_entry.get()

        app.user = self.user_entry.get()

        app.first_window.destroy()

        self.print(self.api_key)

    def __init__(self, app):
        super().__init__()

        # Set Configs for window
        self.title('Bem vindo ao alibabot!')

        # textos da janela
        self.welcome = ctk.CTkLabel(master=self, text="Bem Vindo ao AlibaBot!")
        self.welcome.grid(row=1, column=0, columnspan=2)
        
        self.api_label = ctk.CTkLabel(master=self, text="Insira aqui sua chave de api:")
        self.api_label.grid(row=2, column=0, padx=15, pady=10)

        self.api_label = ctk.CTkLabel(master=self, text="Insira aqui seu usuário:")
        self.api_label.grid(row=3, column=0, padx=15, pady=10)
        
        # Elementos da janela
        self.api_entry = ctk.CTkEntry(master= self, placeholder_text="Seu código de API...")
        self.api_entry.grid(row=2, column=1)

        self.user_entry = ctk.CTkEntry(master= self, placeholder_text="Seu usuário...")
        self.user_entry.grid(row=3, column=1)

        self.confirm_button = ctk.CTkButton(master=self, text="Confirmar", command=lambda: self.send_info(app))
        self.confirm_button.grid(row=4, column=0, pady=10, columnspan=2)

        self.help_button = ctk.CTkButton(master=self, image=app.help_icon, width=10,
                                         fg_color="#282424", hover_color="gray", text='')
        self.help_button.grid(row=0, column=1, sticky="E")

        self.config_button = ctk.CTkButton(master=self, text="", 
                                           width=10, image=app.config_icon, 
                                           fg_color="#282424", hover_color="gray",
                                           command=app.call_config)

        self.config_button.grid(row=0, column=0, sticky="W")

# Change after testing
if __name__ == "__main__":
    gui = FirstUI(ctk.CTk)
    gui.mainloop()