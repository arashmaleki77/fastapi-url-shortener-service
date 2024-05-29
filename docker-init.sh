#!/bin/sh

python create_db.py

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 5000
