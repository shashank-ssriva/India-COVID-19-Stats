FROM python:3.7-alpine
COPY requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
WORKDIR /src
RUN pip install -r /src/requirements.txt
COPY app.py /src
COPY static /src/static
COPY templates /src/templates
CMD python /src/app.py
