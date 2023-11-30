import g4f
from celery.utils.log import get_task_logger

providers = [
    # GPT-3.5
    g4f.Provider.FreeGpt,
    g4f.Provider.ChatForAi,
    g4f.Provider.MyShell,
    g4f.Provider.ChatgptAi,
    g4f.Provider.ChatBase,
    # GPT-4
    g4f.Provider.Bing,
]

logger = get_task_logger(__name__)
g4f.debug.logging = True


def send_gpt_request(message_list, config, stream=True):

    if config['model'] == 'GPT-35':
        model = g4f.models.gpt_35_long
    else:
        model = g4f.models.gpt_4

    # for items in providers:
    try:
        response = g4f.ChatCompletion.create(
            model=model,
            # provider=items,
            max_tokens=config['tokenLimit'],
            temperature=config['temperature'],
            messages=[
                {"role": "system",
                    "content": f"{config['prompt']}",
                    "role": "user",
                    "content": f"The response should be returned in markdown formatting."},
            ] + message_list,
            stream=stream,)

        if response:
            return response

    except Exception as e:
        logger.error(f"Failed to send request to GPT-3.5: {e}")
        # continue

    return "Извините, мои нейроны не понимают вас. Пожалуйста, попробуйте еще раз."


def event_stream(generator):
    for chunk in generator:
        yield f"response: {chunk}\n\n"

