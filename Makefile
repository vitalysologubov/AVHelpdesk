init-app:
	@echo Initializing app
	@export FLASK_APP=webapp

run-app:	
	@echo Runing app
	@export FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

create-migrations:
	@echo Creating migrations
	@flask db stamp head
	@flask db migrate -m "migrating tables"

apply-migrations:
	@echo Applying migrations 
	@flask db upgrade

add-fixtures:
	@echo Adding fixtures
	@python3 add_fixtures.py