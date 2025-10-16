# 🚀 Быстрая Настройка Vercel CI/CD

## Что было исправлено

### 1. Конфигурация Vercel (`vercel.json`)
- ✅ Исправлен routing (использованы `rewrites` вместо `routes`)
- ✅ Добавлена правильная конфигурация для Python функций
- ✅ Настроены CORS headers
- ✅ Увеличен timeout до 60 секунд

### 2. Python Adapter (`api/index.py`)
- ✅ Добавлен Mangum для ASGI адаптации
- ✅ Правильная инициализация FastAPI app
- ✅ Добавлен environment variable для Vercel

### 3. Зависимости (`api/requirements.txt`)
- ✅ Добавлен `mangum` для serverless функций
- ✅ Добавлен `pydantic-ai` и `pydantic-settings`
- ✅ Оптимизированы зависимости для Vercel

### 4. CI/CD Workflows
- ✅ `.github/workflows/vercel-deploy.yml` - Production деплой
- ✅ `.github/workflows/vercel-preview.yml` - Preview для PR

## Шаги для активации CI/CD

### Шаг 1: Установите Vercel CLI
```bash
npm i -g vercel
```

### Шаг 2: Подключите проект
```bash
# Войдите в Vercel
vercel login

# В корне проекта Archon
cd /Users/playra/archon
vercel link
```

Выберите:
- **Set up existing project?** → Yes
- **Link to existing project?** → Yes
- Выберите ваш проект или создайте новый

### Шаг 3: Получите Project ID и Org ID
```bash
cat .vercel/project.json
```

Вы увидите:
```json
{
  "projectId": "prj_xxxxxxxxxxxxx",
  "orgId": "team_xxxxxxxxxxxxx"
}
```

### Шаг 4: Создайте Vercel Token
1. Откройте https://vercel.com/account/tokens
2. Нажмите **Create Token**
3. Name: `GitHub Actions`
4. Scope: **Full Account**
5. Скопируйте токен (показывается только один раз!)

### Шаг 5: Добавьте GitHub Secrets
Откройте: https://github.com/YOUR_USERNAME/archon/settings/secrets/actions

Добавьте три секрета:

| Name | Value | Пример |
|------|-------|--------|
| `VERCEL_TOKEN` | Ваш Vercel токен | `aBc123...xyz` |
| `VERCEL_ORG_ID` | orgId из .vercel/project.json | `team_xxx` |
| `VERCEL_PROJECT_ID` | projectId из .vercel/project.json | `prj_xxx` |

### Шаг 6: Настройте Environment Variables в Vercel

Откройте: https://vercel.com/your-team/archon/settings/environment-variables

Добавьте для **Production, Preview, Development**:

```bash
SUPABASE_URL=https://yuukfqcsdhkyxegfwlcb.supabase.co
SUPABASE_SERVICE_KEY=ваш_service_role_key
SUPABASE_ANON_KEY=ваш_anon_key
OPENAI_API_KEY=ваш_openai_key (опционально)
```

⚠️ **ВАЖНО**: Используйте `service_role` ключ для SUPABASE_SERVICE_KEY!

### Шаг 7: Задеплойте!
```bash
git add .
git commit -m "Fix Vercel deployment configuration"
git push origin main
```

GitHub Actions автоматически:
1. ✅ Соберет frontend (React + Vite)
2. ✅ Подготовит Python backend
3. ✅ Задеплоит на Vercel
4. ✅ Добавит комментарий с URL

## Проверка деплоя

После деплоя проверьте:

### 1. Frontend
Откройте URL из комментария GitHub Actions:
```
https://your-project.vercel.app
```

### 2. Backend API
```bash
# Health check
curl https://your-project.vercel.app/api/health

# Projects endpoint
curl https://your-project.vercel.app/api/projects
```

### 3. Логи
Откройте: https://vercel.com/your-team/archon/deployments

Выберите последний деплой → Function Logs

## Автоматические деплои

### Production (main branch)
Каждый push в `main` → автоматический production деплой

### Preview (Pull Requests)
Каждый PR → preview деплой с уникальным URL

### Ручной деплой
```bash
# Локально
vercel --prod

# Или через GitHub Actions
# Откройте: Actions → Vercel Production Deployment → Run workflow
```

## Troubleshooting

### 404 ошибка
- ✅ Исправлено в `vercel.json` (использованы rewrites)
- Проверьте что билд успешно создал `archon-ui-main/dist/`

### 500 Internal Server Error
- Проверьте Function Logs в Vercel Dashboard
- Убедитесь что все environment variables установлены
- Проверьте что используется `service_role` ключ Supabase

### CORS ошибки
- ✅ Headers настроены в `vercel.json`
- Проверьте что backend доступен по `/api/*` URL

### Timeout ошибки
- ✅ Увеличен до 60 секунд в `vercel.json`
- Для Hobby плана максимум 10 секунд (upgrade to Pro)

## Мониторинг

### Vercel Dashboard
https://vercel.com/your-team/archon

- **Deployments**: История деплоев
- **Functions**: Логи и метрики
- **Analytics**: Трафик и производительность

### GitHub Actions
https://github.com/YOUR_USERNAME/archon/actions

- **Vercel Production Deployment**: Main branch деплои
- **Vercel Preview Deployment**: PR previews

## Полезные команды

```bash
# Локальная разработка с Vercel
vercel dev

# Посмотреть логи последнего деплоя
vercel logs

# Список деплоев
vercel ls

# Удалить preview деплой
vercel remove [deployment-url]

# Информация о проекте
vercel inspect
```

## Документация

- **Полная инструкция**: `VERCEL_DEPLOY.md`
- **Vercel Docs**: https://vercel.com/docs
- **GitHub Actions**: https://docs.github.com/actions
