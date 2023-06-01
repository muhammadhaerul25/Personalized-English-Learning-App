import openai
import tiktoken

from session import session, tokens_used_dict, tokens_had_dict
from database import User
from config import OPENAI_API_KEY, MODEL, MESSAGES


openai.api_key = OPENAI_API_KEY


#MODELS
def chatgpt(request):
    if is_enough_tokens(request):
        try:
            chat = openai.ChatCompletion.create(
                model=MODEL,
                messages=request
            )
            response = chat.choices[0].message.content
            update_tokens()
            return response
        except openai.error.OpenAIError as e:
            if "limit exceeded" in str(e):
                return MESSAGES["server_busy"]
            else:
                return MESSAGES["error_request"]
    else:
       return MESSAGES["limit_request"]


#TOKENS
def num_tokens_from_messages(messages, model=MODEL):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  
  num_tokens = 0
  for message in messages:
    num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
    for key, value in message.items():
      num_tokens += len(encoding.encode(value))
      if key == "name":  # if there's a name, the role is omitted
        num_tokens += -1  # role is always required and always 1 token
  num_tokens += 2  # every reply is primed with <im_start>assistant
  return num_tokens


def count_tokens(messages):
   user_id = session.get("user")
   num_tokens = num_tokens_from_messages(messages)
   tokens_had_dict[user_id] -= num_tokens
   tokens_used_dict[user_id] += num_tokens
   


def is_enough_tokens(messages):
    count_tokens(messages)
    user_id = session.get("user")
    if tokens_had_dict[user_id] >= 0:
        return True
    else:
        return False


def update_tokens():
    user_id = session.get("user")
    User.update_tokens_had(user_id, tokens_had_dict[user_id])
    User.update_tokens_used(user_id, tokens_used_dict[user_id])



