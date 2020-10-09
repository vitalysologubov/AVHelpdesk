## About
AVHelpdesk - система обработки заявок с технологией учёта рабочего времени.

## Using 
* Flask
* Python 3.8


## Installation and tests
**Команды Makefile:**
- `init` - инициализация приложения;
- `migrate`- миграция базы данных;
- `fixture` - добавление фикстур в базу данных;
- `run` - запуск приложения.

**Celery**

обработка очереди: `celery -A tasks beat`

исполнитель:  `celery -A tasks worker --loglevel=INFO`
## Credentials

## License
