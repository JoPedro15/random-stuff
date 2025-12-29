# Git Conventions

To ensure traceability across the Automation Ecosystem, we follow these standardized manual rules.

## 🌿 Branch Naming

Format: `<type>/<short-description>`

| Type        | Use Case                                  |
|:------------|:------------------------------------------|
| `feat/`     | New tools, clients or features.           |
| `bug/`      | Fixes and patches.                        |
| `maint/`    | Documentation and repository maintenance. |
| `research/` | Jupyter Notebooks and AI experiments.     |

## 💬 Commit Messages

Use descriptive titles in English. If an issue exists, link it:
`feat: add gdrive client download logic (closes #12)`

### Guidelines:

- Use the imperative mood ("add", not "added").
- Keep the subject line under 50 characters.
- Reference internal issues using `(closes #ID)`.

## 💎 Code Quality Gate

Before pushing any branch, you must ensure the code passes the local quality suite to avoid CI failures.

```bash
  make quality
```

This command (defined in the root Makefile) executes:

1. **Linting**: Ruff (Formatting & Logic).
2. **Security**: Bandit (SAST) & Pip-audit (Vulnerabilities).
3. **Tests**: Pytest suite.