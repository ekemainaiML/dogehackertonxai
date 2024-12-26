#
FROM python:3.11

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./authapi /code/app

#
CMD ["fastapi", "run", "app/main.py", "--port", "80"]