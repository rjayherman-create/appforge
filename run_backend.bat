@echo off
cd backend
set PYTHONPATH=%cd%
uvicorn app.main:app --reload
