@echo off
.\venv3\bin\python.exe -m pip install flask python-dotenv requests joblib pandas==2.2.3 langchain_groq
if errorlevel 1 goto end
.\venv3\bin\python.exe app.py
:end
