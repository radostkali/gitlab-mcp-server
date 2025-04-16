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
        "GITLAB_URL": "https://gitlab.com/"
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

## Промт (rule) для ревью

Here are some suggestions to improve and clarify your review.mdc rules for code review:

---

**review.mdc (Improved Version)**

**Purpose:**  
Guidelines for conducting code reviews in the current branch, focusing on diffs with the origin/master branch, and integrating with the MCP GitLab server.

---

### 1. Review Scope

- Review only the changes in the current branch compared to the origin/master branch.
- Locate the corresponding Merge Request (MR) for this branch in GitLab using MCP tools.

---

### 2. Review Structure

- **Summary of Changes:**  
  - Provide a concise summary divided into two sections:
    - **Business Changes:** Describe the impact on business logic, user experience, or requirements.
    - **Code Changes:** Summarize technical modifications, refactoring, or architectural shifts.

- **Logical Breakdown:**  
  - Divide the changes into logical blocks (e.g., features, bug fixes, refactoring).
  - List these blocks clearly.

- **Detailed Review:**  
  - For each block, provide:
    - A brief description.
    - Suggestions for improvement (code quality, readability, maintainability, performance, etc.).
    - Identification of potential bugs or issues.
    - Illustrate type of suggestion with emoji.
    - Link to line in code.
  - If the terms of reference (requirements/spec) are not provided, request them to ensure accurate review.

---

### 3. Suggestions and Comments

- Propose to post line comments with suggestions directly in the Merge Request using the MCP GitLab server.
- All line comments in Merge Request must:
  - Begin with “[AI]”.
  - Be specific, actionable, and reference the relevant code line(s).
  - Do not write a lot of text. Smaller is better.

---

### 4. Additional Guidelines

- Prioritize clarity, conciseness, and constructiveness in all feedback.
- Focus on both business logic and code quality.
- Ensure all suggestions are justified and, where possible, reference best practices or project standards.
- If you identify a bug, explain the reasoning and potential impact.
