import openai
from config import MESSAGES, LIMIT_TOKENS

API_Key = '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'
openai.api_key = API_Key

#MODELS
def chatgpt(request):
    request_tokens = count_request_tokens(request)
    if request_tokens > LIMIT_TOKENS:
        return MESSAGES["limit_request"]
    else:
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request
            )
            response = chat.choices[0].message.content
            return response
        except openai.error.OpenAIError as e:
            if "limit exceeded" in str(e):
                return MESSAGES["server_busy"]
            else:
                return MESSAGES["error_request"]


#TOKENS
def count_tokens(text):
    words_lenght = len(text.split())
    tokens = words_lenght * 1.33  #1.33 is the average number of tokens per word in English
    return tokens
    

def count_request_tokens(request):
    total_tokens = 0
    for message in request:
        content = message.get("content", "")
        total_tokens += count_tokens(content)
    return total_tokens