import os

import pytest


def pytest_configure(config):
    """Register the custom marker to avoid warnings."""
    config.addinivalue_line(
        "markers", "local_only: Run this test only in a local environment"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Skip tests marked with `local_only` if not running in a local environment."""
    if "local_only" in item.keywords and os.getenv("ENVIRONMENT") != "local":
        pytest.skip(
            "Skipping test because it's not running in a local environment"
        )
