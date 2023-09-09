import strawberry
from strawberry.types import Info

from src.api.connection import Connection, to_connection
from src.api.definitions.user import UserNode
from src.db.engine import sessionmanager
from src.resolvers.user import User as UserResolver


@strawberry.type
class Query:
    @strawberry.field
    async def users(self, info: Info) -> Connection[UserNode]:
        async with sessionmanager.session() as session:
            users = await UserResolver.get_all(session)
            return to_connection(node_type=UserNode, target=users)
