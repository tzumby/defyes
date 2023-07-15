import logging

import diskcache
import pytest

from defyes import add_stderr_logger


def pytest_addoption(parser):
    parser.addoption("--debug-defiproto", action="store_true", help="Setup a logging handler that logs to stderr.")


@pytest.fixture(autouse=True, scope="session")
def debug_defi_proto(request):
    if request.config.getoption("--debug-defiproto"):
        add_stderr_logger(logging.DEBUG)


@pytest.fixture
def temporary_cache(monkeypatch):
    monkeypatch.setattr("defyes.cache._cache", diskcache.Cache())


@pytest.fixture
def disable_cache(monkeypatch):
    monkeypatch.setattr("defyes.cache._cache", None)
