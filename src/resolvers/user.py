from src.models.user import User as UserModel
from src.resolvers import Base as BaseResolver


class User(BaseResolver):
    model = UserModel
