# 🚨 MANUAL CONFIGURATION REQUIRED: Railway Dashboard

## Проблема

Railway Railpack 0.9.1 игнорирует `railway.json` при первоначальном деплое и автоматически определяет Node.js вместо Docker.

## Решение: Ручная настройка в Railway Dashboard

### Шаг 1: Открой Settings своего сервиса

1. **Перейди** в [Railway Dashboard](https://railway.app)
2. **Выбери** свой проект
3. **Кликни** на сервис (где ошибка "No start command")
4. **Открой** вкладку **Settings**

---

### Шаг 2: Измени Builder на Docker

В разделе **Build**:

1. **Найди** настройку **Builder**
2. **Измени** с `NIXPACKS` (или auto) на **`DOCKERFILE`**
3. **Укажи** путь к Dockerfile: `Dockerfile.railway.simple`

**Screenshot reference** (что должно быть):
```
Builder: DOCKERFILE
Dockerfile Path: Dockerfile.railway.simple
Build Context: .
```

---

### Шаг 3: Проверь Root Directory

В разделе **Source**:

1. **Убедись** что **Root Directory** = `/` (корень репозитория)
2. Если стоит `archon-ui-main` или другая папка - **измени** на `/`

---

### Шаг 4: Добавь Environment Variables

В разделе **Variables**:

**Обязательные переменные:**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=твой-service-role-ключ
```

**Где взять:**
1. [supabase.com/dashboard](https://supabase.com/dashboard)
2. Settings → API
3. Скопируй **service_role** key (ДЛИННЫЙ ключ, не anon!)

---

### Шаг 5: Trigger Redeploy

1. **Нажми** кнопку **Deploy** в правом верхнем углу
2. Или **Settings** → **Redeploy**

---

## Что произойдет после настройки

```
[Region: asia-southeast1]
╭────────────────╮
│ Railpack 0.9.1 │
╰────────────────╯
↳ Found .dockerignore file, applying filters
↳ Using Dockerfile: Dockerfile.railway.simple
↳ Building Docker image...
   ✓ Step 1/20: FROM python:3.12-slim
   ✓ Step 2/20: RUN apt-get update...
   ...
   ✓ Docker build complete!
↳ Starting container...
   ✓ Supervisor started
   ✓ Nginx listening on port 80
   ✓ archon-server started on 8181
   ✓ archon-mcp started on 8051
🎉 Deployment successful!
```

---

## Если все еще не работает

### Альтернативный способ через railway.json

Railway может игнорировать dashboard настройки. Попробуй этот формат:

**Обновленный railway.json:**
```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.railway.simple",
    "dockerContext": "."
  },
  "deploy": {
    "startCommand": "supervisord -c /etc/supervisor/conf.d/archon.conf",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Затем:
1. Commit изменения
2. Push в GitHub
3. Railway автоматически задеплоит

---

## Проверка успешного деплоя

### 1. Логи показывают Docker build:
```
✓ Using Dockerfile: Dockerfile.railway.simple
✓ Building Docker image...
✓ Docker build complete!
```

### 2. Контейнер запустился:
```
✓ Supervisor started
✓ Nginx listening on port 80
```

### 3. Health check работает:
```bash
curl https://твой-railway-url.up.railway.app/health
# Ответ:
{
  "status": "healthy",
  "service": "archon-backend",
  "ready": true
}
```

---

## 🎯 Чек-лист

- [ ] Settings → Builder = **DOCKERFILE**
- [ ] Dockerfile Path = **Dockerfile.railway.simple**
- [ ] Root Directory = **/**
- [ ] SUPABASE_URL добавлен
- [ ] SUPABASE_SERVICE_KEY добавлен (service_role!)
- [ ] Нажал **Deploy**
- [ ] Логи показывают "Using Dockerfile"
- [ ] Deployment успешен
- [ ] /health возвращает 200 OK

---

## Почему это произошло?

**Railway Railpack 0.9.1** (новый builder):
- При первом деплое **игнорирует** railway.json
- Автоматически **определяет** тип проекта по файлам
- Видит `archon-ui-main/package.json` → думает что это Node.js
- Использует **Nixpacks** вместо Docker

**Решение:**
- Ручная настройка в Dashboard **переопределяет** авто-определение
- После первого ручного деплоя Railway **запоминает** настройки
- Следующие деплои будут использовать Docker автоматически

---

**После настройки все будет работать!** 🚀
