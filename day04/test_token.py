from app.services.token_service import count_text_tokens

text = "你好，我是一名前端工程师"

count = count_text_tokens(text)

print(count)
