import logging
import pytest

from defi_protocols import add_stderr_logger

def pytest_configure(config):
    config.run_extra_code_executed = False

def pytest_addoption(parser):
    parser.addoption("--log-stderr", action="store_true", help="Setup a logging handler that logs to stderr.")

@pytest.fixture(autouse=True)
def log_stderr(request):
    if not request.config.run_extra_code_executed:
        if request.config.getoption("--log-stderr"):
            add_stderr_logger(logging.DEBUG)
    request.config.run_extra_code_executed = True

