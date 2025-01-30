from app.database import get_session
from app.service import UsersService


def deactivate_inactive_users():
    for session in get_session():
        UsersService.deactivate_inactive_users(database=session)
