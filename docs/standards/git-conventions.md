# Git Conventions

To ensure traceability across the Automation Ecosystem, we follow these manual standards.

## Branch Naming

Format: `<type>/<short-description>`

| Type        | Use Case                                  |
|:------------|:------------------------------------------|
| `feat/`     | New tools, clients or features.           |
| `bug/`      | Fixes and patches.                        |
| `maint/`    | Documentation and repository maintenance. |
| `research/` | Jupyter Notebooks and AI experiments.     |

## Commit Messages

Use descriptive titles. If an issue exists, link it:
`feat: add spotify client auth logic (closes #12)`