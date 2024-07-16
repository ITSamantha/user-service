#!/bin/bash

alembic revision --autogenerate
alembic upgrade head

PYTHONPATH=/app python src/core/database/seeders/database_seeder.py

uvicorn src.main:app --host 0.0.0.0 --port 9000