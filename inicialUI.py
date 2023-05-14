import customtkinter as ctk

class FirstUI(ctk.CTk): # After testing, change to "ctk.CTkToplevel"

    def send_info(self):
        self.api_key = self.api_entry.get()
        

        root.quit()

        self.print(self.api_key)

    def __init__(self, app):
        super().__init__()

        # Set Configs for window
        self.title('Bem vindo ao alibabot!')


        # textos da janela
        self.welcome = ctk.CTkLabel(master=self, text="Bem Vindo ao AlibaBot!")
        self.welcome.grid(row=0, column=0, columnspan=2)
        
        self.api_label = ctk.CTkLabel(master=self, text="Insira aqui sua chave de api:")
        self.api_label.grid(row=1, column=0, padx=15, pady=10)
        
        # Elementos da janela
        self.api_entry = ctk.CTkEntry(master= self, placeholder_text="Seu código de API...")
        self.api_entry.grid(row=1, column=1)

        self.confirm_button = ctk.CTkButton(master=self, text="Confirmar", command=self.send_info)
        self.confirm_button.grid(row=2, column=0, columnspan=2)

# Change after testing
if __name__ == "__main__":
    root = FirstUI(ctk.CTk)
    root.mainloop()