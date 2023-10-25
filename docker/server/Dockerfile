FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

RUN python3 -m venv /opt/venv/

CMD ["mkdir", "app/server/"]

WORKDIR /app/server/
COPY ./server/ .

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r /app/server/requirements.txt
    
RUN useradd -m -d /app/server -s /bin/bash app \
    && chown -R app:app /app/server  && chmod +x /app/server/scripts/*

USER app

CMD ["/app/server/scripts/entrypoint-dev.sh"]