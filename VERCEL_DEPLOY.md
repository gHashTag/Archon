# 🚀 Деплой Archon на Vercel

## Подготовка проекта

Проект Archon состоит из двух частей:
- **Frontend**: React + Vite (папка `archon-ui-main/`)
- **Backend**: FastAPI (папка `python/`, адаптер в `api/`)

## Автоматический деплой через GitHub Actions

### Настройка CI/CD (Рекомендуется)

1. **Получите токены Vercel**:
   ```bash
   # Установите Vercel CLI
   npm i -g vercel

   # Войдите в аккаунт
   vercel login

   # В корне проекта выполните
   vercel link
   ```

2. **Получите необходимые ID**:
   ```bash
   # После vercel link, проверьте .vercel/project.json
   cat .vercel/project.json
   # Вы увидите: projectId и orgId
   ```

3. **Создайте Vercel токен**:
   - Откройте https://vercel.com/account/tokens
   - Создайте новый токен (Scope: Full Account)
   - Скопируйте токен

4. **Добавьте GitHub Secrets**:
   - Откройте Settings → Secrets → Actions в вашем GitHub репозитории
   - Добавьте:
     - `VERCEL_TOKEN` - ваш Vercel токен
     - `VERCEL_ORG_ID` - из .vercel/project.json (orgId)
     - `VERCEL_PROJECT_ID` - из .vercel/project.json (projectId)

5. **Push в main для деплоя**:
   ```bash
   git add .
   git commit -m "Setup Vercel deployment"
   git push origin main
   ```

GitHub Actions автоматически задеплоит на Vercel! 🚀

### Workflows:
- **Production** (`.github/workflows/vercel-deploy.yml`): Деплоит при push в `main`
- **Preview** (`.github/workflows/vercel-preview.yml`): Создает preview при Pull Request

## Ручной деплой

### 1. Подключение репозитория к Vercel

1. Зайдите на [vercel.com](https://vercel.com)
2. Нажмите **"Add New Project"**
3. Выберите ваш GitHub репозиторий с Archon
4. Vercel автоматически обнаружит конфигурацию из `vercel.json`

### 2. Настройка переменных окружения

В настройках проекта Vercel добавьте следующие Environment Variables:

#### Обязательные переменные:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here
SUPABASE_ANON_KEY=your-anon-key-here
```

#### Опциональные переменные:
```bash
OPENAI_API_KEY=sk-your-openai-key
LOG_LEVEL=INFO
```

**⚠️ ВАЖНО**: Используйте **service_role** ключ для `SUPABASE_SERVICE_KEY`, а не anon ключ!

### 3. Деплой

После настройки переменных окружения:

```bash
# Добавьте файлы в git
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

Vercel автоматически:
1. Установит зависимости через `npm install`
2. Запустит `npm run vercel-build` для билда frontend
3. Настроит Python serverless functions для backend API
4. Задеплоит проект

### 4. Проверка деплоя

После успешного деплоя:

1. **Frontend**: Откройте URL вашего проекта на Vercel
2. **Backend API**: Проверьте `/api/health` endpoint
3. **Settings**: Настройте API ключи через Settings страницу в UI

## Структура проекта для Vercel

```
archon/
├── api/                      # Python serverless functions
│   ├── index.py             # Адаптер для FastAPI
│   └── requirements.txt     # Python зависимости для Vercel
├── archon-ui-main/          # React frontend
│   ├── dist/                # Билд артефакты (создается при билде)
│   └── package.json
├── python/                  # FastAPI backend
│   └── src/server/main.py
├── vercel.json              # Конфигурация Vercel
├── package.json             # Корневой package.json с build командами
└── .vercelignore           # Файлы для исключения из деплоя
```

## Конфигурация

### vercel.json

```json
{
  "version": 2,
  "buildCommand": "npm run vercel-build",
  "outputDirectory": "archon-ui-main/dist",
  "installCommand": "npm install",
  "framework": null,
  "functions": {
    "api/*.py": {
      "runtime": "python3.12"
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/archon-ui-main/dist/$1"
    }
  ]
}
```

### Особенности деплоя

1. **Python Runtime**: Используется Python 3.12
2. **Serverless Functions**: Backend API работает через Vercel Serverless Functions
3. **Static Frontend**: Frontend билдится как статические файлы
4. **Proxy**: Все `/api/*` запросы проксируются на Python backend

## Ограничения Vercel

⚠️ **Важные ограничения**:

1. **Timeout**: 10 секунд для Hobby плана, 60 секунд для Pro
2. **Memory**: 1024 MB для функций
3. **Bundle Size**: Максимум 250 MB для Python функций
4. **Cold Start**: Первый запрос может быть медленным

Некоторые функции Archon могут не работать на Vercel из-за этих ограничений:
- **Web Crawling**: `crawl4ai` исключен из зависимостей (слишком тяжелый)
- **Long Running Tasks**: Задачи > 10 секунд будут обрываться на Hobby плане

## Рекомендации

Для production деплоя рекомендуется:

1. **Vercel Pro**: Для увеличения лимитов
2. **Railway/Render**: Для полной функциональности (web crawling, long tasks)
3. **Docker**: Для самостоятельного хостинга всех компонентов

## Troubleshooting

### Ошибка при билде

```bash
# Локально протестируйте билд
cd archon-ui-main
npm install
npm run build
```

### Backend не отвечает

1. Проверьте логи в Vercel Dashboard
2. Убедитесь что переменные окружения установлены
3. Проверьте что используется service_role ключ Supabase

### CORS ошибки

Backend настроен на CORS "*" для всех доменов. Если есть проблемы, проверьте настройки в `python/src/server/main.py`.

## Документация

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [Archon Repository](https://github.com/coleam00/Archon)
