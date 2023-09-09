from typing import TYPE_CHECKING, Annotated

import strawberry

from src.api.connection import Connection, to_connection
from src.models.guild import Guild as GuildModel

if TYPE_CHECKING:
    from src.api.definitions.member import MemberNode
    from src.api.definitions.user import UserNode


@strawberry.type
class GuildNode:
    id: float = strawberry.field(
        description=GuildModel.id.__doc__
    )  # Int cannot represent non 32-bit signed integer value: xxxxxxxxxxxxxxxxxx
    name: str = strawberry.field(description=GuildModel.name.__doc__)
    owner_id: float = strawberry.field(description=GuildModel.owner_id.__doc__)
    owner: Annotated['UserNode', strawberry.lazy('src.api.definitions.user')]

    @strawberry.field
    def members(self) -> Connection[Annotated['MemberNode', strawberry.lazy('src.api.definitions.member')]]:
        return to_connection(node_type='MemberNode', target=self.members)
