# GitLab MCP Server (in Python)

Model Context Protocol (MCP) server for GitLab integration, built on FastMCP.

This server is implemented in Python, with fastmcp.

## Quick Start

1. Build the Docker image:
```bash
docker build -t gitlab-mcp-server .
```

## Integration with Cursor/Claude

In MCP Settings -> Add MCP server, add this config:

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

Note: Don't forget to replace `GITLAB_TOKEN` and `GITLAB_URL` values with your actual GitLab credentials and instance URL.

## Getting GitLab Token

1. Log in to your GitLab account
2. Go to Settings -> Access Tokens
3. Create a new token:
   - Scopes: select the necessary permissions:
     - `api` - for API access
     - `read_repository` - for reading repositories
     - `write_repository` - for writing to repositories
4. Click "Create personal access token"
5. Copy the generated token (it will be shown only once!)

## Prompt (rule) for review

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
  - Begin with "[AI]".
  - Be specific, actionable, and reference the relevant code line(s).
  - Do not write a lot of text. Smaller is better.

---

### 4. Additional Guidelines

- Prioritize clarity, conciseness, and constructiveness in all feedback.
- Focus on both business logic and code quality.
- Ensure all suggestions are justified and, where possible, reference best practices or project standards.
- If you identify a bug, explain the reasoning and potential impact.

## Contributing

Feel free to:
- Add new GitLab integration tools and features
- Improve existing functionality
- Fix bugs
- Enhance documentation
- Suggest improvements

To contribute:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Open a Pull Request

All contributions, big or small, are appreciated!
