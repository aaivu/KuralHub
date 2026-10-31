import os

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "local_only: needs network access and model downloads"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if "local_only" in item.keywords and os.getenv("ENVIRONMENT") != "local":
        pytest.skip("set ENVIRONMENT=local to run")
