FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r ./requirements.txt

COPY . .

#CMD ["gunicorn", "foodgramm.wsgi:application", "--bind", "0:8000" ] 
CMD ["python3", "manage.py", "runserver", "0:5000"]