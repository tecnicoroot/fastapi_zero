from sqlalchemy.orm import Session

from fastapi_zero.database import get_session


def test_get_session():
    session_generator = get_session()

    session = next(session_generator)

    assert isinstance(session, Session)

    session_generator.close()
