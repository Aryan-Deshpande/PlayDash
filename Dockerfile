FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY . /app 

CMD ["flask", "run", "--host=localhost", "--port=80"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]