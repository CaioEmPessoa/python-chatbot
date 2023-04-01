import openai
openai.api_key = "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"

print('Diga algo pro chatgpt: ')
ask = input('>> ')

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": ask}
    ]
)

print('chatgpt: ' + completion.choices[0].message.content)
