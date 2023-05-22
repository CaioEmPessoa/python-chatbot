import customtkinter as ctk
from pvrecorder import PvRecorder

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
            app.mic = self.device[0]
            app.recorder = PvRecorder(device_index=-int(app.mic), frame_length=512)


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
