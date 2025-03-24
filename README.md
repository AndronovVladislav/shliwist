# Отчёт

## ✅ 1.1 Аутентификация и контроль доступа

- Используется JWT-аутентификация (библиотека `pyjwt`)
- Реализована схема `access_token + refresh_token`
- RSA-ключи хранятся в `src/certs/`
- Токены проверяются через Depends в `FastAPI`

**Папка**:  
[src/routes/auth](src/routes/auth)

---

## ✅ 1.2 HTTP API (CRUD)

- Эндпоинты `/wishlist`, включая:
  - `GET /` — получить вишлист
  - `POST /` — создать элемент
  - `PATCH /{id}` — обновить
  - `DELETE /{id}` — удалить
  - `POST /{id}/assign` — назначить дарителя

**Файл**:
[src/routes/wishlist.py](src/routes/wishlist.py)

---

## ✅ 1.3 Unit и функциональные тесты

- `pytest`, `httpx`, `pytest-asyncio`
- Отдельные юнит-тесты сервисов и функциональные тесты API
- Используются фикстуры и моковые зависимости

**Папка**:  
[src/tests](src/tests)

---

## ✅ 1.4 Используется внешняя PostgreSQL БД

- Конфигурация в `docker-compose` (для удобства разработки и тестирования) и `k8s/postgres/`
- Подключение через `asyncpg` + `sqlalchemy`

---

## ✅ 1.5 Схема создаётся при запуске

- Используется инструмент Alembic для автогенерации миграций
- При запуске образа (в Dockerfile) выполняется команда `alembic upgrade head`, накатывающая все имеющиеся миграции 
---

## ✅ 1.6 Проверка соответствия моделей схеме БД

- Среди тестов, запускаемых в PR через Github Actions, есть проверка на валидность миграций:
  - применяются миграции
  - с помощью команды `alembic check` проверяется соответствие состояние ORM-моделей схеме БД после этих миграций
  - тест падает, если миграции на изменение ORM-моделей не были написаны. 
- Реализовано через workflow GitHub Actions
---

## ✅ 2.1 Логирование

- Конфигурация через [src/logging.yml](src/logging.yml)
- Логи пишутся в stdout
- Форматируемый вывод (дата, уровень, модуль)
- Логи Graphana, Postgres и с других подов также собираются в Grafana

---

## ✅ 2.2 Экспонирование метрик

- Используется `prometheus-fastapi-instrumentator`
- Метрики доступны по `/metrics`
- Kubernetes аннотации включают `prometheus.io/scrape: "true"`

---

## ✅ 2.3 Запуск в Kubernetes

- Приложение, БД, сервисы, ingress — всё описано в [k8s](k8s)
- Используется кластер `k3s`
- Балансировка и маршрутизация через Traefik

---

## ✅ 2.4 Сбор логов в Kubernetes

- Установлен стек: `Loki + Promtail + Grafana`
- Grafana доступна по адресу `/grafana`
- Метки `namespace`, `pod` и `app` настроены

---

## ✅ 3.1 CI/CD

- GitHub Actions:
  - Сборка Docker-образа
  - Публикация в GHCR
  - Применение манифестов в кластер
  - `kubectl rollout restart` при каждом пуше

---

## ✅ 3.2 Swagger-документация

- FastAPI автоматически публикует Swagger по `/docs`
- Доступен извне через Ingress

---

# Отчёт

## ✅ 1.1 Аутентификация и контроль доступа

- Используется JWT-аутентификация (библиотека `pyjwt`)
- Реализована схема `access_token + refresh_token`
- RSA-ключи хранятся в `src/certs/`
- Токены проверяются через Depends в `FastAPI`

**Папка**:  
[src/routes/auth](src/routes/auth)

---

## ✅ 1.2 HTTP API (CRUD)

- Эндпоинты `/wishlist`, включая:
  - `GET /` — получить вишлист
  - `POST /` — создать элемент
  - `PATCH /{id}` — обновить
  - `DELETE /{id}` — удалить
  - `POST /{id}/assign` — назначить дарителя

**Файл**:
[src/routes/wishlist.py](src/routes/wishlist.py)

---

## ✅ 1.3 Unit и функциональные тесты

- `pytest`, `httpx`, `pytest-asyncio`
- Отдельные юнит-тесты сервисов и функциональные тесты API
- Используются фикстуры и моковые зависимости

**Папка**:  
[src/tests](src/tests)

---

## ✅ 1.4 Используется внешняя PostgreSQL БД

- Конфигурация в `docker-compose` (для удобства разработки и тестирования) и `k8s/postgres/`
- Подключение через `asyncpg` + `sqlalchemy`

---

## ✅ 1.5 Схема создаётся при запуске

- Используется инструмент Alembic для автогенерации миграций
- При запуске образа (в Dockerfile) выполняется команда `alembic upgrade head`, накатывающая все имеющиеся миграции 
---

## ✅ 1.6 Проверка соответствия моделей схеме БД

- Среди тестов, запускаемых в PR через Github Actions, есть проверка на валидность миграций:
  - применяются миграции
  - с помощью команды `alembic check` проверяется соответствие состояние ORM-моделей схеме БД после этих миграций
  - тест падает, если миграции на изменение ORM-моделей не были написаны. 
- Реализовано через workflow GitHub Actions
---

## ✅ 2.1 Логирование

- Конфигурация через [src/logging.yml](src/logging.yml)
- Логи пишутся в stdout
- Форматируемый вывод (дата, уровень, модуль)
- Логи Graphana, Postgres и с других подов также собираются в Grafana

---

## ✅ 2.2 Экспонирование метрик

- Используется `prometheus-fastapi-instrumentator`
- Метрики доступны по `/metrics`
- Kubernetes аннотации включают `prometheus.io/scrape: "true"`

---

## ✅ 2.3 Запуск в Kubernetes

- Приложение, БД, сервисы, ingress — всё описано в [k8s](k8s)
- Используется кластер `k3s`
- Балансировка и маршрутизация через Traefik

---

## ✅ 2.4 Сбор логов в Kubernetes

- Установлен стек: `Loki + Promtail + Grafana`
- Grafana доступна по адресу `/grafana`
- Метки `namespace`, `pod` и `app` настроены

---

## ✅ 3.1 CI/CD

- GitHub Actions:
  - Сборка Docker-образа
  - Публикация в GHCR
  - Применение манифестов в кластер
  - `kubectl rollout restart` при каждом пуше

---

## ✅ 3.2 Swagger-документация

- FastAPI автоматически публикует Swagger по `/docs`
- Доступен извне через Ingress

---

## Особенности

- Пуш в main ветку запрещён на уровне репозитория, обновление кода возможно только через PR
- Swagger-документация доступна по ссылке , Grafana – http://46.29.239.94/grafana/

| Компонент    | Особенности реализации                           |
|--------------|--------------------------------------------------|
| **Alembic**  | Миграции через `alembic`, асинхронный движок     |
| **JWT Auth** | `access/refresh` токены + RSA-подпись            |
| **CI/CD**    | GitHub Actions + GHCR + rollout + проверка схемы |
| **Metrics**  | Prometheus `/metrics`, подключён к Grafana       |
| **Logging**  | Вывод в stdout, собирается Promtail → Loki       |

## Ссылки и доступы

| Компонент                         | Ссылка                        | Режим доступа                                      |
|-----------------------------------|-------------------------------|----------------------------------------------------|
| **Swagger-документация**          | http://46.29.239.94/docs/     | Открытый                                           |
| **Grafana**                       | http://46.29.239.94/grafana/  | Логин и пароль можно получить у @matematessa в TG  |
| **Хост с поднятым k8s-кластером** | ssh root@46.29.239.94         | Пароль можно получить у @matematessa в TG          |

---

## 🚀 Как развернуть проект

### 🔧 1. Локальная разработка (Docker Compose)

Для локального запуска в режиме разработки:
1. Настроить все переменные окружения (`.env` на верхнем уровне и `src/env/.stable.env`)
2. Затем выполнить:
```bash
docker compose -f docker-compose.dev.yml up -d
```

Это поднимает:
- FastAPI-приложение
- PostgreSQL

Для остановки:

```bash
docker-compose down
```

Для запуска тестов:

```bash
cd src ; make test
```

---

### ☁️ 2. Продакшн

Чтобы развернуть проект в Kubernetes с нуля:

1. Установить кластер `k3s` или другой Kubernetes-дистрибутив
2. Установить `Helm`:

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

3. Установить Prometheus и Grafana:
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/prometheus --namespace default
helm install my-grafana grafana/grafana --namespace default \
  --set adminPassword=... \
  --set service.port=80 \
  --set env.GF_SERVER_ROOT_URL="/grafana" \
  --set env.GF_SERVER_SERVE_FROM_SUB_PATH=true
```

4. Применить манифесты приложения:

```bash
kubectl apply -f k8s/
```

5. Перезапустить деплоймент (так как в манифесте используется тег `:latest`):

```bash
kubectl rollout restart deployment shliwist-deployment
```

6. Перейти по адресу:

- Swagger: http://<ip>/docs
- Grafana: http://<ip>/grafana

## Особенности

- Пуш в main ветку запрещён на уровне репозитория, обновление кода возможно только через PR
- Swagger-документация доступна по ссылке , Grafana – http://46.29.239.94/grafana/

| Компонент    | Особенности реализации                           |
|--------------|--------------------------------------------------|
| **Alembic**  | Миграции через `alembic`, асинхронный движок     |
| **JWT Auth** | `access/refresh` токены + RSA-подпись            |
| **CI/CD**    | GitHub Actions + GHCR + rollout + проверка схемы |
| **Metrics**  | Prometheus `/metrics`, подключён к Grafana       |
| **Logging**  | Вывод в stdout, собирается Promtail → Loki       |

## Ссылки и доступы

| Компонент                         | Ссылка                        | Режим доступа                                      |
|-----------------------------------|-------------------------------|----------------------------------------------------|
| **Swagger-документация**          | http://46.29.239.94/docs/     | Открытый                                           |
| **Grafana**                       | http://46.29.239.94/grafana/  | Логин и пароль можно получить у @matematessa в TG  |
| **Хост с поднятым k8s-кластером** | ssh root@46.29.239.94         | Пароль можно получить у @matematessa в TG          |