OPENAI_API_KEY = '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'

GOOGLE_API_KEY = "AIzaSyDpILKGfpUi7vOhZMm63z6t5G7ZiCLeSGs"
GOOGLE_CLIENT_ID = "831953260452-6m547qjriitpmph658d0533b1v922u0j.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

MODEL = 'gpt-3.5-turbo'

INITIAL_TOKENS = 100000 # 100k
UPDATE_TOKENS = 10000 # 10k
MAX_UPDATE_TOKENS = 100000 # 100k

TIME_OF_TOKENS_UPDATE = 1 # 1 hour (in hours)


MESSAGES = {
    'error_request': 'Sorry, something went wrong. Please, refresh the page',
    'server_busy': 'Sorry, the server is currently busy. Please, try again later.',
    'limit_request': 'Sorry, your token is reached the limit. Please, check your profile and try again later.',
    'login_first': 'Please login first',
    'session_expired': 'Sorry, your session has expired. Please, logout and then login again',
}

