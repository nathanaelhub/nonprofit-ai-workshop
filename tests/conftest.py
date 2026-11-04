import pytest

from workshop.build import build


@pytest.fixture(scope="session")
def site(tmp_path_factory):
    return build(tmp_path_factory.mktemp("site") / "_site")
