import json
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


def send_gpt_request(message_list, config):

    try:
        response = client.chat.completions.create(
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['maxTokens'],
            top_p=config['topP'],
            frequency_penalty=config['frequencyPenalty'],
            presence_penalty=config['presencePenalty'],
            stream=True,
            messages=[
                {"role": "system",
                    "content": f"{config['prompt']}",
                    "role": "user",
                    "content": f"The response should be returned in markdown formatting."},
            ] + message_list,
        )

        if response:
            return response

    except Exception as e:
        return "Извините, мои нейроны не понимают вас. Пожалуйста, попробуйте еще раз."

    return "Извините, мои нейроны не понимают вас. Пожалуйста, попробуйте еще раз."


def event_stream(generator):
    for chunk in generator:
        if chunk.choices[0].delta.content is not None:
            yield f'data: {chunk.choices[0].delta.content}\n\n'


async def send_gpt_request_async(message_list, config):
    response = client.chat.completions.create(
        model=config['model'],
        temperature=config['temperature'],
        max_tokens=config['maxTokens'],
        top_p=config['topP'],
        frequency_penalty=config['frequencyPenalty'],
        presence_penalty=config['presencePenalty'],
        stream=True,
        messages=[
            {"role": "system",
             "content": f"{config['prompt']}",
             "role": "user",
             "content": f"The response should be returned in markdown formatting."},
        ] + message_list,
    )
    for chunk in response:

        chunk_parsed = {
            "role": "assistant",
            "content": chunk.choices[0].delta.content,
            "finish_reason": chunk.choices[0].finish_reason,
        }
        yield f"data: {json.dumps(chunk_parsed)}\n\n"
