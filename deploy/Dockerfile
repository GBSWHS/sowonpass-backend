FROM python:3.11-alpine3.17

COPY . /app/

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "sowonpass_backend"]
