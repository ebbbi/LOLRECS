FROM python:3.10

EXPOSE 80

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./server.py /code/server.py

ENV RIOT_API_KEY RGAPI-9f4aec3a-1cf1-4b6c-8079-37bab48ac7b7

ENV DB_URL {DB_URL}

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python", "server.py"]
