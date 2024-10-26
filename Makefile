migrate:
	alembic upgrade head

create-migration:
	alembic revision --autogenerate -m '${msg}'