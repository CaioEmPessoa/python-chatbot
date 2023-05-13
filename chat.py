
import customtkinter as ctk
import tkinter as tk
import threading
from queue import Queue
from pvrecorder import PvRecorder
import wave, struct
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
        self.maxsize(450, 300)

        def apply():

            # Pega o valor escolhido nas caixas
            self.fonte = self.font_box.get()
            self.sans = self.checkbox.get()
            self.tema = self.temas_box.get()
            self.device = self.devices_box.get()

            # Altera o valor que aparecerá como padrão na proxima
            self.font_box.set(self.fonte)
            self.checkbox.toggle()
            self.temas_box.set(self.tema)

            # Troca a fonte
            app.change_font(self.sans)
            app.change_font(self.fonte)

            # Troca o tema
            app.change_theme(self.tema)

            # Troca o dispositivo
            self.mic = self.device[0]
            self.recorder = PvRecorder(device_index=-int(self.mic), frame_length=512)


            # Fecha a aba de config
            app.config_window.destroy()

        mic_list = []
        for mic in PvRecorder.get_audio_devices():
            start_index = mic.find('(') + 1
            end_index = mic.find(')')

            mic_number = PvRecorder.get_audio_devices().index(mic)
            mic_list.append(str(mic_number) + " - " + mic[start_index:end_index])

        # Labels 
        self.temas_label = ctk.CTkLabel(master=self, text="Temas:")
        self.temas_label.grid(row=0, column=0, padx=10, sticky="W")

        self.fonte_label = ctk.CTkLabel(master=self, text="Fonte:")
        self.fonte_label.grid(row=1, column=0, padx=10, sticky="W")

        self.sans_label = ctk.CTkLabel(master=self, text="Comic Sans:")
        self.sans_label.grid(row=2, column=0, padx=10, sticky="W")

        self.devices_label = ctk.CTkLabel(master=self, text="Microfone: ")
        self.devices_label.grid(row=3, column=0, padx=10, sticky="W")

        # Caixas de escolha----- -------------------------------<
        # Caixa dos temas
        self.temas_box = ctk.CTkOptionMenu(master=self,
                                       values=["Escuro (Padrão)", "Claro", 
                                               "Metal","Hello Kitty"])
        self.temas_box.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        # Caixa da fonte
        self.font_box = ctk.CTkOptionMenu(master=self,
                                       values=["Pequena", "Média", "Grande"])
        self.font_box.grid(row=1, column=1, padx=10, pady=10, sticky="W")

        # Mic Devices
        self.devices_box = ctk.CTkOptionMenu(master=self,
                                            values=mic_list)
        self.devices_box.grid(row=3, column=1, padx=10, pady=10, sticky="W")

        # Checkbox
        self.checkbox = ctk.CTkCheckBox(master=self, text="",
                                         onvalue="on", offvalue="off")
        self.checkbox.grid(row=2, column=1, padx=10, pady=10, sticky="W")
        
        # >---------------------------------- END CaixasEscolha

        self.apply_button = ctk.CTkButton(master=self, text="Aplicar.", width=5, command=apply)
        self.apply_button.grid(row=5, column=1, columnspan=3, sticky="W", pady=10)


# Criando a janela
class App(ctk.CTk):

    def fechar(self):
        root.quit()

    def call_config(self):
        if self.config_window is None or not self.config_window.winfo_exists():
            self.config_window = ConfigWindow(self)  # create window if its None or destroyed
            self.config_window.grab_set()


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
        match choice:

            case "Claro":
                # Modes: system (default), light, dark
                ctk.set_appearance_mode("Light")
                # Themes: blue (default), dark-blue, green
                ctk.set_default_color_theme("dark-blue")
                self.mic_button.configure(fg_color="#ebebeb")
                self.config_button.configure(fg_color="#ebebeb")

                # Troca a letra da fonte, pra branca
                self.text_color = 'black'
                self.textbox.configure(state="disabled", text_color=self.text_color)

            case "Metal":
                # Themes: blue (default), dark-blue, green
                ctk.set_default_color_theme("D:\Área de Trabalho do hd\estudos\programação\python\projetos\Python-ChatGPT\Themes\\dedfault.json")

            case "Escuro (Padrão)":
                # Modes: system (default), light, dark
                ctk.set_appearance_mode("Dark")
                # Themes: blue (default), dark-blue, green
                ctk.set_default_color_theme("dark-blue")
                self.mic_button.configure(fg_color="#282424")
                self.config_button.configure(fg_color="#282424")

                
                self.text_color = 'white'
                self.textbox.configure(state="disabled", text_color=self.text_color)


    # Audio Things ------------------------------------------------------------<
    def speech_text(self):
        print("Traduzindo... ")
        audio_file = open("audio.wav", "rb") # Lê o "audio.wav"
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript.text)
        self.entry.insert(0, str(transcript.text))

    def toggle_recording(self):
        

        if not self.recording: # Se nao está gravando
            self.recording = True # Esta gravando

            # Muda o botão pro vermelho
            self.mic_button.configure(image=self.on_mic_icon)

            # Começa a thread de gravar
            self.record_audio_thread = threading.Thread(target=self.record_audio)
            self.record_audio_thread.start()
            
        # Se esta gravando
        else:
            self.recording = False  # Não está gravando

            # Muda o ícone pro normal
            self.mic_button.configure(image=self.off_mic_icon)

            # Para de gravar
            self.recorder.stop()

            # salva o arquivo
            with wave.open(self.store_path, 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(self.audio), *self.audio))

            self.audio = []
            self.speech_text() # chama pra traduzir

    def record_audio(self):

        # Começa a gravar realmente
        self.recorder.start()
        #Enquanto grava, manda cada frame dela pra lista "audio"
        while self.recording:
            frame = self.recorder.read()
            self.audio.extend(frame)

        self.recorder.stop()
    # >------------------------------------------------- END Audio Things


    # Root Config ----------------------------------------------------------<
    def __init__(self):
        super().__init__()
        self.config_window = None

        # Modes: system (default), light, dark
        ctk.set_appearance_mode("Dark")
        # Themes: blue (default), dark-blue, green
        ctk.set_default_color_theme("dark-blue")

        # Configure the window
        self.title('Chat with Alibabot')

        self.minsize(50, 500)

        self.grid_rowconfigure((1), weight=1)  # configure grid system
        self.grid_columnconfigure((1), weight=1)

    # >------------------------------------------------------ END Root Config 

    # Set Dedfault Values ----------------------------------------------<

        self.mic = 1 # Change the mic
        self.recorder = PvRecorder(device_index=-self.mic, frame_length=512)

        self.audio = [] # on what the audio will be stored

        self.store_path = "audio.wav" # where the audio will be stored

        self.recording = False

        self.text_color = 'white'

        self.conversa = []
        self.bot_msg = []
    # >------------------------------------------- END Setting Dedfault Values

        def new_entry(entry):
            
            self.textbox.configure(state="normal") # allow to edit it                        
            self.textbox.insert("end", entry)
            self.textbox.configure(state="disabled", text_color=self.text_color) # not allow to edit it

        # Perguntas e Respostas Escritas -------------------------------------------------------<
        def resposta():
            #pega o que ta escrito na entrada
            entry_str = self.entry.get()

            #saves up the chat for the user side
            self.conversa.append({"role": "user", "content": entry_str})

            # Request da resposta, passa toda a conversa que já tiveram anteriormente também.
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversa, 
                stream=True # Passa a mesnagem separadamente.
            )

            new_entry("\nAlibabot: ")

            # pra cada resposta que for enviada, e pra cada "escolha" do gpt, pega apenas o conteudo que fica em "delta", que é onde ficam os conteudos do bot. 
            for chunk in completion:

                for choice in chunk.choices:
                    content = choice['delta'].get('content')
                    if content is not None:

                        # Append the messege to "bot msg", to save uo for the history later
                        self.bot_msg.append(content)

                        new_entry(str(content)) # Put the bot text on the textbox  s l o w l y

            #saves the chat of the bot side
            self.conversa.append({'role': 'assistant', 'content': str(self.bot_msg)})

            #Apaga o que tava na entrada anterior
            self.entry.delete(first_index=0, last_index=len(entry_str))
            

        def pergunta(x):

            #pega o que ta escrito na entrada
            entry_str = self.entry.get()
            
            # Monta a mensagem
            user = 'Usuário' + ': '

            new_entry(f'\n {user} {entry_str} \n')

            resposta()
        # >-------------------------------------------------- END Perguntas e Respostas Escritas

        # Image Config ------------------------------------------------------------------------------------------------<
        # Import Location of the code for images
        self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\img\\"

        # Images of the GUI
        self.config_icon = ImageTk.PhotoImage(Image.open(self.location + "config.png").resize((30,30), Image.ANTIALIAS))

        self.off_mic_icon = ImageTk.PhotoImage(Image.open(self.location + "mic.png").resize((30,30), Image.ANTIALIAS))

        self.on_mic_icon = ImageTk.PhotoImage(Image.open(self.location + "mic_on.png").resize((30,30), Image.ANTIALIAS))

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
                                         command=lambda: pergunta('x'))

        self.send_button.grid(row=2, column=2, pady=10, padx=10, sticky="nsew")


        self.mic_button = ctk.CTkButton(master=self, text="",
                                           width=100, image=self.off_mic_icon, 
                                           fg_color="#282424", hover_color="gray",
                                           command=self.toggle_recording)
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