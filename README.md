# praktikum_new_diplom

### <a name="Описание_проекта">Описание</a>
Foodgram реализован для публикации рецептов. Авторизованные пользователи могут 
подписываться на понравившихся авторов, добавлять рецепты в избранное, 
в покупки, скачать список покупок ингредиентов для добавленных в покупки 
рецептов.

Проект запущен и доступен по ссылке http://158.160.4.3/

В проекте применяется 
- **Django REST Framework**, 

- **Python 3**,
- **PostgreSQL**,
- **Docker**, 
- **Nginx**,
- **Gunicorn**,
- **Git**, 
- Аутентификация реализована с помощью **токена**.

### Инструкция по установке и запуску проекта
Склонировать репозиторий на локальную машину:
git clone https://github.com/Regina-Ibragimova/foodgram-project-react.git
На удаленном сервере:
скопируйте файлы docker-compose.yml, docker-compose.prod.yml и nginx.conf из директории infra на сервер;

в директории infra/ создайте .env на основе .env.template

DB_ENGINE - указать СУБД 
DB_NAME - имя базы данных
POSTGRES_USER - логин пользователя базы данных PostgreSQL
POSTGRES_PASSWORD - пароль пользователя базы данных PostgreSQL
DB_HOST - IP адрес сервера базы данных PostgreSQL
DB_PORT - порт сервера базы данных PostgreSQL

DJANGO_SECRET_KEY - секретный ключ
DJANGO_DEBUG - режим работы сервера
для развёртывания с github action добавьте в Secrets GitHub переменные окружения:
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>
USER=<username для подключения к серверу>
HOST=<IP сервера>
SSH_KEY=< SSH ключ
TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
на сервере запустите контейнеры через docker-compose:
sudo docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
только при первом развёртывании проекта на сервере:

соберите статические файлы:
sudo docker-compose exec web python manage.py collectstatic --noinput
примените миграции:
sudo docker-compose exec web python manage.py migrate --noinput
загрузите ингридиенты в базу данных (необязательно):
sudo docker-compose exec web python manage.py filling -a `приложение` -m `Модель` -f файл из директории static/data `.csv`
cоздать суперпользователя Django:
sudo docker-compose exec web python manage.py createsuperuser


### Автор
Регина Ибрагимова