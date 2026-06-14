import pytest

@pytest.mark.integration
def test_test_database_url_is_used(engine):
    assert engine.url.drivername == "postgresql+asyncpg"
    assert engine.url.username == "postgres"
    assert engine.url.password == "1234"
    assert engine.url.host == "localhost"
    assert engine.url.port == 5432
    assert engine.url.database == "test_db"