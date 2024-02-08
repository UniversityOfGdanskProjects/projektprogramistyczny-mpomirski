
FROM python:3.10-alpine3.19
WORKDIR /app
COPY . .
RUN apk add openssl && \
pip install -r requirements.txt
CMD export SECRET_KEY=$(openssl rand -hex 32); python3 app/main.py
EXPOSE 3001
