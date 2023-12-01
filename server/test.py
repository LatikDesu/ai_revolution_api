from openai import OpenAI
import httpx
from src.settings import APIKEY, PROXY_URL

proxies = {
    "all://": PROXY_URL,
}

client = OpenAI(
    api_key=APIKEY,
    http_client=httpx.Client(proxies=proxies),
)


stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "расскажи о белых медведях"}],
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
