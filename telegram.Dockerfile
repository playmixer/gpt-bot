FROM python:3.11-slim-buster

WORKDIR /src

COPY requirements_telegram.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY classes classes
COPY core core
COPY telegram_bot.py telegram_bot.py

CMD [ "python", "telegram_bot.py"]