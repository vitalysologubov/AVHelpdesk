## About
AVHelpdesk - система обработки заявок, поступающих от клиентов по электронной почте.


## Using
* Python 3.8
* Flask 1.1.2
* celery 5.0.0


**Makefile:**

- `init-app` - инициализация приложения;
- `run-app` - запуск приложения;
- `create-migrations`- создание миграции базы данных;
- `apply-migrations` - применение миграции базы данных;
- `add-fixtures-client` - добавление клиентов;
- `add-fixtures-department` - добавление отделов;
- `add-fixtures-staff` - добавление сотрудников;
- `add-fixtures-ticket-status` - добавление статусов заявок;
- `add-fixtures-ticket-urgency` - добавление срочности заявок;
- `add-fixtures-ticket` - добавление заявок;
- `add-fixtures-message` - добавление содержания писем;
- `add-fixtures-all` - добавление всех фикстур.


**Celery**

- `celery -A tasks beat` - обработка очереди;
- `celery -A tasks worker --loglevel=INFO` - исполнитель.

## Credentials


## License
