## Приложение по согласованию карточки опломбировки счетчиков

Само приложение находится в ветке Celery

Настройка и запуск осуществляется через `docker-compose`
Управлениями пакетами и окружением через `poetry`

Основные сущности:
- Профиль пользователя (`UserProile`)
- Карточка (`Card`)
- Согласования (`Approval`)
