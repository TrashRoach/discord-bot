from typing import TYPE_CHECKING, Annotated, Optional

import strawberry

from src.api.connection import Connection, to_connection
from src.api.filters import MemberFilter
from src.models.guild import Guild as GuildModel

if TYPE_CHECKING:
    from src.api.definitions.member import MemberNode
    from src.api.definitions.user import UserNode


@strawberry.type
class GuildNode:
    # Changed to float for bigint repr
    # "Int cannot represent non 32-bit signed integer value: 123456789012345678"
    id: float = strawberry.field(description=GuildModel.id.__doc__)

    name: str = strawberry.field(description=GuildModel.name.__doc__)
    owner_id: float = strawberry.field(description=GuildModel.owner_id.__doc__)
    owner: Annotated['UserNode', strawberry.lazy('src.api.definitions.user')]

    @strawberry.field
    def members(
        self,
        filters: Optional[MemberFilter] = None,  # TODO: Integrate nested filters (Dataloader?)
    ) -> Connection[Annotated['MemberNode', strawberry.lazy('src.api.definitions.member')]]:
        return to_connection(node_type='MemberNode', relationship_field=self.members)
