@echo off
start cmd /k "python url_flask.py"
start cmd /k "uvicorn url_api:app --reload --port 8000"
pause