# GitLab MCP Сервер

Сервер протокола контекста модели (MCP) для интеграции с GitLab, построенный на FastMCP.

## Быстрый старт

1. Соберите Docker образ:
```bash
docker build -t gitlab-mcp-server .
```

## Интеграция с Cursor AI

В настройках MCP -> Добавить MCP сервер, туда закидывается конфиг:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e",
        "GITLAB_TOKEN",
        "-e",
        "GITLAB_URL",
        "gitlab-mcp-server:latest"
      ],
      "env": {
        "GITLAB_TOKEN": "token",
        "GITLAB_URL": "https://mimimi.ninja/"
      }
    }
  }
}
```

Примечание: Не забудьте заменить значения `GITLAB_TOKEN` и `GITLAB_URL` на ваши реальные учетные данные GitLab и URL вашего экземпляра. 

## Получение GitLab токена

1. Войдите в свой аккаунт GitLab
2. Перейдите в Settings -> Access Tokens
3. Создайте новый токен:
   - Scopes: выберите необходимые разрешения:
     - `api` - для доступа к API
     - `read_repository` - для чтения репозиториев
     - `write_repository` - для записи в репозитории
4. Нажмите "Create personal access token"
5. Скопируйте сгенерированный токен (он будет показан только один раз!)