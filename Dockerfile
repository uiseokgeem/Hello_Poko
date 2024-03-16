# pull official base image
FROM python:3.10-slim

# Install gcc and python3-dev
RUN apt-get update && apt-get install -y gcc python3-dev

# set work directory
WORKDIR /usr/src/app

# set enviroment variabels
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
