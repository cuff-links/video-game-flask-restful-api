FROM python:3.9-slim-buster

RUN pip3 install pipenv

ENV PROJECT_DIR /usr/src/video-game-api-tc

WORKDIR ${PROJECT_DIR}

COPY Pipfile .
COPY Pipfile.lock .
COPY . .

RUN pipenv install --deploy --ignore-pipfile

EXPOSE 5050

CMD ["pipenv", "run", "python", "api.py"]