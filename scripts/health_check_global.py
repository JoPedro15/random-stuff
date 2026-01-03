# automation-hub/scripts/health_check_global.py
import importlib
import pkgutil
import sys
from pathlib import Path
from typing import Any

# --- 1. Infrastructure Setup ---
PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


def run_all_health_checks() -> None:
    """
    Dynamically discovers and executes all health check modules in the scripts folder.
    Convention: Must start with 'health_check_' and NOT be 'health_check_global'.
    """
    sys.stdout.write(
        "\n\033[1m>>> 🩺 [DYNAMIC] Starting Global Health Orchestration\033[0m\n"
    )
    sys.stdout.write("-" * 65 + "\n")

    scripts_path: str = str(PROJECT_ROOT / "scripts")
    failed_components: list[str] = []

    # 1. Discover modules
    for _, module_name, _ in pkgutil.iter_modules([scripts_path]):
        if (
            module_name.startswith("health_check_")
            and module_name != "health_check_global"
        ):
            display_name: str = (
                module_name.replace("health_check_", "").replace("_", " ").title()
            )

            # Progress indicator
            sys.stdout.write(f"Testing {display_name}...")
            sys.stdout.flush()

            try:
                # 2. Dynamic Import
                module: Any = importlib.import_module(f"scripts.{module_name}")
                # Ensure we have the latest version of the module code
                importlib.reload(module)

                # 3. Contract Validation
                if hasattr(module, "run_check"):
                    result: Any = module.run_check()

                    success, message = (
                        result if isinstance(result, tuple) else (result, "OK")
                    )

                    status_color: str = (
                        "\033[92mPASS\033[0m" if success else "\033[91mFAIL\033[0m"
                    )
                    # \r clears the "Testing..." line and writes the result
                    sys.stdout.write(
                        f"\r[{status_color}] {display_name:.<30} {message}\n"
                    )

                    if not success:
                        failed_components.append(display_name)
                else:
                    sys.stdout.write(
                        f"\r[⚠️ SKIP] {display_name:.<30} No 'run_check()' found.\n"
                    )

            except Exception as e:
                # Robustness: Capture crashes during import or execution
                sys.stdout.write(f"\r[❌ CRASH] {display_name:.<30} {str(e)}\n")
                failed_components.append(display_name)

    # --- Verdict Logic ---
    sys.stdout.write("-" * 65 + "\n")
    if failed_components:
        # Rigor: Exit code 1 for CI/CD failure
        sys.stderr.write(
            f"\n\033[91m\033[1m❌ FAILED: {', '.join(failed_components)}\033[0m\n\n"
        )
        sys.exit(1)

    sys.stdout.write("\n\033[92m\033[1m✅ ALL SYSTEMS FUNCTIONAL\033[0m\n\n")
    sys.exit(0)


if __name__ == "__main__":
    run_all_health_checks()
