from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def sample_chapter() -> Path:
    return PROJECT_ROOT / "sample" / "sample_chapter.md"


@pytest.fixture
def tmp_path() -> Path:
    """tmp_path'i proje build/ altına yönlendir (sandbox izin sorunu için)."""
    import uuid

    base = PROJECT_ROOT / "build" / ".pytest_tmp" / uuid.uuid4().hex[:8]
    base.mkdir(parents=True, exist_ok=True)
    yield base
    import shutil

    shutil.rmtree(base, ignore_errors=True)
