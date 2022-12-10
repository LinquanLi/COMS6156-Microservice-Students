From python:3.9

RUN mkdir /app

ADD src/. /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

ENV FLASK_APP /app/src

WORKDIR
 /app/src

#CMD ["bash",  "-c", "flask run --host 0.0.0.0 --port 80"]
CMD ["bash", "-c", "python3 ./app/src/application.py"]
