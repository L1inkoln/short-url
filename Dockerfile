FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

RUN chmod +x app/entrypoint.sh

ENTRYPOINT ["./app/entrypoint.sh"]
