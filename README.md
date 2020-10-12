## About
AVHelpdesk - система обработки заявок с технологией учёта рабочего времени.


## Using 
* Flask 1.1.2
* Python 3.8



**Celery**

обработка очереди: `celery -A tasks beat`

**Команды Makefile:**

- `init-app` - инициализация приложения;
- `run-app` - запуск приложения;
- `create-migrations`- создание миграции базы данных;
- `apply-migrations` - применение миграции базы данных;
- `add-fixtures` - добавление фикстур в базу данных.


обработка очереди: `celery -A tasks beat`
исполнитель:  `celery -A tasks worker --loglevel=INFO`

## Credentials

## License
