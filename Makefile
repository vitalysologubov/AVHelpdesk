init-app:
	@echo Initializing app
	@export FLASK_APP=webapp

run-app:	
	@echo Running app
	@export FLASK_APP=webapp && FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

create-migrations:
	@echo Creating migrations
	@export FLASK_APP=webapp && flask db stamp head && flask db migrate -m "migrating tables"

apply-migrations:
	@echo Applying migrations 
	@export FLASK_APP=webapp && flask db upgrade

add-fixtures-client:
	@echo Adding client
	@python3 add_fixtures.py -c client

add-fixtures-department:
	@echo Adding department
	@python3 add_fixtures.py -d department

add-fixtures-staff:
	@echo Adding staff
	@python3 add_fixtures.py -s staff

add-fixtures-ticket-status:
	@echo Adding ticket_status
	@python3 add_fixtures.py -ts ticket_status

add-fixtures-ticket-urgency:
	@echo Adding ticket_urgency
	@python3 add_fixtures.py -tu ticket_urgency

add-fixtures-ticket:
	@echo Adding ticket
	@python3 add_fixtures.py -t ticket

add-fixtures-message:
	@echo Adding message
	@python3 add_fixtures.py -m message

add-fixtures-all:
	@echo Adding fixtures
	@python3 add_fixtures.py -c client
	@python3 add_fixtures.py -d department
	@python3 add_fixtures.py -s staff
	@python3 add_fixtures.py -ts ticket_status
	@python3 add_fixtures.py -tu ticket_urgency
	@python3 add_fixtures.py -t ticket
	@python3 add_fixtures.py -m message
