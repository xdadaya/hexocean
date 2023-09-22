FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY entrypoint.sh /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/
