init:
	@echo Initialize app
	@FLASK_APP=webapp

migrate:
	@echo Migrate database
	@flask db stamp 3d9a8939b562
	@flask db migrate -m "migrating tables"
	@flask db upgrade

fixture:
	@echo Add fixtures
	@python3 add_fixtures.py

run:	
	@echo Run app
	@export FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
