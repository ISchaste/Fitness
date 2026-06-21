# Фитнес Центр Часть I

REST API на базе FastAPI.

## Описание

Проект реализует систему управления клиентами и тренерами фитнес-центра.

Данные хранятся в памяти. После перезапуска сервера данные сбрасываются.

---

## Технологии

- Python
- FastAPI
- Uvicorn
- Pydantic

---

## Запуск

```
pip install -r requirements.txt
uvicorn app.main:app --reload
