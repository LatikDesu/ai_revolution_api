from datetime import datetime, timezone
import openai
from django.conf import settings

openai.api_key = settings.APIKEY


def time_since(dt):
    """
    Returns string representing "time since" e.g.
    """
    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    days = int(hours // 24)
    months = int(days // 30)
    years = int(days // 365)

    if years > 0:
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif months > 0:
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif days > 0:
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif hours > 0:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return f"{int(seconds)} second{'s' if seconds > 1 else ''} ago"


def send_gpt_request(message_list, system_prompt):

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{system_prompt}"},
            ] + message_list,
        )
        return res["choices"][0]["message"]["content"]
    except openai.error.APIError as e:
        raise ValueError(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        raise ValueError(f"Failed to connect to OpenAI API: {e}")
    except openai.error.RateLimitError as e:
        raise ValueError(f"OpenAI API request exceeded rate limit: {e}")
