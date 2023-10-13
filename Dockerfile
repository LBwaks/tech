# selecting image to be used
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create working directory
WORKDIR /tech

# get requirements
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install  --upgrade pip

# insatll packages
RUN pip install  -r requirements.txt

# copy everything to the current working directory
COPY . .

CMD ["celery -A Technical worker --loglevel=info","python","manage.py","runserver","0.0.0.0:8000"]

# EXPOSE 8000