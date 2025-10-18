# 🚀 Railway Deployment - Быстрый старт

## ✅ Всё готово к деплою!

У тебя уже есть все необходимые файлы:
- ✅ `railway.json` - конфигурация Railway
- ✅ `Dockerfile.railway.simple` - Docker образ
- ✅ `.dockerignore.railway` - исключения для Docker
- ✅ База данных Supabase настроена (45 settings, 11 таблиц)

---

## 📋 Шаг 1: Создай проект на Railway

1. **Открой** [railway.app](https://railway.app)
2. **Войди** через GitHub (если еще не вошел)
3. **Нажми** "New Project"
4. **Выбери** "Deploy from GitHub repo"
5. **Выбери** репозиторий `gHashTag/Archon`
6. **Жди** пока Railway клонирует репозиторий

> Railway автоматически найдет `railway.json` и начнет build!

---

## 🔑 Шаг 2: Добавь Environment Variables

**В Railway Dashboard → Variables, добавь:**

### Обязательные переменные:

```bash
# Supabase (используй ТВОИ значения из Supabase Dashboard)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=твой-длинный-service-role-key

# OpenAI (если есть)
OPENAI_API_KEY=sk-твой-ключ
```

### Где взять Supabase данные:

1. Открой [supabase.com/dashboard](https://supabase.com/dashboard)
2. Выбери свой проект
3. Settings → API
4. Скопируй:
   - **Project URL** → `SUPABASE_URL`
   - **service_role key** (ДЛИННЫЙ ключ) → `SUPABASE_SERVICE_KEY`

> ⚠️ ВАЖНО: Используй **service_role**, а НЕ anon key!

---

## 🚂 Шаг 3: Запусти Deployment

1. **После добавления variables** Railway автоматически начнет deploy
2. **Или нажми** "Deploy" вручную
3. **Жди** 5-10 минут (первый build долгий)

### Что происходит:

```
1. Клонирование репозитория      ⏱️ 30 сек
2. Docker build                  ⏱️ 5-8 минут
   - Установка Python 3.12
   - Установка зависимостей
   - Build React frontend
   - Настройка Nginx + Supervisor
3. Запуск приложения             ⏱️ 1-2 минуты
4. Health check                  ✅ Готово!
```

---

## 🌐 Шаг 4: Получи Public URL

1. **В Railway Dashboard** → Settings → Networking
2. **Нажми** "Generate Domain"
3. **Railway выдаст** URL типа: `archon-production.up.railway.app`
4. **Скопируй** этот URL

---

## ✅ Шаг 5: Проверь работу

### Тест 1: Health Check
Открой в браузере:
```
https://твой-railway-url.up.railway.app/health
```

Должен вернуть:
```json
{
  "status": "healthy",
  "service": "archon-backend",
  "ready": true
}
```

### Тест 2: Frontend
Открой:
```
https://твой-railway-url.up.railway.app
```

Должен загрузиться React интерфейс Archon!

### Тест 3: API Docs
```
https://твой-railway-url.up.railway.app/api/docs
```

Swagger документация API!

---

## 📊 Мониторинг

### Просмотр логов:

1. **Railway Dashboard** → твой проект
2. **Вкладка "Deployments"**
3. **Клик на последний deployment**
4. **View Logs**

### Что смотреть в логах:

✅ **Успешный запуск**:
```
[supervisord] started
[nginx] started
[archon-server] started on port 8181
[archon-mcp] started on port 8051
```

❌ **Проблемы**:
```
ERROR: Database connection failed
ERROR: Missing environment variable
```

---

## 🐛 Troubleshooting

### Проблема: Build fails

**Проверь**:
1. `railway.json` существует в корне
2. `Dockerfile.railway.simple` существует
3. Логи build в Railway Dashboard

### Проблема: 500 error при открытии

**Проверь**:
1. Environment variables добавлены правильно
2. `SUPABASE_SERVICE_KEY` - это ДЛИННЫЙ ключ (не anon)
3. База данных инициализирована (`complete_setup.sql` выполнен)

### Проблема: Медленный запуск

**Норма**: Первый запуск 5-10 минут (установка ML библиотек)
**Потом**: Перезапуски быстрее (1-2 минуты)

---

## 💰 Railway Pricing

**Hobby Plan** (бесплатно):
- $5 кредитов в месяц
- 512 MB RAM
- Достаточно для тестирования

**Developer Plan** ($5/мес):
- $5 + usage based
- Больше ресурсов
- Рекомендуется для production

---

## 🔄 Автоматические обновления

Railway автоматически пересобирает при push в GitHub!

```bash
# Сделай изменения в коде
git add .
git commit -m "Update feature"
git push origin main

# Railway автоматически:
# 1. Обнаружит изменения
# 2. Запустит новый build
# 3. Задеплоит обновление
```

---

## 🎯 Финальный чеклист

- [ ] Railway проект создан
- [ ] GitHub репозиторий подключен
- [ ] `SUPABASE_URL` добавлен
- [ ] `SUPABASE_SERVICE_KEY` добавлен (ДЛИННЫЙ ключ!)
- [ ] Deployment завершен успешно
- [ ] Public URL получен
- [ ] `/health` возвращает 200 OK
- [ ] Frontend загружается
- [ ] API docs доступны

---

## 🆘 Нужна помощь?

1. **Проверь логи** в Railway Dashboard
2. **Проверь** что все переменные окружения правильные
3. **Убедись** что база данных инициализирована

---

**Готово!** Твой Archon теперь на Railway! 🎉

**Production URL**: `https://твой-домен.up.railway.app`
