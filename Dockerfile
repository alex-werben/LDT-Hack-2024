FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /web_django/
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]