FROM python:3.11

WORKDIR /app

COPY django-web-llm/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

COPY ./docker-files-llm/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
