import g4f
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
g4f.debug.logging = True


def send_gpt_request(message_list, config):

    if config['model'] == 'GPT-35':
        model = g4f.models.gpt_35_long
    else:
        model = g4f.models.gpt_4

    try:
        response = g4f.ChatCompletion.create(
            model=model,
            temperature=config['temperature'],
            max_tokens=config['tokenLimit'],
            messages=[
                {"role": "system",
                 "content": f"{config['prompt']}"},
            ] + message_list)

        assistant_response = response

    except Exception as e:
        logger.error(f"Failed to send request to GPT-3.5: {e}")
        return "Sorry, I'm having trouble understanding you."
    return assistant_response

    # try:
    #     openai.api_key = settings.APIKEY
    #     gpt3_response = openai.ChatCompletion.create(
    #         model=f"{config['model']}",
    #         # Управляет степенью случайности в ответах модели
    #         temperature=config['temperature'],
    #         # Ограничение на количество токенов в ответе
    #         max_tokens=config['tokenLimit'],
    #         # Ограничение на размер беседы
    #         # total_tokens=config['maxLength'],
    #         messages=[
    #             {"role": "system",
    #              "content": f"{config['prompt']}"},
    #         ] + message_list
    #     )

    #     assistant_response = gpt3_response["choices"][0]["message"]["content"].strip(
    #     )

    #     logger.info(f"GPT-3 response: {gpt3_response['usage']}")

    # except Exception as e:
    #     logger.error(f"Failed to send request to GPT-3.5: {e}")
    #     return "Sorry, I'm having trouble understanding you."
    # return assistant_response
