# collect_money
## Описание
Сервис, позволяющий создавать Сбор (Collect) на определенную сумму.
К каждому сбору можно сделать Платёж (Payment).
После создания платежа на почту "отправляется" письмо о платеже.
После создания сбора на почту "отправляется" письмо о сборе.
При достижении целевого значачения сбора на почту "отправляется" письмо о достижении цели.
Имитация отправки письма через Celery task, и создания файла в папке EMAIL_FILE_PATH.
Реализовано кэширование GET запросов в Redis, с актуализацией при изменении данных.

Полная документация к API доступна по эндпоинтам http://localhost:8000/api/schema/swagger-ui/ и http://localhost:8000/api/schema/redoc/

### Cтэк технологий:
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Celery
- Redis

#### Запуск через Docker Compose локально (рекомендуемый способ запуска)
1. Создайте файл `.env` и заполните его своими данными. Файл `.env` должен находиться в корневой папке проекта. Если вы решите не создавать свой `.env` файл - в проекте предусмотрен файл `.env.example`, обеспечивающий переменные для базовой работы на локальном уровне.
2. Собрерите и запустите докер-контейнеры через Docker Compose:
```bash
docker compose up -d --build
```
3. Загрузка данных:
```bash
python manage.py import_collects_csv collects.csv
python manage.py import_payments_csv payments.csv
```
CSV файлы должны быть вида (без заголовка):
collects.csv
```
id,name,cause,description,goal_amount,current_amount,bakers_count,image,close_date,author_id
Например:
8,Разное,msc,Сбор средств на различные нужды,40000,35000,90,,2024-09-25,1
```
payments.csv
```
id,amount,date,collect_id,user_id
Например:
1,1000,2024-09-25,1,1
```
