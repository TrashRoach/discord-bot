from typing import TYPE_CHECKING, Annotated, Optional

import strawberry
from strawberry.types import Info

from src.api.connection import Connection, to_connection
from src.models.user import User as UserModel

if TYPE_CHECKING:
    from src.api.definitions.guild import GuildNode
    from src.api.definitions.member import MemberNode


@strawberry.type
class UserNode:
    # Changed to float for bigint repr
    # "Int cannot represent non 32-bit signed integer value: 123456789012345678"
    id: float = strawberry.field(description=UserModel.id.__doc__)
    name: str = strawberry.field(description=UserModel.name.__doc__)
    global_name: Optional[str] = strawberry.field(description=UserModel.global_name.__doc__)
    avatar_url: Optional[str] = strawberry.field(description=UserModel.avatar_url.__doc__)
    bot: bool = strawberry.field(description=UserModel.bot.__doc__)

    @strawberry.field
    def owner_of(
        self,
        info: Info,
        # filters: Optional[GuildFilter] = None,
    ) -> Connection[Annotated['GuildNode', strawberry.lazy('src.api.definitions.guild')]]:
        return to_connection(node_type='GuildNode', relationship_field=self.owner_of)

    @strawberry.field
    def known_as(
        self,
        info: Info,
        # filters: Optional[MemberFilter] = None,
    ) -> Connection[Annotated['MemberNode', strawberry.lazy('src.api.definitions.member')]]:
        return to_connection(node_type='MemberNode', relationship_field=self.known_as)
