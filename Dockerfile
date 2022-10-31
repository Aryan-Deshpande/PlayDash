FROM python:3.10-slim as step1

WORKDIR /app

COPY . .

RUN \
python3 -m pip install -r requirements.txt --no-cache-dir
COPY . /app 

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app", "timeout 600", "workers 2"]