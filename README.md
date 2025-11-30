# expert-demo-0.1.0

Демонстрационная версия экспертной системы для диагностики здоровья студентов.
Для установки:

0. Скачать проект.
1. Установить NodeJS, установить Python (если их нет).
2. Перейти в папку с фронтендом (`cd ./frontend`).
3. Установить зависимости `npm install`.
4. Запустить фронтенд-сервер командой `npm run dev`.
5. Перейти в папку с бекендом (`cd ./app`).
6. Установить зависимости `pip install -r requirements.txt` (или `pip install fastapi uvicorn pydantic sqlalchemy sqlalchemy-utils`).
7. Запустить бекенд-сервер командой `uvicorn main:app --reload --port 8000`.
