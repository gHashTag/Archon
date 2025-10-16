# 🔧 Исправление 404 ошибки на Vercel

## Проблема

При деплое на Vercel возникала ошибка:
```
404: NOT_FOUND
Code: NOT_FOUND
ID: sin1::ffth2-1760619173065-5e6550a0cef9
```

## Причина

Неправильная конфигурация для Python serverless functions:

### ❌ Что было неправильно:

1. **api/index.py** - использовал Mangum и custom async handler:
```python
async def handler(request):
    from mangum import Mangum
    asgi_handler = Mangum(app, lifespan="off")
    return await asgi_handler(request, None)
```

2. **vercel.json** - использовал `functions` и `rewrites`:
```json
{
  "functions": {
    "api/index.py": { "runtime": "python3.12" }
  },
  "rewrites": [...]
}
```

3. **requirements.txt** - лишняя зависимость `mangum`

### ✅ Правильное решение:

Vercel для FastAPI ожидает просто экспорт переменной `app` (ASGI приложение).

## Исправления

### 1. api/index.py - Упрощен
```python
"""
Vercel serverless adapter for Archon FastAPI backend
"""
import os
import sys
from pathlib import Path

# Add python directory to path
python_dir = Path(__file__).parent.parent / "python"
sys.path.insert(0, str(python_dir))

# Set environment variable to indicate Vercel deployment
os.environ["VERCEL_DEPLOYMENT"] = "1"

# Import and export the FastAPI app
# Vercel automatically handles ASGI apps
from src.server.main import app
```

**Ключевой момент**: Просто импортируем и экспортируем `app`. Vercel автоматически обрабатывает ASGI приложения!

### 2. vercel.json - Обновлена конфигурация
```json
{
  "version": 2,
  "buildCommand": "npm run vercel-build",
  "outputDirectory": "archon-ui-main/dist",
  "installCommand": "npm install",
  "framework": null,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "archon-ui-main/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "archon-ui-main/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "/archon-ui-main/dist/$1"
    }
  ]
}
```

**Изменения**:
- Использованы `builds` вместо `functions`
- Использованы `routes` вместо `rewrites`
- Добавлен `"handle": "filesystem"` для статических файлов
- Явное указание `@vercel/python` и `@vercel/static-build`

### 3. requirements.txt - Удален Mangum
```txt
# Web framework
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.20

# Остальные зависимости без изменений
```

**Удалено**: `mangum>=0.17.0` - больше не нужен!

## Как работает Vercel с FastAPI

### Автоматическая обработка ASGI

Vercel автоматически определяет ASGI приложения по переменной `app`:

1. **Обнаружение**: Vercel ищет переменную `app` в `api/index.py`
2. **ASGI адаптер**: Vercel имеет встроенный ASGI адаптер
3. **Маршрутизация**: Все `/api/*` запросы направляются на FastAPI
4. **Статика**: Остальные запросы обслуживает React frontend

### Структура после исправления

```
archon/
├── api/
│   ├── index.py          # ✅ Просто экспорт app
│   └── requirements.txt  # ✅ Без Mangum
├── archon-ui-main/
│   └── dist/             # Frontend билд
├── python/
│   └── src/server/
│       └── main.py       # FastAPI app
└── vercel.json           # ✅ Правильная конфигурация
```

## Деплой исправлений

### 1. Коммит изменений
```bash
git add api/index.py vercel.json api/requirements.txt VERCEL_404_FIX.md
git commit -m "Fix Vercel 404: simplify ASGI handler and update config"
```

### 2. Push в main
```bash
git push origin stable
# Или merge в main и push туда
```

### 3. Vercel автоматически пересоберет

GitHub Actions запустит новый деплой с исправленной конфигурацией.

## Проверка после деплоя

### Frontend
```bash
curl https://archon-[hash].vercel.app
# Должен вернуть HTML страницу
```

### Backend API
```bash
# Health check
curl https://archon-[hash].vercel.app/api/health

# OpenAPI docs
curl https://archon-[hash].vercel.app/api/docs

# Projects endpoint
curl https://archon-[hash].vercel.app/api/projects
```

## Ограничения Vercel

### Что НЕ работает на Vercel:
- **Web Crawling** (`crawl4ai`) - слишком тяжелый для serverless
- **Long Running Tasks** - таймаут 10 сек (Hobby) или 60 сек (Pro)
- **Websockets** - не поддерживаются в serverless functions

### Что РАБОТАЕТ:
- ✅ REST API (все основные эндпоинты)
- ✅ Database queries (Supabase)
- ✅ AI operations (OpenAI, PydanticAI)
- ✅ Document processing (легковесные операции)
- ✅ Frontend (React + Vite)

## Альтернативы для полной функциональности

Если нужны web crawling или long tasks:
- **Railway** - поддерживает Docker и долгие процессы
- **Render** - полноценный backend с persistent storage
- **Self-hosted** - Docker Compose на VPS

## Документация

- **Vercel Python Runtime**: https://vercel.com/docs/functions/runtimes/python
- **FastAPI on Vercel**: https://github.com/hebertcisco/deploy-python-fastapi-in-vercel
- **Vercel Builds**: https://vercel.com/docs/build-step

## Итог

✅ Проблема решена упрощением конфигурации:
- Убран Mangum
- Прямой экспорт FastAPI app
- Правильная конфигурация builds/routes
- Vercel теперь правильно обрабатывает ASGI запросы

Следующий деплой должен работать без 404 ошибок! 🚀
