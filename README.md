# (AI Revolution project) Платформа для работы с Chat GPT (backend)

Задача заключалась в разработке веб-сервиса, который объединит функциональность ChatGPT и будет специализирован для помощи в решении креативных задач. Данный сервис будет полезен для агентств, пиарщиков, контент-мейкеров, маркетологов и т.д.

<h2 align="center">
<p align="center">
<img src="https://img.shields.io/badge/Django-4.2.6-green">
<img src="https://img.shields.io/badge/DRF-3.14-green">
<img src="https://img.shields.io/badge/drfyasg-1.21-green">
<img src="https://img.shields.io/badge/djoser-2.2-green">
<img src="https://img.shields.io/badge/openai-3.2-red">
<img src="https://img.shields.io/badge/gunicorn-21.2-blue">
<img src="https://img.shields.io/badge/docker-3.9-blue">
</p>
</h2>

### Реализовано

- Кастомная модель пользователя
- Аутентификация через токены
- Подтверждение регистрации по электронной почте
- Аутентификация через социальные сети
- Работа с контекстом ChatGPT, передача результатов генерации ответа потоком
- Swagger документация
- Форматирования кода с использованием ruff

### Установка
Скопировать .env.exemple в .env, внести данные

#### Основные параметры:<br>
Раздел `Django development config` - настройки режима запуска<br>
Раздел `Django Superuser` - данные для создания суперпользователя
Раздел `Django Postgres Database Config` - настройки параметров базы данных
Раздел `Postgres container config` - переменные для Postgres Container
Раздел `Email Config` - настройки почтового сервиса
Раздел `Social Auth` - настройки для работы с социальными сетями

#### Команда для развертывания:
```
docker-compose up --build
```
Суперпользователь и данные, необходимые для работы системы, устанавливаются автоматически.