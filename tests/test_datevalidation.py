import pytest
from datetime import datetime
from .data_sets import DataWithSets
from src.oai_repo.repository import OAIRepository
from src.oai_repo.exceptions import OAIErrorBadArgument

repo = OAIRepository(DataWithSets(timestamp=True))

@pytest.mark.parametrize(
    ('date'),
    [
        '2017-01-01T00:00:00Z',
        '2023-09-19'
    ]
)
def test_valid_dates(date: str):
    assert isinstance(repo.valid_date(date), datetime)

@pytest.mark.parametrize(
    ('date'),
    [
        '2017/01/01T00-00-00Z',
        '2023.09.19T12/54/00Z'
    ]
)
def test_invalid_dates(date: str):
    with pytest.raises(OAIErrorBadArgument):
        repo.valid_date(date)
