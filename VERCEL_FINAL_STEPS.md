# ✅ Vercel CI/CD Настроено! Последние шаги

## Что было сделано

### 1. ✅ Vercel CLI установлен
- Установлена последняя версия Vercel CLI
- Авторизован пользователь: **raoffonom**

### 2. ✅ Проект подключен к Vercel
- Проект: **ghashtag/archon**
- Project ID: `prj_i786DCaCJAqnDBPIZnCRlcrB8QNn`
- Org ID: `team_jIw4AOO9xChy3TQn37T4pX9x`
- Папка `.vercel/` создана (добавлена в .gitignore)

### 3. ✅ GitHub Secrets добавлены
В репозитории **gHashTag/Archon** добавлены секреты:
- ✅ `VERCEL_ORG_ID`
- ✅ `VERCEL_PROJECT_ID`
- ⏳ `VERCEL_TOKEN` - нужно добавить вручную

### 4. ✅ GitHub Actions Workflows созданы
- `.github/workflows/vercel-deploy.yml` - Production деплой (при push в `main`)
- `.github/workflows/vercel-preview.yml` - Preview деплой (при Pull Request)

### 5. ✅ Конфигурация исправлена
- `vercel.json` - исправлен routing (rewrites вместо routes)
- `api/index.py` - добавлен Mangum ASGI адаптер
- `api/requirements.txt` - обновлены зависимости

### 6. ✅ Git remote обновлен
- Изменен remote с `coleam00/archon` на `gHashTag/Archon`
- Коммит создан и запушен в ветку `stable`

### 7. ✅ Документация создана
- `VERCEL_DEPLOY.md` - полное руководство по деплою
- `VERCEL_SETUP.md` - быстрая настройка CI/CD
- `scripts/add-vercel-token.sh` - скрипт для добавления токена

## 🚨 Осталось сделать: Добавить VERCEL_TOKEN

### Шаг 1: Создайте Vercel Token

Страница для создания токена **уже открыта** в вашем браузере:
https://vercel.com/account/tokens

Если нет, откройте её:
```bash
open "https://vercel.com/account/tokens"
```

### Шаг 2: Создайте токен
1. Нажмите **"Create Token"**
2. Name: `GitHub Actions`
3. Scope: **Full Account**
4. Нажмите **"Create"**
5. **Скопируйте токен** (показывается только один раз!)

### Шаг 3: Добавьте токен в GitHub

**Вариант A: Используйте готовый скрипт (рекомендуется)**
```bash
./scripts/add-vercel-token.sh
```

Скрипт попросит вас:
1. Подтвердить, что токен создан
2. Вставить токен
3. Автоматически добавит его в GitHub Secrets
4. Проверит, что все секреты на месте

**Вариант B: Добавьте вручную через GitHub CLI**
```bash
# Вставьте свой токен вместо YOUR_VERCEL_TOKEN
gh secret set VERCEL_TOKEN --body "YOUR_VERCEL_TOKEN" --repo gHashTag/Archon
```

**Вариант C: Через веб-интерфейс GitHub**
1. Откройте: https://github.com/gHashTag/Archon/settings/secrets/actions
2. Нажмите **"New repository secret"**
3. Name: `VERCEL_TOKEN`
4. Value: вставьте ваш токен
5. Нажмите **"Add secret"**

## 🚀 Запуск автоматического деплоя

### Вариант 1: Push в main (рекомендуется для production)

```bash
# Переключитесь на main
git checkout main

# Merge изменений из stable
git merge stable

# Push в main для автодеплоя
git push origin main
```

**Результат**: GitHub Actions автоматически задеплоит на Vercel Production!

### Вариант 2: Создать Pull Request

```bash
# Создать PR из stable в main
gh pr create --base main --head stable --title "Setup Vercel CI/CD deployment" --body "This PR adds automated Vercel deployment via GitHub Actions"
```

**Результат**:
- Создастся Preview деплой (можно протестировать)
- После merge в main - Production деплой

### Вариант 3: Ручной workflow запуск

1. Откройте: https://github.com/gHashTag/Archon/actions/workflows/vercel-deploy.yml
2. Нажмите **"Run workflow"**
3. Выберите ветку `main`
4. Нажмите **"Run workflow"**

## 📊 Мониторинг деплоя

### GitHub Actions
После push в main откройте:
https://github.com/gHashTag/Archon/actions

Вы увидите workflow **"Vercel Production Deployment"** в процессе выполнения.

### Vercel Dashboard
Откройте: https://vercel.com/ghashtag/archon/deployments

Вы увидите:
- Статус деплоя
- Логи билда
- URL production сайта

## ✅ Проверка успешного деплоя

После завершения деплоя:

### 1. Frontend
```bash
# URL будет в комментарии к коммиту или в логах GitHub Actions
curl https://archon-[hash].vercel.app
```

### 2. Backend API
```bash
# Health check
curl https://archon-[hash].vercel.app/api/health

# Projects endpoint
curl https://archon-[hash].vercel.app/api/projects
```

### 3. Vercel Environment Variables
Убедитесь, что добавлены в Vercel Dashboard:
https://vercel.com/ghashtag/archon/settings/environment-variables

Нужны:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SUPABASE_ANON_KEY`
- `OPENAI_API_KEY` (опционально)

## 🎯 Текущий статус

| Задача | Статус |
|--------|--------|
| Vercel CLI установлен | ✅ |
| Проект подключен | ✅ |
| VERCEL_ORG_ID | ✅ |
| VERCEL_PROJECT_ID | ✅ |
| VERCEL_TOKEN | ⏳ **ТРЕБУЕТСЯ** |
| GitHub Workflows | ✅ |
| Конфигурация исправлена | ✅ |
| Изменения закоммичены | ✅ |
| Push в stable | ✅ |
| Push в main | ⏳ Ждёт вас |

## 🔥 Quick Start - Всё в одном месте

```bash
# 1. Откройте браузер для создания токена
open "https://vercel.com/account/tokens"

# 2. После создания токена, запустите скрипт
./scripts/add-vercel-token.sh

# 3. Задеплойте на production
git checkout main
git merge stable
git push origin main

# 4. Откройте Actions для мониторинга
open "https://github.com/gHashTag/Archon/actions"
```

## 📚 Документация

- **Быстрая настройка**: `VERCEL_SETUP.md`
- **Полное руководство**: `VERCEL_DEPLOY.md`
- **Текущий файл**: `VERCEL_FINAL_STEPS.md`

## 🆘 Troubleshooting

### GitHub Actions не запускается
- Проверьте что push был в ветку `main`
- Проверьте что workflow файл существует: `.github/workflows/vercel-deploy.yml`

### Deployment fails
- Проверьте логи в GitHub Actions
- Проверьте что `VERCEL_TOKEN` добавлен в Secrets
- Проверьте что Environment Variables установлены в Vercel

### 404 ошибка после деплоя
- ✅ Уже исправлено в `vercel.json`
- Проверьте что билд прошёл успешно
- Проверьте что `archon-ui-main/dist/` содержит файлы

---

**Следующий шаг**: Добавьте `VERCEL_TOKEN` через `./scripts/add-vercel-token.sh` 🚀
