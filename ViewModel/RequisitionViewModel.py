import sys
import openai


sys.path.append(
    'D:\Área de Trabalho do hd\estudos\programação\python\zPython-ChatGPT')
from View import PrimeiraTelaView as PTV


openai.api_key = "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"

instancia = PTV.App()

def resposta(entry):
    get_entry = entry

    # pega oq ta escrito na textbox
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": get_entry}
        ]
    )

    PTV.instancia.textbox("0.0", ('chatgpt: ' + completion.choices[0].message.content))

