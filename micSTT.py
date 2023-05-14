import openai
import wave, struct
import threading
from queue import Queue
from pvrecorder import PvRecorder


openai.api_key = "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"


def speech_text(app):
    print("Traduzindo... ")
    audio_file = open("audio.wav", "rb") # Lê o "audio.wav"
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript.text)
    app.entry.insert(0, str(transcript.text))


def toggle_recording(app):

    if not app.recording: # Se nao está gravando
        app.recording = True # Esta gravando

        # Muda o botão pro vermelho
        app.mic_button.configure(image=app.on_mic_icon)

        # Começa a thread de gravar
        record_audio_thread = threading.Thread(target=lambda: record_audio(app))
        record_audio_thread.start()
        
    # Se esta gravando
    else:
        app.recording = False  # Não está gravando

        # Muda o ícone pro normal
        app.mic_button.configure(image=app.off_mic_icon)

        # Para de gravar
        app.recorder.stop()

        # salva o arquivo
        with wave.open("audio.wav", 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(app.audio), *app.audio))

        app.audio = []
        speech_text(app) # chama pra traduzir

def record_audio(app):

    # Começa a gravar realmente
    app.recorder.start()
    #Enquanto grava, manda cada frame dela pra lista "audio"
    while app.recording:
        frame = app.recorder.read()
        app.audio.extend(frame)

    app.recorder.stop()

