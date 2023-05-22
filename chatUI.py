import customtkinter as ctk
from PIL import Image, ImageTk
from pvrecorder import PvRecorder
import openai
import os
#My Code
import inicialUI
import configUI
import chatAI
import micSTT

def start():
    if __name__ == "__main__":
        root = App()
        root.mainloop()

# Criando a janela
class App(ctk.CTk):

    def fechar(self):
        root.quit()

    def call_config(self):
        if self.config_window is None or not self.config_window.winfo_exists():
            self.config_window = configUI.ConfigWindow(self)  # create window if its None or destroyed
            self.config_window.grab_set()

    def restart(self):
        # Reiniciar a tela e manter as configurações dos botões
        self.destroy()
        start()


    def change_font(self, choice):
        if choice == "on":
            self.fonte = 'Comic Sans MS'

        if choice == "off":
            self.fonte = 'Segoe UI'

        match choice:
            case "Pequena":
                self.textbox.configure(state="disabled", font=(self.fonte, 13))

            case "Média":
                self.textbox.configure(state="disabled", font=(self.fonte, 18))

            case "Grande":
                self.textbox.configure(state="disabled", font=(self.fonte, 30))

    def change_theme(self, choice):
        self.tema = choice

        match choice:

            case "Claro":
                # Modes: system (default), light, dark
                ctk.set_appearance_mode("Light")
                # Themes: blue (default), dark-blue, green
                ctk.set_default_color_theme("green")

                self.mic_button.configure(fg_color="#ebebeb")
                self.config_button.configure(fg_color="#ebebeb")

                # Troca a letra da fonte, pra preta
                self.text_color = 'black'
                self.textbox.configure(state="disabled", text_color=self.text_color)


            case "Escuro (Padrão)":

                # Modes: system (default), light, dark
                ctk.set_appearance_mode("Dark")
                # Themes: blue (default), dark-blue, green
                ctk.set_default_color_theme("blue")
                self.mic_button.configure(fg_color="#282424")
                self.config_button.configure(fg_color="#282424")

                
                self.text_color = 'white'
                self.textbox.configure(state="disabled", text_color=self.text_color)

            case "Metal":
                tema_padrao = "Metal"
                # Themes: blue (default), dark-blue, green
                ctk.set_default_color_theme("Themes\\dedfault.json")

                self.destroy()
                start()
        
        self.restart()


    def new_entry(self, entry):
        
        self.textbox.configure(state="normal") # allow to edit it                        
        self.textbox.insert("end", entry)
        self.textbox.configure(state="disabled", text_color=self.text_color) # not allow to edit it

    # Root Config ----------------------------------------------------------<
    def __init__(self):
        super().__init__()

        # Configure the window
        self.title('Chat with Alibabot')

        self.minsize(50, 500)

        self.grid_rowconfigure((1), weight=1)  # configure grid system
        self.grid_columnconfigure((1), weight=1)

    # >------------------------------------------------------ END Root Config 

    # Set Dedfault Values ----------------------------------------------<
        self.recording = False
        self.mic = 1 # Change the mic
        self.recorder = PvRecorder(device_index=-self.mic, frame_length=512)
        self.audio = [] # on what the audio will be stored

        self.conversa = []
        self.bot_msg = []
        self.text_color = 'white'

        self.config_window = None
        self.first_window = None

        self.user = "Usuário"
        self.api_key = ""

        openai.api_key = self.api_key

        global tema_padrao

    # >------------------------------------------- END Setting Dedfault Values

        # Image Config ------------------------------------------------------------------------------------------------<
        # Import Location of the code for images
        self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\img\\"

        try:
            # Images of the GUI
            self.config_icon = ImageTk.PhotoImage(Image.open(self.location + "config.png").resize((30,30), Image.ANTIALIAS))

            self.help_icon = ImageTk.PhotoImage(Image.open(self.location + "help.png").resize((30,30), Image.ANTIALIAS))

            self.off_mic_icon = ImageTk.PhotoImage(Image.open(self.location + "mic.png").resize((30,30), Image.ANTIALIAS))

            self.on_mic_icon = ImageTk.PhotoImage(Image.open(self.location + "mic_on.png").resize((30,30), Image.ANTIALIAS))

        except:
            print('')

        # >-------------------------------------------------------------------------------------------- END Image Config


        # Buttons and Entrys ------------------------------------------------------<
        # Create textbox and shows it
        self.textbox = ctk.CTkTextbox(master=self, state="disabled",
                                      width=400, height=200, corner_radius=0)
        self.textbox.grid(row=1, column=0, 
                          columnspan=3, pady=15, padx=20, sticky="nsew")

        # Create and entry
        self.entry = ctk.CTkEntry(master=self, placeholder_text="Fale algo... ",
                                width=240, corner_radius=10)
        
        self.entry.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        # Create an button and shows it
        self.send_button = ctk.CTkButton(master=self, text="Send", 
                                         corner_radius=10, width=150, 
                                         command=lambda: chatAI.pergunta(self))

        self.send_button.grid(row=2, column=2, pady=10, padx=10, sticky="nsew")


        self.mic_button = ctk.CTkButton(master=self, text="",
                                           width=100, image=self.off_mic_icon, 
                                           fg_color="#282424", hover_color="gray",
                                           command=lambda: micSTT.toggle_recording(app=self))
        self.mic_button.grid(row=2, column=0)


        # Config Button
        self.config_button = ctk.CTkButton(master=self, text="", 
                                           width=10, image=self.config_icon, 
                                           fg_color="#282424", hover_color="gray",
                                           command=self.call_config)

        self.config_button.grid(row=0, column=0, sticky="W")

        # >------------------------------------------------- END Buttons and Entrys

        # bind keys -------------------<
        self.bind('<Return>', lambda event:chatAI.pergunta(self))
        self.bind('<Escape>', App.fechar)
        # >----------------END bind keys

        if self.first_window is None or not self.first_window.winfo_exists():
            self.first_window = inicialUI.FirstUI(self)  # create window if its None or destroyed
            self.first_window.grab_set()
        else:
            print(inicialUI.FirstUI.send_info.api_key)



start()

print('sad')
#clear cache
try:
    os.remove("audio.wav")

except:
    print('Não tem arquivo de audio :)')