"""Java kod derleme ve çalıştırma."""

from __future__ import annotations

import subprocess
from pathlib import Path


def compile_java(source_path: Path, compile_dir: Path | None = None) -> dict:
    """Java kaynak kodunu derler."""
    result: dict = {
        "file": str(source_path),
        "compile_status": "unknown",
        "compile_output": "",
        "compile_error": "",
        "class_path": None,
    }

    if not source_path.exists():
        result["compile_status"] = "error"
        result["compile_error"] = "File not found"
        return result

    work_dir = compile_dir or source_path.parent
    try:
        proc = subprocess.run(
            ["javac", "-encoding", "UTF-8", "-d", str(work_dir), str(source_path)],
            capture_output=True, text=True, timeout=30,
        )
        result["compile_status"] = "passed" if proc.returncode == 0 else "failed"
        result["compile_output"] = proc.stdout
        result["compile_error"] = proc.stderr
        if proc.returncode == 0:
            # .class dosya yolunu bul
            class_name = source_path.stem
            class_file = work_dir / f"{class_name}.class"
            if class_file.exists():
                result["class_path"] = str(class_file)
    except subprocess.TimeoutExpired:
        result["compile_status"] = "timeout"
        result["compile_error"] = "Compilation timed out (30s)"
    except FileNotFoundError:
        result["compile_status"] = "error"
        result["compile_error"] = "javac not found in PATH"
    except Exception as e:
        result["compile_status"] = "error"
        result["compile_error"] = str(e)

    return result


def run_java(class_name: str, class_dir: Path) -> dict:
    """Derlenmiş Java sınıfını çalıştırır."""
    result: dict = {
        "class": class_name,
        "run_status": "unknown",
        "stdout": "",
        "stderr": "",
    }

    try:
        proc = subprocess.run(
            ["java", "-Dfile.encoding=UTF-8", "-cp", str(class_dir), class_name],
            capture_output=True, text=True, timeout=15,
        )
        result["run_status"] = "passed" if proc.returncode == 0 else "failed"
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
    except subprocess.TimeoutExpired:
        result["run_status"] = "timeout"
        result["stderr"] = "Execution timed out (15s)"
    except FileNotFoundError:
        result["run_status"] = "error"
        result["stderr"] = "java not found in PATH"
    except Exception as e:
        result["run_status"] = "error"
        result["stderr"] = str(e)

    return result


def test_code(source_path: Path, test_mode: str, compile_dir: Path | None = None) -> dict:
    """Java kodunu derler ve isteğe bağlı çalıştırır."""
    work_dir = compile_dir or source_path.parent
    result = compile_java(source_path, work_dir)
    result["test_mode"] = test_mode

    if result["compile_status"] != "passed":
        return result

    if test_mode in ("run", "run_assert", "compile_run", "compile_run_assert"):
        run_result = run_java(source_path.stem, work_dir)
        result["run_status"] = run_result["run_status"]
        result["stdout"] = run_result["stdout"]
        result["stderr"] = run_result["stderr"]

    return result
