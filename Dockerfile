FROM python:3.10.7-alpine
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -e .

CMD [ "python", "qbit_ci" ]
