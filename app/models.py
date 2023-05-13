import openai

API_Key = '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'
openai.api_key = API_Key

#MODELS
def chatgpt(request):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=request
    )
    response = chat.choices[0].message.content
    return response
