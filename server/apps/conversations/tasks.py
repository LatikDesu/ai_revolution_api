import openai
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task
def send_gpt_request(message_list, system_prompt):
    try:
        openai.api_key = settings.APIKEY
        gpt3_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system",
                 "content": f"{system_prompt}"},
            ] + message_list
        )

        assistant_response = gpt3_response["choices"][0]["message"]["content"].strip(
        )

    except Exception as e:
        logger.error(f"Failed to send request to GPT-3.5: {e}")
        return "Sorry, I'm having trouble understanding you."
    return assistant_response


@shared_task
def generate_title_request(message_list):
    try:
        openai.api_key = settings.APIKEY
        gpt3_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system",
                 "content": "Summarize and make a very short meaningful title under 24 characters"},
            ] + message_list
        )
        response = gpt3_response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.error(f"Failed to send request to GPT-3.5: {e}")
        return "Problematic title with error."
    return response
