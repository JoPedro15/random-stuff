# Issue Standardization and Management

This document defines the standardized workflow for managing work items across **ai-lab** and **automation-hub**. As an
Automation Engineer, following these templates ensures scalability, traceability, and seamless integration with our
CI/CD pipelines.

---

## 1. Issue Types

| Type            | Label         | Description                                                                                                      |
|:----------------|:--------------|:-----------------------------------------------------------------------------------------------------------------|
| **Feature**     | `feature`     | Development of new functionalities, API clients, or automation scripts that add new capabilities to the system.  |
| **Bug**         | `bug`         | Identification and resolution of unexpected behavior, code failures, or broken pipelines.                        |
| **Maintenance** | `maintenance` | Routine tasks including dependency updates, code refactoring, infrastructure improvements, or `Makefile` tuning. |
| **Research**    | `research`    | Data exploration, Jupyter Notebook development, machine learning model training, and experimental analysis.      |

---

## 2. Issue Content Structure

Every issue, regardless of its type, must be documented using the following three pillars to be considered actionable.

### I. Context

A clear and concise explanation of the problem, the necessity of the task, or the technical goal to be achieved.

### II. Tasks

A bulleted list of technical steps or sub-tasks required to complete the work.

### III. Acceptance Criteria

The specific conditions or outcomes that must be met for the issue to be officially resolved and closed.

---

## 3. Practical Examples

### Example 1: Feature Request

**Title:** `[Feature] Implement Automated Health Checks for API Clients`

**Context:**
Currently, we lack a quick way to verify if the Google Drive and Spotify credentials are still valid before running long
data processing notebooks. We need an automated "ping" mechanism to prevent runtime authentication failures.

**Tasks:**

* [ ] Create a standalone `scripts/health_check.py` script.
* [ ] Implement a lightweight connection test for `gdrive-client`.
* [ ] Implement a profile fetch test for `spotify-client`.
* [ ] Integrate the health check into the `Makefile` as a new target.
* [ ] Add type annotations to all new functions.

**Acceptance Criteria:**

* Running `make health-check` returns a clear success/fail status for all configured clients.
* The script must fail (exit code 1) if any client is unauthorized.
* Security analysis via `make security` remains green.

---

### Example 2: Bug Report

**Title:** `[Bug] Bandit Security Audit failing on .venv directory`

**Context:**
The `make security` command is currently scanning the internal library files inside the `.venv` folder, leading to
thousands of false positives and slow execution times.

**Tasks:**

* [ ] Update `.bandit` configuration file to explicitly exclude the `.venv` directory.
* [ ] Refactor the `Makefile` security target to use the configuration file.
* [ ] Verify that only project source files are being scanned.

**Acceptance Criteria:**

* `make security` execution time is under 5 seconds.
* Total lines of code scanned match only the project's Python files.
* No issues identified from third-party libraries.

---

## 4. Workflow Automation

To streamline this process, use the project's **Orchestration Scripts** (when available) or the **GitHub Issue Forms**
to ensure all fields are populated correctly before starting a new branch.

> **Note:** Always use Type Annotations for any Python code implemented as part of these issues.
