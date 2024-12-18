
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["pipenv", "run", "python", "main.py"]
