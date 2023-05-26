import customtkinter as ctk
from pvrecorder import PvRecorder
import os

#janela de config
class ConfigWindow(ctk.CTkToplevel):
        
    # Read save_file
    def read_save(self, app):
        if os.path.isfile('save.txt'):
            with open('save.txt', 'r') as f:
                config_save = f.read()
                config_save = config_save.split(',')
                app.config_list = [x for x in config_save if x.strip()]
            
            print("Last Config: " + str(app.config_list))

            self.temas_box.set(app.config_list[0])
            self.font_box.set(app.config_list[2])
            self.devices_box.set(app.config_list[3])

    def apply(self, app):

        lambda: self.read_save(app)

        # Pega o valor escolhido nas caixas
        self.fonte = self.font_box.get()
        self.sans = self.checkbox.get()
        self.tema = self.temas_box.get()
        self.device = self.devices_box.get()

        # Salva os valores escolhidos *na lista*
        print(app.config_list)
        app.config_list[0:4] = [self.tema, self.sans, self.fonte, self.device]
        print(app.config_list)
        
        # Escreve essa lista em um arquivo de texto
        with open('save.txt', 'w') as f:
            for config in app.config_list:
                f.write(config + ',')

        # Altera o valor que aparecerá como padrão na proxima
        self.font_box.set(self.fonte)
        self.temas_box.set(self.tema)

        # Troca a fonte
        app.change_font(self.sans)
        app.change_font(self.fonte)

        # Troca o tema
        app.change_theme(self.tema)

        # Troca o dispositivo
        app.mic = self.device[0]
        app.recorder = PvRecorder(device_index=-int(app.mic), frame_length=512)

        # Fecha a aba de config
        app.config_window.destroy()

    def __init__(self, app):
        super().__init__()

        # Set Configs for window
        self.title('Config Alibabot')

        self.minsize(300, 300)
        self.maxsize(450, 300)


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

        # Caixas de escolha------------------------------------<
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

        self.apply_button = ctk.CTkButton(master=self, text="Aplicar.", width=5, command=lambda: self.apply(app))
        self.apply_button.grid(row=5, column=1, columnspan=3, sticky="W", pady=10)

        self.read_save(app)

