import openai

API_Key = 'sk-'
openai.api_key = API_Key

#MODELS
def chatgpt(request):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=request
    )
    response = chat.choices[0].message.content
    return response
