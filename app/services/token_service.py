import tiktoken
from app.constants import DEFAULT_MODEL


def estimate_tokens(prompt, model=DEFAULT_MODEL):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(prompt))
    return num_tokens
