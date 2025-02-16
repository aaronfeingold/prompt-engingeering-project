import tiktoken
from app.constants import OPENAI_DEFAULT_MODEL


def estimate_tokens(prompt, model=OPENAI_DEFAULT_MODEL):
    # TODO: question if tiktoken can keep with the latest models
    encoding = tiktoken.encoding_for_model(model)
    # if you want to know the token count for a prompt
    # you find the length of the list of tokens
    return len(encoding.encode(prompt))
