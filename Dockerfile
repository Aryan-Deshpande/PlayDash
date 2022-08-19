FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN \
python3 -m pip install -r requirements.txt --no-cache-dir
COPY . /app 

CMD ["flask", "run", "--host=localhost", "--port=80"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]