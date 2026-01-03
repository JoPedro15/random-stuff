# automation-hub/scripts/health_check_logger.py
import logging
import os
import sys
from pathlib import Path

# --- 1. Infrastructure Setup ---
# Ensure project root is in PYTHONPATH for standalone execution
PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

# --- 2. Logger Injection ---
# Import the logger instance with explicit type casting for IDE support
try:
    from core_lib_client.logger_client import logger as raw_logger

    # Casting ensures 'getEffectiveLevel' and other Logger methods are recognized
    logger: logging.Logger = raw_logger
except ImportError as err:
    sys.stderr.write("❌ Critical: Could not import core_lib. Check your PYTHONPATH.\n")
    sys.stderr.write(f"📂 Project Root detected as: {PROJECT_ROOT}\n")
    sys.stderr.write(f"⚠️ Error: {err}\n")
    sys.exit(1)


def run_check() -> bool:
    """
    Executes a clinical validation of the Logger infrastructure.
    Validates: Instantiation, Environment Config, and File System Permissions.
    """
    sys.stdout.write(">>> 🩺 [HEALTH CHECK] Starting Logger System Validation\n")

    try:
        # 1. Emission Test
        # Validates if the Singleton is alive and formatting logic is sound
        logger.info("Health Check: Standard emission test.")

        # 2. Environment Integrity
        # Confirms that LOG_LEVEL from environment is being respected
        level_name: str = os.getenv("LOG_LEVEL", "INFO").upper()
        sys.stdout.write(f">>> ⚙️  Configuration: Log Level is set to {level_name}\n")

        # 3. File System Integrity (Rigor step)
        # Validates write permissions if a file path is defined
        log_file: str | None = os.getenv("LOG_FILE_PATH")
        if log_file:
            log_path: Path = Path(log_file).resolve()
            log_dir: Path = log_path.parent

            sys.stdout.write(f">>> 📂 Validating Log Directory: {log_dir}\n")

            if not log_dir.exists():
                sys.stdout.write("⚠️  Warning: Log directory missing. Creating...\n")
                log_dir.mkdir(parents=True, exist_ok=True)

            # Smoke test: Practical write/delete validation
            test_file: Path = log_dir / ".logger_health_test"
            try:
                test_file.write_text("Health check probe", encoding="utf-8")
                test_file.unlink()  # Clean up artifact
                sys.stdout.write(f"✅ Write permissions verified at {log_dir}\n")
            except OSError as e:
                sys.stdout.write(
                    f"❌ Critical: No write permission at {log_dir}. Error: {e}\n"
                )
                return False

        sys.stdout.write("✅ Logger infrastructure is fully operational.\n")
        return True

    except Exception as e:
        # Fallback to sys.stderr if the check itself crashes
        sys.stderr.write(f"❌ Logger Health Check Failed: {str(e)}\n")
        return False


if __name__ == "__main__":
    # Standard exit codes for CI/CD and Makefile integration
    if not run_check():
        sys.stdout.write("❌ Health check concluded with errors.\n")
        sys.exit(1)

    sys.stdout.write("✅ System is healthy.\n")
    sys.exit(0)
