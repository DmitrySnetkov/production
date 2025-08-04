FROM python:3.10
# FROM python:3.13.2
# FROM python:3.9

WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN pip install loguru
RUN pip install --upgrade mailru-im-bot
RUN pip install opencv-python
RUN pip install schedule
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# RUN pip install selenium

# COPY . .
COPY my_bot .

# CMD ["python", "my_bot", "my_bot.py"]
CMD ["python", "my_bot.py"]