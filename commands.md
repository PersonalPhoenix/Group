# Подсказки по работе

### Запуск сервера

```uvicorn <module>:<attributes>```<br>
<br>
Например:<br>
<br>
```uvicorn app.main:app```<br>
<br>
### Запуск миграций

```alembic revision --autogenerate -m 'message'```<br>
<br>
Например:<br>
<br>
```alembic revision --autogenerate -m 'init'```<br>
<br>
### Запуск тестов ассинхронно

```pytest --asyncio-mode=auto```

#### Показать покрытие тестами

```pytest --cov=app --cov-report=term-missing```