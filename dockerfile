FROM python:3.10

WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN pip install loguru
RUN pip install --upgrade mailru-im-bot

# COPY . .
COPY my_bot .

# CMD ["python", "my_bot", "my_bot.py"]
CMD ["python", "my_bot.py"]