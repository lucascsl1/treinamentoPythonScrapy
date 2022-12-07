FROM python:3.12-rc-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "aplicacao_treinamento/spider_runner.py" ]
