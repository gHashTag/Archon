# Деплой Archon на Railway

Это руководство описывает процесс деплоя Archon на платформу Railway.

## Предварительные требования

1. **Аккаунт Railway**: Зарегистрируйтесь на [railway.app](https://railway.app)
2. **Аккаунт Supabase**: Создайте проект на [supabase.com](https://supabase.com)
3. **OpenAI API Key**: Получите на [platform.openai.com](https://platform.openai.com)

## Шаг 1: Подготовка Supabase

### 1.1 Создание проекта Supabase
1. Войдите в [Supabase Dashboard](https://supabase.com/dashboard)
2. Создайте новый проект
3. Дождитесь завершения инициализации

### 1.2 Настройка базы данных
1. Перейдите в SQL Editor в вашем Supabase проекте
2. Скопируйте содержимое файла `migration/complete_setup.sql`
3. Вставьте и выполните SQL код в редакторе

### 1.3 Получение учетных данных
1. Перейдите в Settings → API
2. Скопируйте следующие значения:
   - **Project URL** (SUPABASE_URL)
   - **Service Role Key** (SUPABASE_SERVICE_KEY) - используйте ДЛИННЫЙ ключ!

## Шаг 2: Деплой на Railway

### 2.1 Создание проекта
1. Войдите в [Railway Dashboard](https://railway.app/dashboard)
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Подключите GitHub аккаунт и выберите форк репозитория Archon

### 2.2 Конфигурация сборки
Railway автоматически обнаружит `railway.json` и `Dockerfile.railway`. Если нужно, можно указать:
- **Build Command**: `docker build -f Dockerfile.railway -t archon .`
- **Start Command**: автоматически из Dockerfile

### 2.3 Настройка переменных окружения
В разделе Variables вашего Railway проекта добавьте:

```env
# Обязательные переменные
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Дополнительные переменные
PORT=80
PYTHONPATH=/app
PROD=true
LOG_LEVEL=INFO

# Порты сервисов (фиксированные для Railway)
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_UI_PORT=80
HOST=0.0.0.0
```

### 2.4 Запуск деплоя
1. После добавления переменных нажмите "Deploy"
2. Дождитесь завершения сборки (может занять 5-10 минут)
3. Railway предоставит публичный URL вашего приложения

## Шаг 3: Настройка приложения

### 3.1 Первичная настройка
1. Откройте URL вашего Archon приложения
2. Пройдите процесс onboarding
3. Добавьте ваш OpenAI API ключ в настройках

### 3.2 Тестирование функциональности
1. **Тест загрузки сайта**: Knowledge Base → "Crawl Website" → введите URL документации
2. **Тест загрузки файла**: Knowledge Base → загрузите PDF документ
3. **Тест проектов**: Projects → создайте новый проект и задачи
4. **Тест MCP**: MCP Dashboard → скопируйте конфигурацию для AI ассистента

## Шаг 4: Настройка MCP для AI ассистентов

### 4.1 Подключение к Claude Code
Добавьте в настройки Claude Code:
```json
{
  "mcpServers": {
    "archon": {
      "command": "curl",
      "args": ["-X", "POST", "YOUR_RAILWAY_URL/api/mcp/tools", "-H", "Content-Type: application/json"]
    }
  }
}
```

### 4.2 Подключение к Cursor/Windsurf
Используйте HTTP транспорт для подключения к вашему Railway URL.

## Troubleshooting

### Проблемы с сборкой
- Убедитесь, что все файлы `Dockerfile.railway`, `railway.json` присутствуют
- Проверьте логи сборки в Railway Dashboard

### Проблемы с переменными окружения
- Используйте **service_role key**, а не anon key для Supabase
- Убедитесь, что все обязательные переменные заданы

### Проблемы с подключением к базе данных
- Проверьте, что SQL миграция была выполнена корректно
- Убедитесь, что Supabase URL и ключи правильные

### Медленный запуск
- Первый запуск может занять до 5 минут из-за установки ML зависимостей
- Последующие перезапуски будут быстрее благодаря кэшированию

## Мониторинг

### Логи приложения
Используйте Railway Dashboard для просмотра логов:
- **Build Logs**: логи сборки Docker образа
- **Deploy Logs**: логи запуска приложения
- **App Logs**: логи работы приложения

### Health Check
Railway автоматически мониторит здоровье приложения через `/health` endpoint.

## Обновления

### Автоматические обновления
Railway автоматически пересобирает приложение при изменениях в главной ветке репозитория.

### Ручное обновление
1. Сделайте git push в подключенный репозиторий
2. Railway автоматически запустит новый деплой

## Лимиты Railway

- **Free Tier**: 512 MB RAM, $5 кредитов в месяц
- **Pro Tier**: Больше ресурсов и кредитов
- **Время сборки**: обычно 5-15 минут для Archon

## Поддержка

При возникновении проблем:
1. Проверьте логи в Railway Dashboard
2. Убедитесь, что все переменные окружения заданы правильно
3. Проверьте статус Supabase проекта
4. Обратитесь к документации Archon или Railway