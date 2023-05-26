API_KEY = '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'

MODEL = 'gpt-3.5-turbo'

INITIAL_TOKENS = 100000 # 100k
UPDATE_TOKENS = 10000 # 10k
MAX_TOKENS = 100000 # 100k

TIME_OF_TOKENS_UPDATE = 1 # 1 hour (in hours)


MESSAGES = {
    'error_request': 'Sorry, something went wrong. Please, refresh the page',
    'server_busy': 'Sorry, the server is currently busy. Please, try again later.',
    'limit_request': 'Sorry, you have exceeded the limit. Please, try again later.',
    'login_first': 'Please login first',
    'session_expired': 'Sorry, your session has expired. Please, logout and then login again',
}

