FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ .

CMD ["gunicorn", "foodgramm.wsgi:application", "--bind", "0:8000" ] 
# CMD ["python3", "manage.py", "runserver", "0:5000"]