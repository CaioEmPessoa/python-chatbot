import sys
import openai


sys.path.append(
    'D:\Área de Trabalho do hd\estudos\programação\python\zPython-ChatGPT')
from View import PrimeiraTelaView as PTV


openai.api_key = "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"

def responder():
    entry = PTV.get_entry
    print(entry)

    # pega oq ta escrito na textbox
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": entry}
        ]
    )

    print(str('Chatgpt: ' + completion.choices[0].message.content))


