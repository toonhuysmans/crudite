FROM python:3.9

RUN mkdir /app
WORKDIR /app

ADD requirements.in /app/requirements.in

RUN pip install pip-tools
RUN pip-compile requirements.in
RUN pip install --upgrade -r requirements.txt

EXPOSE 8000

#COPY backend /app
RUN rm -rf /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--log-level", "debug"]