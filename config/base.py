from os import getenv
import tiktoken

token_encoding = tiktoken.get_encoding("cl100k_base")

# provide your openai secret key
OPENAI_API_KEY = getenv('OPENAI_API_KEY')
DATABASE_URL = getenv('DATABASE_URL')


# Categorization
# AIHUB_URL = getenv('AIHUB_URL')
# AIHUB_API_KEY = getenv('AIHUB_API_KEY')
