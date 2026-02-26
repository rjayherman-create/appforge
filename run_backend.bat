@echo off
cd backend
set PYTHONPATH=%cd%
uvicorn appforge.main:app --reload
