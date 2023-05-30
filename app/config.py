API_KEY = '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'

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

