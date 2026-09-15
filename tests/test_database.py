import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session


@pytest.mark.asyncio
async def test_get_session():
    asession_generator = get_session()

    session = await anext(asession_generator)

    assert isinstance(session, AsyncSession)

    await asession_generator.aclose()
