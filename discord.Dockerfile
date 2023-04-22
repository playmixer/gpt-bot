FROM python:3.11-slim-buster

WORKDIR /src

COPY requirements_discord.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY classes classes
COPY core core
COPY discord_bot.py discord_bot.py

CMD [ "python", "discord_bot.py"]