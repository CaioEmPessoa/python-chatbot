import openai

def resposta(app):
    openai.api_key = app.api_key
    
    #pega o que ta escrito na entrada
    entry_str = app.entry.get()

    #saves up the chat for the user side
    app.conversa.append({"role": "user", "content": entry_str})

    # Request da resposta, passa toda a conversa que já tiveram anteriormente também.
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=app.conversa, 
        stream=True # Passa a mesnagem separadamente.
    )

    app.new_entry("\nAlibabot: ")

    # pra cada resposta que for enviada, e pra cada "escolha" do gpt, pega apenas o conteudo que fica em "delta", que é onde ficam os conteudos do bot. 
    for chunk in completion:

        for choice in chunk.choices:
            content = choice['delta'].get('content')
            if content is not None:

                # Append the messege to "bot msg", to save uo for the history later
                app.bot_msg.append(content)

                app.new_entry(str(content)) # Put the bot text on the textbox  s l o w l y

    #saves the chat of the bot side
    app.conversa.append({'role': 'assistant', 'content': str(app.bot_msg)})

    #Apaga o que tava na entrada anterior
    app.entry.delete(first_index=0, last_index=len(entry_str))

def pergunta(app):
    openai.api_key = app.api_key

    #pega o que ta escrito na entrada
    entry_str = app.entry.get()
    
    # Monta a mensagem
    user = app.user + ': '

    app.new_entry(f'\n {user} {entry_str} \n')

    resposta(app)
