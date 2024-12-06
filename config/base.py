from os import getenv
import tiktoken

token_encoding = tiktoken.get_encoding("cl100k_base")

# provide your openai secret key
OPENAI_API_KEY = getenv('OPENAI_API_KEY')
DATABASE_URL = getenv('DATABASE_URL')
#postgresql://postgres:postgres@localhost:9452/embeddings

#Redis Cinfiguration
REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')
REDIS_DB = getenv('REDIS_DB')
REDIS_EXPIRE_TIME = int(getenv('REDIS_EXPIRE_TIME', 3600))


# Categorization
# AIHUB_URL = ge`
# tenv('AIHUB_URL')
# AIHUB_API_KEY = getenv('AIHUB_API_KEY')
