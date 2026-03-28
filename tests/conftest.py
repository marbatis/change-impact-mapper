from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db_url = f"sqlite:///{tmp_path / 'impact_test.db'}"
    monkeypatch.setenv("DATABASE_URL", db_url)

    from app.config import get_settings
    from app.db import configure_database, init_db
    from app.main import app

    get_settings.cache_clear()
    configure_database(db_url)
    init_db()

    with TestClient(app) as tc:
        yield tc
