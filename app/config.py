OPENAI_API_KEY = 'sk-'

GOOGLE_API_KEY = ""
GOOGLE_CLIENT_ID = "644921762385-7mht08oouifcgp3cha7v6m0d6r9ls2qd.apps.googleusercontent.com"
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

