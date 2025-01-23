from database import get_session, Session
from typing import Annotated
from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_session)]
